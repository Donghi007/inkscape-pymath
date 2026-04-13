import pytest
from math_formula.renderer import render_latex, render_mathml

def test_render_latex_basic():
    # 测试基础 LaTeX 渲染
    latex = r"\frac{1}{2}"
    svg = render_latex(latex)
    assert "<svg" in svg
    assert "<path" in svg

def test_render_latex_complex():
    # 测试更复杂的 LaTeX 渲染
    latex = r"\sqrt{x^2 + y^2} = z"
    svg = render_latex(latex, size=24, color="#ff0000")
    assert 'fill="#ff0000"' in svg.lower()
    assert "24" in svg or "24" in svg # ziamath 可能会将 size 编码在 viewBox 或样式中

def test_render_mathml_basic():
    # 测试基础 MathML 渲染
    mathml = """
    <math xmlns="http://www.w3.org/1998/Math/MathML">
      <mfrac>
        <mn>1</mn>
        <mn>2</mn>
      </mfrac>
    </math>
    """
    svg = render_mathml(mathml)
    assert "<svg" in svg
    assert "<path" in svg

def test_render_invalid_latex():
    # 测试无效 LaTeX 输入 (例如不匹配的括号)
    with pytest.raises(RuntimeError):
        render_latex(r"{")
