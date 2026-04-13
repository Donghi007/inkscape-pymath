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
        pars.add_argument("--pos_type", type=str, default="viewport", help="插入位置类型")
        pars.add_argument("--ungroup", type=inkex.Boolean, default=False, help="插入后取消组合")
        # 实时预览
        pars.add_argument("--tab", type=str, help="当前激活的标签页")

    def effect(self):
        # 获取用户参数
        formula_str = self.options.formula
        input_type = self.options.input_type
        font = self.options.font
        size = self.options.size
        color = color_to_hex(self.options.color)
        pos_type = self.options.pos_type
        should_ungroup = self.options.ungroup

        if not formula_str:
            return

        try:
            # 渲染为 SVG
            if input_type == "latex":
                svg_xml = render_latex(formula_str, font=font, size=size, color=color)
            else:
                svg_xml = render_mathml(formula_str, font=font, size=size, color=color)

            # 将 SVG 字符串解析为 lxml 元素
            svg_element = etree.fromstring(svg_xml.encode('utf-8'))
            
            # 创建一个临时的组，用来组织渲染出来的路径
            temp_group = Group()
            for child in svg_element:
                temp_group.append(child)
            
            # 必须先将组加入文档树，inkex 才能计算它的 bounding box (bbox)
            # 否则会报 "Element fragment does not have a document root" 错误
            self.svg.append(temp_group)
            
            # 获取公式自身的中心点，用于将其“归零”
            bbox = temp_group.bounding_box()
            offset_transform = inkex.Transform()
            if bbox:
                # 计算平移量，使公式中心对齐到 (0,0)
                dx, dy = -bbox.center.x, -bbox.center.y
                offset_transform = inkex.Transform(translate=(dx, dy))
            
            # 从临时位置移除
            temp_group.getparent().remove(temp_group)

            # 确定目标插入位置 (画布坐标)
            center_x, center_y = 0, 0
            try:
                if pos_type == "selection" and self.svg.selection:
                    sel_bbox = self.svg.selection.bounding_box()
                    if sel_bbox:
                        center_x, center_y = sel_bbox.center
                elif pos_type == "viewport":
                    if hasattr(self.svg, "get_viewport"):
                        center_x, center_y = self.svg.get_viewport().center
                    elif hasattr(self.svg, "get_center_position"):
                        center_x, center_y = self.svg.get_center_position()
                elif pos_type == "center":
                    width = self.svg.viewbox_width
                    height = self.svg.viewbox_height
                    center_x, center_y = width / 2, height / 2
                elif pos_type == "origin":
                    center_x, center_y = 0, 0
                else:
                    vbox = self.svg.get_viewbox()
                    if vbox:
                        center_x = vbox[0] + vbox[2] / 2
                        center_y = vbox[1] + vbox[3] / 2
            except:
                pass

            # 获取当前图层
            layer = self.svg.get_current_layer()
            
            # 计算最终的变换矩阵：先归零，再移动到目标位置
            final_move = inkex.Transform(translate=(center_x, center_y)) @ offset_transform

            if should_ungroup:
                # 插入后取消组合：直接将路径加入图层并应用变换
                for child in temp_group:
                    child.transform @= final_move
                    layer.append(child)
            else:
                # 保持组合：创建一个正式的组
                new_group = Group()
                new_group.label = f"Math: {formula_str[:20]}"
                for child in temp_group:
                    new_group.append(child)
                new_group.transform @= final_move
                layer.append(new_group)

        except Exception as e:
            inkex.errormsg(f"渲染公式时出错: {str(e)}")

if __name__ == "__main__":
    MathFormulaExtension().run()
