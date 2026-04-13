import ziamath
from typing import Optional
import re

def render_latex(latex_str: str, font: Optional[str] = None, size: float = 12, color: str = "black") -> str:
    """
    使用 ziamath 将 LaTeX 渲染为 SVG 路径。
    """
    try:
        # 处理换行逻辑：
        # 1. 统一将字面量的 \n (两个字符) 转换为真实换行符
        # 2. 使用 splitlines() 拆分，会自动处理各种平台的换行符 (\n, \r\n)
        # 3. 用空格重新连接，确保 LaTeX 引擎看到的是连续的一行，且不会被误认为有 \n 字符
        clean_lines = [line.strip() for line in latex_str.replace('\\n', '\n').splitlines()]
        latex_str = ' '.join(clean_lines).strip()
        
        if font == "STIXTwoMath-Regular":
            font = None
            
        formula = ziamath.Latex(latex_str, size=size, color=color, font=font)
        return formula.svg()
    except Exception as e:
        if "Font has no MATH table" in str(e):
            raise RuntimeError(f"字体错误: 所选字体 '{font}' 不支持数学公式排版 (缺少 MATH 表)。请使用内置的 STIX 字体或其它数学字体。")
        raise RuntimeError(f"LaTeX 渲染错误: {str(e)}")

def render_mathml(mathml_str: str, font: Optional[str] = None, size: float = 12, color: str = "black") -> str:
    """
    使用 ziamath 将 MathML 渲染为 SVG 路径。
    """
    try:
        # 清理多余空白
        clean_lines = [line.strip() for line in mathml_str.replace('\\n', '\n').splitlines()]
        mathml_str = ''.join(clean_lines).strip()
        mathml_str = re.sub(r'>\s+<', '><', mathml_str)
        
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
