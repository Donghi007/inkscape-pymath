import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inkex
from inkex import Group, Layer, TextElement
from lxml import etree
from math_formula_core.renderer import render_latex, render_mathml
from math_formula_core.utils import color_to_hex

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
            svg_element = etree.fromstring(svg_xml.encode('utf-8'))
            
            # 创建一个组，并将渲染结果放入
            # 我们只需要 svg 内部的内容
            new_group = Group()
            new_group.label = f"Math Formula: {formula_str[:20]}"
            
            for child in svg_element:
                new_group.append(child)

            # 确定插入位置
            center_x, center_y = 0, 0
            
            try:
                if self.svg.selection:
                    # 如果有选中，使用选中物体的中心
                    bbox = self.svg.selection.bounding_box()
                    if bbox:
                        center_x, center_y = bbox.center
                else:
                    # 尝试多种方法获取画布中心
                    if hasattr(self.svg, "get_viewport"):
                        center_x, center_y = self.svg.get_viewport().center
                    elif hasattr(self.svg, "get_center_position"):
                        center_x, center_y = self.svg.get_center_position()
                    elif hasattr(self.svg, "namedview") and self.svg.namedview is not None:
                        # 尝试从 namedview 获取
                        nv = self.svg.namedview
                        center_x = float(nv.get('inkscape:cx', 0))
                        center_y = float(nv.get('inkscape:cy', 0))
                    else:
                        # 最后的保底方案: 使用视图框 (viewBox) 的中心
                        vbox = self.svg.get_viewbox()
                        if vbox:
                            center_x = vbox[0] + vbox[2] / 2
                            center_y = vbox[1] + vbox[3] / 2
            except:
                # 即使出错也保持 (0,0)
                pass

            # 应用位移
            # 使用更兼容的 Transform 语法
            new_group.transform @= inkex.Transform(translate=(center_x, center_y))
            self.svg.get_current_layer().append(new_group)

        except Exception as e:
            inkex.errormsg(f"渲染公式时出错: {str(e)}")

if __name__ == "__main__":
    MathFormulaExtension().run()
