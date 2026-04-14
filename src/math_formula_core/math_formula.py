import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import inkex
from inkex import Group, Layer
from lxml import etree
from math_formula_core.renderer import render_latex, render_mathml
from math_formula_core.utils import color_to_hex

class MathFormulaExtension(inkex.EffectExtension):
    """
    Inkscape 扩展: 在画布中插入数学公式 (LaTeX/MathML)。
    """
    def add_arguments(self, pars):
        pars.add_argument("--formula", type=str, default=r"\frac{1}{2}", help="LaTeX 或 MathML 公式内容")
        pars.add_argument("--input_type", type=str, default="latex", help="输入类型: latex 或 mathml")
        pars.add_argument("--font", type=str, default="STIXTwoMath-Regular", help="渲染字体")
        pars.add_argument("--size", type=float, default=12.0, help="字号 (pt)")
        pars.add_argument("--color", type=str, default="#000000", help="颜色 (HEX)")
        pars.add_argument("--pos_type", type=str, default="viewport", help="插入位置类型")
        pars.add_argument("--ungroup", type=inkex.Boolean, default=False, help="插入后取消组合")
        pars.add_argument("--tab", type=str, help="当前激活的标签页")

    def effect(self):
        formula_str = self.options.formula
        if formula_str:
            formula_str = formula_str.replace('\\n', '\n')
            
        input_type = self.options.input_type
        font = self.options.font
        size = self.options.size
        color = color_to_hex(self.options.color)
        pos_type = self.options.pos_type
        should_ungroup = self.options.ungroup

        if not formula_str:
            return

        try:
            if input_type == "latex":
                svg_xml = render_latex(formula_str, font=font, size=size, color=color)
            else:
                svg_xml = render_mathml(formula_str, font=font, size=size, color=color)

            svg_element = etree.fromstring(svg_xml.encode('utf-8'))
            
            symbols = {}
            for sym in svg_element.findall('.//{http://www.w3.org/2000/svg}symbol'):
                sym_id = sym.get('id')
                if sym_id:
                    symbols['#' + sym_id] = sym
            
            flat_group = Group()
            
            for child in svg_element:
                tag = etree.QName(child).localname
                
                if tag == 'symbol':
                    continue
                
                if tag == 'use':
                    href = child.get('href', '')
                    if href in symbols:
                        sym = symbols[href]
                        sym_vbox = sym.get('viewBox')
                        if sym_vbox:
                            parts = sym_vbox.split()
                            sym_origin_x = float(parts[0])
                            sym_origin_y = float(parts[1])
                            sym_width = float(parts[2])
                            sym_height = float(parts[3])
                        else:
                            sym_origin_x = 0
                            sym_origin_y = 0
                            sym_width = float(sym.get('width', 0))
                            sym_height = float(sym.get('height', 0))
                        
                        use_x = float(child.get('x', 0))
                        use_y = float(child.get('y', 0))
                        use_width = float(child.get('width', sym_width))
                        use_height = float(child.get('height', sym_height))
                        
                        scale_x = use_width / sym_width if sym_width != 0 else 1
                        scale_y = use_height / sym_height if sym_height != 0 else 1
                        
                        translate_x = use_x - sym_origin_x * scale_x
                        translate_y = use_y - sym_origin_y * scale_y
                        
                        for path_elem in sym.findall('.//{http://www.w3.org/2000/svg}path'):
                            new_path = etree.SubElement(flat_group, '{http://www.w3.org/2000/svg}path')
                            new_path.set('d', path_elem.get('d', ''))
                            
                            path_fill = path_elem.get('fill', '')
                            path_style = path_elem.get('style', '')
                            child_fill = child.get('fill', '')
                            child_style = child.get('style', '')
                            
                            if child_fill:
                                new_path.set('fill', child_fill)
                            elif path_fill:
                                new_path.set('fill', path_fill)
                            else:
                                new_path.set('fill', color)
                            
                            if child_style:
                                new_path.set('style', child_style)
                            elif path_style:
                                new_path.set('style', path_style)
                                    
                            if not new_path.get('fill'):
                                new_path.set('fill', color)
                                    
                            transform_str = f"translate({translate_x}, {translate_y}) scale({scale_x}, {scale_y})"
                            new_path.set('transform', transform_str)
                    continue
                
                if tag == 'rect':
                    fill = child.get('fill', '').lower()
                    stroke = child.get('stroke', '').lower()
                    style = child.get('style', '').lower()
                    
                    is_fill_none = (fill == 'none' or 'fill:none' in style)
                    is_stroke_none = (stroke == 'none' or 'stroke:none' in style)
                    
                    if is_fill_none and is_stroke_none:
                        continue
                    
                    flat_group.append(child)
                    continue
                
                if tag == 'path':
                    flat_group.append(child)
                    continue
            
            if len(flat_group) == 0:
                return
            
            self.svg.append(flat_group)
            
            bbox = flat_group.bounding_box()
            offset_transform = inkex.Transform()
            if bbox:
                dx, dy = -bbox.center.x, -bbox.center.y
                offset_transform = inkex.Transform(translate=(dx, dy))
            
            flat_group.getparent().remove(flat_group)

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

            layer = self.svg.get_current_layer()
            
            final_move = inkex.Transform(translate=(center_x, center_y)) @ offset_transform

            if should_ungroup:
                for child in flat_group:
                    if child.get('transform'):
                        existing = inkex.Transform(child.get('transform'))
                        combined = existing @ final_move
                        child.set('transform', str(combined))
                    else:
                        child.set('transform', str(final_move))
                    layer.append(child)
            else:
                new_group = Group()
                new_group.label = f"Math: {formula_str[:20]}"
                for child in flat_group:
                    new_group.append(child)
                new_group.transform = final_move
                layer.append(new_group)

        except Exception as e:
            import traceback
            inkex.errormsg(f"渲染公式时出错: {str(e)}\n{traceback.format_exc()}")

if __name__ == "__main__":
    MathFormulaExtension().run()
