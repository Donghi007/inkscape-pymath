import inkex
from inkex import Group, Layer, TextElement
from math_formula.renderer import render_latex, render_mathml
from math_formula.utils import color_to_hex

class MathFormulaExtension(inkex.EffectExtension):
    """
    Inkscape 扩展: 在画布中插入数学公式 (LaTeX/MathML)。
    """
    def add_arguments(self, pars):
        # 定义 INX 文件中传递的参数
        pars.add_argument("--formula", type=str, default=r"\frac{1}{2}", help="LaTeX 或 MathML 公式内容")
        pars.add_argument("--input_type", type=str, default="latex", help="输入类型: latex 或 mathml")
        pars.add_argument("--font", type=str, default="STIXTwoMath-Regular", help="渲染字体")
        pars.add_argument("--size", type=float, default=12.0, help="字号 (pt)")
        pars.add_argument("--color", type=str, default="#000000", help="颜色 (HEX)")
        # 实时预览
        pars.add_argument("--tab", type=str, help="当前激活的标签页")

    def effect(self):
        # 获取用户参数
        formula_str = self.options.formula
        input_type = self.options.input_type
        font = self.options.font
        size = self.options.size
        color = color_to_hex(self.options.color)

        if not formula_str:
            return

        try:
            # 渲染为 SVG
            if input_type == "latex":
                svg_xml = render_latex(formula_str, font=font, size=size, color=color)
            else:
                svg_xml = render_mathml(formula_str, font=font, size=size, color=color)

            # 将 SVG 字符串解析为 lxml 元素
            # ziamath 返回的是完整的 <svg>，我们需要将其转换为 Inkscape 可识别的组或路径
            svg_element = inkex.utils.etree.fromstring(svg_xml.encode('utf-8'))
            
            # 创建一个组，并将渲染结果放入
            # 我们只需要 svg 内部的内容
            new_group = Group()
            new_group.label = f"Math Formula: {formula_str[:20]}"
            
            for child in svg_element:
                new_group.append(child)

            # 确定插入位置: 如果有选中，放在选中位置；否则放在画布中心
            if self.svg.get_selection():
                # 插入到选中的第一个对象上方
                target = self.svg.get_selection()[0]
                target.getparent().append(new_group)
                # 简单居中对齐到目标
                bbox = target.bounding_box()
                if bbox:
                    new_group.transform.add_translation(bbox.center.x, bbox.center.y)
            else:
                # 插入到当前层，位置设为 (0,0) 或视图中心
                view_center = self.svg.get_center_position()
                new_group.transform.add_translation(view_center[0], view_center[1])
                self.svg.get_current_layer().append(new_group)

        except Exception as e:
            inkex.errormsg(f"渲染公式时出错: {str(e)}")

if __name__ == "__main__":
    MathFormulaExtension().run()
