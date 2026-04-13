import ziamath
from typing import Optional
import re

def render_latex(latex_str: str, font: Optional[str] = None, size: float = 12, color: str = "black") -> str:
    """
    使用 ziamath 将 LaTeX 渲染为 SVG 路径。
    """
    try:
        # ziamath.Latex 支持 color 参数
        formula = ziamath.Latex(latex_str, size=size, color=color, font=font)
        return formula.svg()
    except Exception as e:
        # ziamath 可能不会对所有语法错误抛出 RuntimeError，我们需要确保能捕获并转换
        raise RuntimeError(f"LaTeX 渲染错误: {str(e)}")

def render_mathml(mathml_str: str, font: Optional[str] = None, size: float = 12, color: str = "black") -> str:
    """
    使用 ziamath 将 MathML 渲染为 SVG 路径。
    """
    try:
        # Math 对象不支持 color 参数，我们需要在 MathML 字符串中注入 mathcolor
        if color and 'mathcolor' not in mathml_str:
            # 简单处理：在 <math 标签中注入 mathcolor
            mathml_str = re.sub(r'(<math[^>]*)>', rf'\1 mathcolor="{color}">', mathml_str)
        
        formula = ziamath.Math(mathml_str, size=size, font=font)
        return formula.svg()
    except Exception as e:
        raise RuntimeError(f"MathML 渲染错误: {str(e)}")
