import os
import sys
import re
import struct
import glob
import inkex
import ziamath as zm
from lxml import etree as ElementTree

NS_SVG = "http://www.w3.org/2000/svg"


def _has_math_table(font_path):
    """快速检测 TTF/OTF 字体文件是否包含 MATH table"""
    try:
        with open(font_path, "rb") as f:
            header = f.read(12)
            if len(header) < 12:
                return False
            sf_version = struct.unpack(">I", header[:4])[0]
            num_tables = struct.unpack(">H", header[4:6])[0]
            f.seek(12)
            for _ in range(min(num_tables, 100)):
                entry = f.read(16)
                if len(entry) < 16:
                    break
                tag = entry[:4].decode("ascii", errors="ignore")
                if tag == "MATH":
                    return True
    except Exception:
        pass
    return False


def _scan_math_fonts(plugin_dir):
    """扫描插件目录和 math_fonts/ 中的数学字体

    Returns:
        dict: {字体显示名: 绝对文件路径}
    """
    fonts = {}

    # 1. 内置默认字体
    builtin = os.path.join(plugin_dir, "ziamath", "fonts", "STIXTwoMath-Regular.ttf")
    if os.path.isfile(builtin):
        fonts["STIX Two Math (Built-in)"] = builtin

    # 2. 用户 math_fonts/ 目录
    user_dir = os.path.join(plugin_dir, "math_fonts")
    if os.path.isdir(user_dir):
        for ext in ("*.ttf", "*.otf", "*.TTF", "*.OTF"):
            for fp in glob.glob(os.path.join(user_dir, ext)):
                if _has_math_table(fp):
                    name = os.path.splitext(os.path.basename(fp))[0]
                    fonts[name] = fp

    # 3. 系统常见数学字体路径（Linux）
    system_globs = [
        "/usr/share/fonts/truetype/latin-modern/*.otf",
        "/usr/share/fonts/opentype/latin-modern/*.otf",
        "/usr/share/fonts/truetype/libertinus/*.otf",
        "/usr/share/fonts/opentype/libertinus/*.otf",
        "/usr/share/fonts/truetype/stix/*.otf",
        "/usr/share/fonts/opentype/stix/*.otf",
        "/usr/share/fonts/opentype/xits/*.otf",
        "/usr/share/fonts/opentype/asana-math/*.otf",
        os.path.expanduser("~/.fonts/*.otf"),
        os.path.expanduser("~/.local/share/fonts/*.otf"),
    ]
    for pattern in system_globs:
        for fp in glob.glob(pattern):
            if _has_math_table(fp) and os.path.basename(fp) not in fonts:
                name = os.path.splitext(os.path.basename(fp))[0]
                fonts[name] = fp

    return fonts


class LatexMathExtension(inkex.EffectExtension):
    """将 LaTeX 数学公式渲染为 SVG 并插入到当前文档中"""

    def add_arguments(self, pars):
        pars.add_argument(
            "--tab",
            type=str,
            default="formula",
            help="Selected notebook tab",
        )
        pars.add_argument(
            "--latex_string",
            type=str,
            default="",
            help="LaTeX math formula string",
        )
        pars.add_argument(
            "--font_size",
            type=float,
            default=24.0,
            help="Font size in points",
        )
        pars.add_argument(
            "--inline",
            type=inkex.Boolean,
            default=False,
            help="Use inline math mode instead of display mode",
        )
        pars.add_argument(
            "--font_preset",
            type=str,
            default="latin-modern",
            help="Predefined font selection",
        )
        pars.add_argument(
            "--font_file",
            type=str,
            default="",
            help="Path to a math-enabled .ttf/.otf font file (for custom preset)",
        )

    # LaTeX 命令中以 \n 开头的完整白名单
    _N_COMMANDS = frozenset({
        r"\nabla", r"\neq", r"\neg", r"\ni", r"\not", r"\nu",
        r"\natural", r"\nmid", r"\nsubseteq", r"\nsupseteq",
        r"\nless", r"\ngtr", r"\nleq", r"\ngeq",
        r"\nwarrow", r"\nnearrow", r"\nparallel",
        r"\nrightarrow", r"\nleftarrow", r"\nLeftarrow", r"\nRightarrow",
        r"\napprox", r"\nsim", r"\ncong",
        r"\nvDash", r"\nvdash", r"\nVDash",
    })

    def _remove_stray_n(self, s):
        """移除所有不是 LaTeX 命令的孤立 \\n"""
        result = []
        i = 0
        cmds = sorted(self._N_COMMANDS, key=len, reverse=True)
        while i < len(s):
            if s[i : i + 2] == "\\n":
                matched = False
                for cmd in cmds:
                    if s[i : i + len(cmd)] == cmd:
                        result.append(cmd)
                        i += len(cmd)
                        matched = True
                        break
                if not matched:
                    i += 2  # 跳过孤立 \n
            else:
                result.append(s[i])
                i += 1
        return "".join(result)

    def _normalize_latex(self, latex_str):
        """修复 Inkscape 多行输入框的编码问题

        Inkscape 将 Enter 编码为字面 \\n（反斜杠+n），需转为真实换行。
        三步处理：
          1. 保护 LaTeX \\\\（分行命令）
          2. \\n → 真实换行（仅当不后跟字母时——这步会漏掉后跟字母的情况）
          3. 白名单移除：剩余 \\n 若不是 \\nabla 等合法命令则删除
        """
        MARKER = "\x00DBL\x00"
        latex_str = latex_str.replace("\\\\", MARKER)
        latex_str = re.sub(r"\\n(?!\w)", "\n", latex_str)
        latex_str = latex_str.replace(MARKER, "\\\\")
        latex_str = self._remove_stray_n(latex_str)
        latex_str = re.sub(r"\n{3,}", "\n\n", latex_str)
        return latex_str.strip()

    # enum value → math_fonts/ 中的文件名映射
    FONT_PRESET_MAP = {
        "latin-modern": "LatinModern-Math.otf",
        "xits": "XITSMath-Regular.otf",
        "libertinus": "LibertinusMath-Regular.otf",
        "stix-two": None,  # 内置字体，路径在 _resolve_font 中处理
        "custom": None,    # 使用 font_file 参数
    }

    def _resolve_font(self):
        """根据预设下拉框或文件选择器确定字体路径"""
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        preset = self.options.font_preset

        if preset == "custom":
            user_font = self.options.font_file.strip()
            if not user_font:
                inkex.errormsg(
                    "Custom font selected but no file chosen.\n"
                    "Falling back to STIX Two Math."
                )
            elif not os.path.isfile(user_font):
                inkex.errormsg(
                    f"Font file not found, falling back to STIX Two Math:\n"
                    f"{user_font}"
                )
            elif not _has_math_table(user_font):
                inkex.errormsg(
                    f"Not a math font (no MATH table), falling back to STIX Two Math:\n"
                    f"{user_font}"
                )
            else:
                return user_font
            return self._get_builtin_font(plugin_dir)

        # 预设字体：在 math_fonts/ 中查找对应文件名
        if preset in self.FONT_PRESET_MAP and preset != "stix-two":
            expected = self.FONT_PRESET_MAP[preset]
            if expected:
                font_path = os.path.join(plugin_dir, "math_fonts", expected)
                if os.path.isfile(font_path) and _has_math_table(font_path):
                    return font_path
            inkex.errormsg(
                f"Preset font not found: {preset}\n"
                f"Falling back to STIX Two Math."
            )

        # stix-two 或任何回退
        return self._get_builtin_font(plugin_dir)

    def _get_builtin_font(self, plugin_dir):
        builtin = os.path.join(
            plugin_dir, "ziamath", "fonts", "STIXTwoMath-Regular.ttf"
        )
        if os.path.isfile(builtin):
            return builtin
        return None

    def effect(self):
        # 获取用户输入的 LaTeX 公式
        latex_str = self.options.latex_string.strip()
        if not latex_str:
            inkex.errormsg("Please enter a LaTeX math formula.")
            return

        # 修正 Inkscape 多行输入框的编码
        latex_str = self._normalize_latex(latex_str)

        font_size = self.options.font_size
        inline_mode = self.options.inline
        font_path = self._resolve_font()

        # 使用 ziamath 将 LaTeX 渲染为 SVG 字符串
        try:
            math_obj = zm.Latex(
                latex_str,
                size=font_size,
                inline=inline_mode,
                font=font_path,
            )
            svg_str = math_obj.svg()
        except Exception as e:
            inkex.errormsg(
                f"Failed to render LaTeX formula.\n\n"
                f"Formula: {latex_str}\n"
                f"Error: {e}"
            )
            return

        # 解析生成的 SVG
        try:
            svg_root = ElementTree.fromstring(svg_str.encode("utf-8"))
        except Exception as e:
            inkex.errormsg(f"Failed to parse generated SVG: {e}")
            return

        # 将 defs 和 symbol 元素添加到文档的 <defs> 中
        # 注意：lxml 的 append() 是移动操作，会自动从原父节点移除
        doc_defs = self.get_or_create_defs()
        for child in list(svg_root):
            tag = ElementTree.QName(child).localname
            if tag == "defs":
                for sub_child in list(child):
                    doc_defs.append(sub_child)
                svg_root.remove(child)
            elif tag == "symbol":
                doc_defs.append(child)

        # 创建组元素放置渲染结果
        group = inkex.Group()
        group.label = "LaTeX Math"

        for child in svg_root:
            group.append(child)

        # 获取视口中心位置
        try:
            center = self.svg.namedview.center
            cx, cy = center.x, center.y
        except Exception:
            cx, cy = 0.0, 0.0

        group.transform = inkex.Transform(translate=(cx, cy))

        # 将组添加到当前图层
        layer = self.svg.get_current_layer()
        layer.append(group)

    def get_or_create_defs(self):
        """获取或创建文档的 <defs> 元素"""
        defs_list = self.svg.xpath("//svg:defs", namespaces={"svg": NS_SVG})
        if defs_list:
            return defs_list[0]
        defs_el = ElementTree.SubElement(self.svg, f"{{{NS_SVG}}}defs")
        return defs_el


if __name__ == "__main__":
    LatexMathExtension().run()
