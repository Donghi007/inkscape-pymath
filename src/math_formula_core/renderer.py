import ziamath
from typing import Optional
import re

def render_latex(latex_str: str, font: Optional[str] = None, size: float = 12, color: str = "black") -> str:
    """
    使用 ziamath 将 LaTeX 渲染为 SVG 路径。
    """
    try:
        # 如果是默认字体字符串，传 None 给 ziamath 以使用其内置的 STIXTwoMath
        if font == "STIXTwoMath-Regular":
            font = None
            
        formula = ziamath.Latex(latex_str, size=size, color=color, font=font)
        return formula.svg()
    except Exception as e:
        # 如果是因为字体缺少 MATH 表导致的错误，给出更友好的提示
        if "Font has no MATH table" in str(e):
            raise RuntimeError(f"字体错误: 所选字体 '{font}' 不支持数学公式排版 (缺少 MATH 表)。请使用内置的 STIX 字体或其它数学字体。")
        raise RuntimeError(f"LaTeX 渲染错误: {str(e)}")

def render_mathml(mathml_str: str, font: Optional[str] = None, size: float = 12, color: str = "black") -> str:
    """
    使用 ziamath 将 MathML 渲染为 SVG 路径。
    """
    try:
        if font == "STIXTwoMath-Regular":
            font = None
            
        if color and 'mathcolor' not in mathml_str:
            mathml_str = re.sub(r'(<math[^>]*)>', rf'\1 mathcolor="{color}">', mathml_str)
        
        formula = ziamath.Math(mathml_str, size=size, font=font)
        return formula.svg()
    except Exception as e:
        if "Font has no MATH table" in str(e):
            raise RuntimeError(f"字体错误: 所选字体 '{font}' 不支持数学公式排版 (缺少 MATH 表)。")
        raise RuntimeError(f"MathML 渲染错误: {str(e)}")
