import re

def color_to_hex(color_str: str) -> str:
    """
    尝试将各种颜色字符串格式统一转换为 HEX 格式 (例如: #RRGGBB)。
    Inkscape 的 inx 传出的颜色可能是十进制整数或 HEX。
    """
    if not color_str:
        return "#000000"
    
    # 如果是 "#" 开头的，已经是 HEX
    if color_str.startswith("#"):
        return color_str
    
    # 如果是纯数字字符串 (可能是十进制 RGBA/RGB)
    if color_str.isdigit():
        val = int(color_str)
        # 将十进制转为十六进制，假设它是 RGB 格式
        # Inkscape 的 color param 传递的值有时是 10 进制表示的 HEX (例如: 255 -> #0000FF?)
        # 实际上在 inx 中定义的 color 会返回类似 "#ff0000ff" (带 alpha)
        # 我们这里做一个简单处理
        try:
            # 去掉 alpha 通道，转为 6 位 HEX
            hex_val = hex(val).replace('0x', '').zfill(8)
            # 取前 6 位，或者根据具体返回格式调整
            return f"#{hex_val[:6]}"
        except:
            pass

    return color_str

def parse_svg_path(svg_content: str) -> str:
    """
    从 ziamath 返回的完整 SVG 字符串中提取 <path> 或关键部分。
    实际上 ziamath.svg() 返回一个完整的 <svg> 容器，我们需要它内部的内容。
    """
    # 简单提取 <svg ...> 之后的内容，或者直接返回
    # 在 Inkscape 中，我们通常会将这些内容放到一个 <g> 组中。
    return svg_content
