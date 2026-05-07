''' Latex to MathML interface '''
import re
import latex2mathml.tokenizer
import latex2mathml.commands
from latex2mathml.converter import convert

from .config import config


def declareoperator(name: str) -> None:
    r''' Declare a new operator name, similar to Latex ``\DeclareMathOperator`` command.

        Args:
            name: Name of operator, should start with a ``\``.
                Example: ``declareoperator(r'\myfunc')``
    '''
    latex2mathml.commands.FUNCTIONS = latex2mathml.commands.FUNCTIONS + (name,)  # type: ignore


def _fix_ce(tex: str) -> str:
    r''' Fix \\ce{...} chemical equation syntax.
        Convert mhchem-style notation to regular LaTeX.
    '''
    result = []
    i = 0
    while i < len(tex):
        if tex[i:i+4] == r'\ce{':
            i += 4
            depth = 1
            start_arg = i
            while i < len(tex) and depth > 0:
                if tex[i] == '{':
                    depth += 1
                elif tex[i] == '}':
                    depth -= 1
                i += 1
            ce_content = tex[start_arg:i-1]
            
            processed = []
            j = 0
            n = len(ce_content)
            
            while j < n:
                if j + 3 <= n and ce_content[j:j+3] == '<=>':
                    arrow_text = r' \rightleftharpoons '
                    j += 3
                    upper_text = None
                    lower_text = None
                    if j < n and ce_content[j] == '[':
                        j += 1
                        depth_bracket = 1
                        start_upper = j
                        while j < n and depth_bracket > 0:
                            if ce_content[j] == '[':
                                depth_bracket += 1
                            elif ce_content[j] == ']':
                                depth_bracket -= 1
                            j += 1
                        upper_text = ce_content[start_upper:j-1]
                    if j < n and ce_content[j] == '[':
                        j += 1
                        depth_bracket = 1
                        start_lower = j
                        while j < n and depth_bracket > 0:
                            if ce_content[j] == '[':
                                depth_bracket += 1
                            elif ce_content[j] == ']':
                                depth_bracket -= 1
                            j += 1
                        lower_text = ce_content[start_lower:j-1]
                    if upper_text:
                        processed.append(r' \overset{')
                        processed.append(upper_text)
                        processed.append(r'}{')
                        processed.append(arrow_text.strip())
                        processed.append(r'} ')
                    elif lower_text:
                        processed.append(r' \underset{')
                        processed.append(lower_text)
                        processed.append(r'}{')
                        processed.append(arrow_text.strip())
                        processed.append(r'} ')
                    else:
                        processed.append(arrow_text)
                elif j + 2 <= n and ce_content[j:j+2] == '->':
                    arrow_text = r' \rightarrow '
                    j += 2
                    upper_text = None
                    lower_text = None
                    if j < n and ce_content[j] == '[':
                        j += 1
                        depth_bracket = 1
                        start_upper = j
                        while j < n and depth_bracket > 0:
                            if ce_content[j] == '[':
                                depth_bracket += 1
                            elif ce_content[j] == ']':
                                depth_bracket -= 1
                            j += 1
                        upper_text = ce_content[start_upper:j-1]
                    if j < n and ce_content[j] == '[':
                        j += 1
                        depth_bracket = 1
                        start_lower = j
                        while j < n and depth_bracket > 0:
                            if ce_content[j] == '[':
                                depth_bracket += 1
                            elif ce_content[j] == ']':
                                depth_bracket -= 1
                            j += 1
                        lower_text = ce_content[start_lower:j-1]
                    if upper_text:
                        processed.append(r' \overset{')
                        processed.append(upper_text)
                        processed.append(r'}{')
                        processed.append(arrow_text.strip())
                        processed.append(r'} ')
                    elif lower_text:
                        processed.append(r' \underset{')
                        processed.append(lower_text)
                        processed.append(r'}{')
                        processed.append(arrow_text.strip())
                        processed.append(r'} ')
                    else:
                        processed.append(arrow_text)
                elif j + 2 <= n and ce_content[j:j+2] == '<-':
                    arrow_text = r' \leftarrow '
                    j += 2
                    upper_text = None
                    lower_text = None
                    if j < n and ce_content[j] == '[':
                        j += 1
                        depth_bracket = 1
                        start_upper = j
                        while j < n and depth_bracket > 0:
                            if ce_content[j] == '[':
                                depth_bracket += 1
                            elif ce_content[j] == ']':
                                depth_bracket -= 1
                            j += 1
                        upper_text = ce_content[start_upper:j-1]
                    if j < n and ce_content[j] == '[':
                        j += 1
                        depth_bracket = 1
                        start_lower = j
                        while j < n and depth_bracket > 0:
                            if ce_content[j] == '[':
                                depth_bracket += 1
                            elif ce_content[j] == ']':
                                depth_bracket -= 1
                            j += 1
                        lower_text = ce_content[start_lower:j-1]
                    if upper_text:
                        processed.append(r' \overset{')
                        processed.append(upper_text)
                        processed.append(r'}{')
                        processed.append(arrow_text.strip())
                        processed.append(r'} ')
                    elif lower_text:
                        processed.append(r' \underset{')
                        processed.append(lower_text)
                        processed.append(r'}{')
                        processed.append(arrow_text.strip())
                        processed.append(r'} ')
                    else:
                        processed.append(arrow_text)
                elif ce_content[j] == '^':
                    next_is_not_charge = j + 1 >= n or not (ce_content[j+1] in '+-' or ce_content[j+1].isdigit())
                    if next_is_not_charge:
                        processed.append(r' \uparrow ')
                        j += 1
                    else:
                        processed.append('^')
                        j += 1
                        if j < n and ce_content[j] != '{':
                            processed.append('{')
                            while j < n and (ce_content[j].isdigit() or ce_content[j] in '+-'):
                                processed.append(ce_content[j])
                                j += 1
                            processed.append('}')
                elif ce_content[j] == 'v':
                    prev_is_space = j == 0 or ce_content[j-1] in ' \t'
                    if prev_is_space or (j > 0 and ce_content[j-1] in ' \t'):
                        processed.append(r' \downarrow ')
                        j += 1
                    else:
                        processed.append(ce_content[j])
                        j += 1
                elif ce_content[j] == '_':
                    processed.append('_')
                    j += 1
                    if j < n and ce_content[j] != '{':
                        processed.append('{')
                        while j < n and ce_content[j].isdigit():
                            processed.append(ce_content[j])
                            j += 1
                        processed.append('}')
                elif ce_content[j] == '+':
                    if j > 0 and (ce_content[j-1].isalnum() or ce_content[j-1] == ']'):
                        if j > 1 and ce_content[j-2] == '^':
                            processed.append('+')
                        else:
                            processed.append('^{+}')
                    else:
                        processed.append(' + ')
                    j += 1
                elif ce_content[j] == '-':
                    if j > 0 and (ce_content[j-1].isalnum() or ce_content[j-1] == ']' or ce_content[j-1].isdigit()):
                        if j > 1 and ce_content[j-2] == '^':
                            processed.append('-')
                        else:
                            processed.append('^{-}')
                    else:
                        processed.append('-')
                    j += 1
                elif ce_content[j] in ' \t\n':
                    j += 1
                else:
                    processed.append(ce_content[j])
                    j += 1
            
            processed_str = ''.join(processed)
            processed_str = re.sub(r'([A-Za-z\)])(\d)', r'\1_{\2}', processed_str)
            result.append(r'\mathrm{')
            result.append(processed_str)
            result.append('}')
        else:
            result.append(tex[i])
            i += 1
    return ''.join(result)


def _fix_binom(tex: str) -> str:
    r''' Fix \\binom{}{} handling to support nested braces.
        \\binom{\cos\phi_{\mathrm{A}}}{-\sin\phi_{\mathrm{A}}}
    '''
    result = []
    i = 0
    while i < len(tex):
        if tex[i:i+7] == r'\binom{':
            result.append(r'\left( ')
            i += 7
            depth = 1
            start_arg1 = i
            while i < len(tex) and depth > 0:
                if tex[i] == '{':
                    depth += 1
                elif tex[i] == '}':
                    depth -= 1
                i += 1
            arg1 = tex[start_arg1:i-1]
            result.append(arg1)
            result.append(r' \atop ')
            if i < len(tex) and tex[i] == '{':
                i += 1
                depth = 1
                start_arg2 = i
                while i < len(tex) and depth > 0:
                    if tex[i] == '{':
                        depth += 1
                    elif tex[i] == '}':
                        depth -= 1
                    i += 1
                arg2 = tex[start_arg2:i-1]
                result.append(arg2)
            result.append(r' \right)')
        else:
            result.append(tex[i])
            i += 1
    return ''.join(result)


def _fix_mathrm_spaces(tex: str) -> str:
    ''' Fix spaces after \\mathrm, correctly handling nested braces '''
    result = []
    i = 0
    n = len(tex)
    while i < n:
        if tex[i:i+8] == r'\mathrm{':
            result.append(r'\mathrm {')
            i += 8
            depth = 1
            while i < n and depth > 0:
                if tex[i] == '{':
                    depth += 1
                elif tex[i] == '}':
                    depth -= 1
                result.append(tex[i])
                i += 1
        else:
            result.append(tex[i])
            i += 1
    return ''.join(result)


def tex2mml(tex: str, inline: bool = False) -> str:
    ''' Convert Latex to MathML. Do some hacky preprocessing to work around
        some issues with generated MathML that ziamath doesn't support yet.
    '''
    tex = _fix_ce(tex)
    tex = _fix_binom(tex)
    # latex2mathml bug requires space after mathrm
    tex = _fix_mathrm_spaces(tex)
    tex = tex.replace('||', '‖')
    tex = tex.replace(r'\begin{aligned}', r'\begin{align*}')
    tex = tex.replace(r'\end{aligned}', r'\end{align*}')

    if config.decimal_separator == ',':
        # Replace , with {,} to remove right space
        # (must be surrounded by digits)
        tex = re.sub(r'([0-9]),([0-9])', r'\1{,}\2', tex)

    mml = convert(tex, display='inline' if inline else 'block')

    # Tex \uparrow, \downarrow are not stretchy,
    # but in MathML they are (as drawn by Katex and Mathjax).
    # Keep the operators list as stretchy, but set to false when
    # processing tex.
    mml = re.sub(r'>&#x02191;', r' stretchy="false">&#x02191;', mml)  # \uparrow
    mml = re.sub(r'>&#x02193;', r' stretchy="false">&#x02193;', mml)  # \downarrow
    mml = re.sub(r'<mi>&#x027E8;', r'<mi stretchy="false">&#x027E8;', mml)  # \langle
    mml = re.sub(r'<mi>&#x027E9;', r'<mi stretchy="false">&#x027E9;', mml)  # \rangle

    # Replace some operators with "stretchy" variants
    mml = re.sub(r'<mo stretchy="false">&#x0005E;', r'<mo stretchy="false">&#710;', mml)  # hat
    mml = re.sub(r'<mo>&#x0005E;', r'<mo>&#x00302;', mml)  # widehat
    mml = re.sub(r'<mo>&#x0007E;', r'<mo>&#x00303;', mml)  # widetilde

    # shrink the huge column spacing in \align to something more reasonable
    mml = re.sub(r'columnspacing="0em 2em"', r'columnspacing="0em 0.3em"', mml)
    return mml
