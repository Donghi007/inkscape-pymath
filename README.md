# Inkscape 数学公式扩展 (Math Formula Extension)

> **[English Version](#english-version)** | **[英文版本](#english-version)**

***

## 中文版本

这是一个为矢量图形软件 Inkscape 开发的扩展插件，允许用户在画布中插入由 **ziamath** 渲染的数学公式。

## 核心特性

- **纯 Python 实现**: 不依赖 LaTeX 环境 (如 TeX Live, MiKTeX)，完全使用 Python 渲染。
- **支持 LaTeX & MathML**: 使用 LaTeX 语法 (例如 `\frac{1}{2}`) 或标准的 MathML。
- **SVG 矢量输出**: 公式渲染为 SVG 路径，保持高清晰度且可缩放。
- **样式自定义**: 支持设置字号、颜色和字体 (内置 STIX Two Math，支持其他数学字体)。

## 字体选择说明

由于 `ziamath` 库的特性，它要求使用的字体必须包含特殊的 **OpenType MATH 表** 才能正确排版数学公式。大多数普通系统字体不具备此特性。

插件的字体选择列表仅包含已知支持 MATH 表的字体：

- **STIX Two Math**: `ziamath` 内置，无需额外安装，推荐使用。
- **Cambria Math, Latin Modern Math, DejaVu Math TeX Gyre**: 这些是常见的数学字体，如果你的系统已安装它们，也可以选择使用。

**重要提示**: Inkscape 扩展的 UI (INX 文件) 无法动态获取系统字体列表。因此，我们无法提供一个像 Inkscape 自身那样的完整系统字体下拉菜单。请根据上述说明选择合适的字体。

## 环境要求

- Inkscape 1.0+ (自带 inkex 库，无需额外安装)
- Python 3.13+ (uv 虚拟环境会自动配置)
- `uv` 包管理工具


### 1. 安装

```bash
# 克隆项目
git clone <repository-url>
cd inkscape-pymath

# 安装 Python 依赖
uv sync
```

手动将以下两个文件或文件夹复制到inkscape的extension文件夹中即可完成安装。

- inx/math\_formula.inx
- src/math\_formula\_core/ (整个目录)

一般情况下extension路径为：

| 平台                  | 路径                                                             |
| ------------------- | -------------------------------------------------------------- |
| Linux (原生)          | `~/.config/inkscape/extensions`                                |
| Linux (Flatpak 推荐！) | `~/.var/app/org.inkscape.Inkscape/config/inkscape/extensions/` |
| macOS               | `~/Library/Application Support/inkscape/extensions`            |
| Windows             | `%APPDATA%\inkscape\extensions`                                |

若想卸载只需要移除刚才的文件以及文件夹即可。

### 2. 配置 Python 环境

**这是最关键的步骤！** Inkscape 使用自带的 Python 环境，而扩展所需的库 (`ziamath` 等) 安装在 uv 虚拟环境中。需要让 Inkscape 能访问这些库。
请参考scripts/inkscape-pythonSelect.sh 以及对应的说明文件inkscape-pythonSelect-README.md。支持conda虚拟环境。

### 3. 验证安装

1. 打开 Inkscape
2. 菜单栏点击: **扩展 > 文本 > 数学公式**
3. 在公式输入框中输入 `\frac{1}{2}` 或 `J_{xx}`
4. 点击 **应用**

如果公式正确渲染，说明安装成功！

## 卸载

移除安装时复制的文件以及文件夹即可完成卸载。
卸载后请重启 Inkscape。

## 使用说明

1. 打开 Inkscape。
2. 菜单栏点击: **扩展 > 文本 > 数学公式**。
3. 在弹出的对话框中输入公式。
4. 点击 **应用** 即可将公式插入画布。

**可用选项：**

- **字号**: 公式文字大小 (8-72 pt)
- **颜色**: 公式颜色 (HEX 值)
- **字体**: 选择数学字体 (需支持 OpenType MATH 表)
- **插入位置**:
  - 当前选中物体的中心
  - 当前画布视图的中心
  - 文档页面的几何中心
  - 坐标原点 (0,0)
- **取消组合**: 是否在插入后自动拆分公式元素

## 常见问题

### Q: 扩展菜单没有出现？

1. 确认扩展文件已正确安装到 Inkscape 扩展目录
2. 确认 Python 环境变量已正确设置
3. 重启 Inkscape

### Q: 公式显示为空白或报错 "No module named 'ziamath'"？

这是最常见的问题。`PYTHONPATH` 未正确设置。请参考上文的"配置 Python 环境"部分。

### Q: 公式位置不正确？

尝试选择不同的"插入位置"选项。

### Q: 如何编辑已插入的公式？

目前不支持直接编辑。需删除原公式，重新渲染。

### Q: 支持哪些 LaTeX 命令？

支持 ziamath 支持的大部分 LaTeX 数学命令，包括：

- 分数: `\frac{a}{b}`
- 上下标: `x^2`, `a_{i}`
- 根号: `\sqrt{x}`, `\sqrt[n]{x}`
- 积分: `\int_0^1 f(x)dx`
- 求和: `\sum_{i=0}^n`
- 矩阵: `\begin{matrix}...\end{matrix}`
- 等等

## 单元测试

项目包含针对公式渲染逻辑的单元测试。

```bash
uv run pytest
```

## 项目结构

```
extension-inkscape/
├── inx/                    # Inkscape 扩展 UI 定义
│   └── math_formula.inx
├── src/                    # 源代码
│   └── math_formula_core/
│       ├── __init__.py
│       ├── math_formula.py # 主扩展文件
│       ├── renderer.py     # 公式渲染逻辑
│       └── utils.py       # 工具函数
├── scripts/                # python环境工具
│   ├── inkscape-pythonSelect.sh
│   └── inkscape-pythonSelect-README.md
├── tests/                  # 单元测试
│   └── test_renderer.py
├── pyproject.toml         # 项目配置
└── README.md
```

## 技术说明

**此插件的核心功能（公式渲染）完全不依赖** **`inkex`**，仅依赖 `ziamath`。`inkex` 仅在插件与 Inkscape 进行交互（读取文档、插入元素）时需要。

Inkscape 1.x 已经内置了 `inkex` 库。当插件被 Inkscape 调用时，Python 解释器已经加载了 `inkex`，因此插件可以正常工作，无需在虚拟环境中安装 `inkex`。

## 贡献

欢迎提交 Issue 和 Pull Request！

***

<a id="english-version"></a>

# Inkscape Math Formula Extension

> **[中文版本](#中文版本)** | **[Chinese Version](#中文版本)**

***

## English Version

This is an extension plugin for the vector graphics software Inkscape, allowing users to insert mathematically rendered formulas into the canvas using **ziamath**.

## Features

- **Pure Python Implementation**: No LaTeX environment required (e.g., TeX Live, MiKTeX), uses Python for rendering.
- **LaTeX & MathML Support**: Use LaTeX syntax (e.g., `\frac{1}{2}`) or standard MathML.
- **SVG Vector Output**: Formulas are rendered as SVG paths, maintaining high clarity and scalability.
- **Customizable Styles**: Supports font size, color, and font selection (built-in STIX Two Math, supports other math fonts).

## Font Selection

Due to the characteristics of the `ziamath` library, the fonts used must contain a special **OpenType MATH table** to properly typeset mathematical formulas. Most regular system fonts do not have this feature.

The font selection list only includes fonts known to support the MATH table:

- **STIX Two Math**: Built into `ziamath`, no additional installation needed, recommended.
- **Cambria Math, Latin Modern Math, DejaVu Math TeX Gyre**: These are common math fonts. If your system has them installed, you can choose to use them.

**Important Note**: Inkscape extension UI (INX files) cannot dynamically fetch system font lists. Therefore, we cannot provide a complete system font dropdown like Inkscape itself. Please select a suitable font based on the above description.

## Requirements

- Inkscape 1.0+ (includes inkex library, no additional installation needed)
- Python 3.13+ (uv virtual environment will be configured automatically)
- `uv` package manager

## Quick Start

### 1. Install Dependencies and Deploy Extension

```bash
# Clone the project
git clone <repository-url>
cd extension-inkscape

# Install Python dependencies
uv sync
```

Manually copy the following two files or folders to the Inkscape extension folder to complete installation.

- inx/math\_formula.inx
- src/math\_formula\_core/ (entire directory)

Extension paths for different platforms:

| Platform                     | Path                                                           |
| ---------------------------- | -------------------------------------------------------------- |
| Linux (native)               | `~/.config/inkscape/extensions`                                |
| Linux (Flatpak recommended!) | `~/.var/app/org.inkscape.Inkscape/config/inkscape/extensions/` |
| macOS                        | `~/Library/Application Support/inkscape/extensions`            |
| Windows                      | `%APPDATA%\inkscape\extensions`                                |

To uninstall, simply remove the files and folders you copied earlier.

### 2. Configure Python Environment

**This is the most crucial step!** Inkscape uses its own Python environment, while the required libraries (`ziamath`, etc.) are installed in the uv virtual environment. You need to make Inkscape access these libraries.
Please refer to scripts/inkscape-pythonSelect.sh and its documentation inkscape-pythonSelect-README.md. Conda virtual environments are also supported.

### 3. Verify Installation

1. Open Inkscape
2. Menu bar: **Extensions > Text > Math Formula**
3. Enter `\frac{1}{2}` or `J_{xx}` in the formula input
4. Click **Apply**

If the formula renders correctly, the installation is successful!

## Uninstallation

Remove the files and folders you copied during installation.
Please restart Inkscape after uninstallation.

## Usage

1. Open Inkscape.
2. Menu bar: **Extensions > Text > Math Formula**.
3. Enter a formula in the dialog.
4. Click **Apply** to insert the formula into the canvas.

**Available Options:**

- **Font Size**: Formula text size (8-72 pt)
- **Color**: Formula color (HEX value)
- **Font**: Choose a math font (must support OpenType MATH table)
- **Insert Position**:
  - Center of currently selected object
  - Center of current canvas view
  - Geometric center of document page
  - Origin (0,0)
- **Ungroup**: Whether to automatically split formula elements after insertion

## FAQ

### Q: The extension menu doesn't appear?

1. Confirm extension files are correctly installed in the Inkscape extension directory
2. Confirm Python environment variable is correctly set
3. Restart Inkscape

### Q: Formula appears blank or shows error "No module named 'ziamath'"?

This is the most common issue. `PYTHONPATH` is not correctly set. Please refer to the "Configure Python Environment" section above.

### Q: Formula position is incorrect?

Try selecting different "Insert Position" options.

### Q: How to edit an inserted formula?

Direct editing is not currently supported. Delete the original formula and re-render.

### Q: Which LaTeX commands are supported?

Most LaTeX math commands supported by ziamath, including:

- Fractions: `\frac{a}{b}`
- Superscripts/Subscripts: `x^2`, `a_{i}`
- Square roots: `\sqrt{x}`, `\sqrt[n]{x}`
- Integrals: `\int_0^1 f(x)dx`
- Summations: `\sum_{i=0}^n`
- Matrices: `\begin{matrix}...\end{matrix}`
- And more

## Unit Tests

The project includes unit tests for formula rendering logic.

```bash
uv run pytest
```

## Project Structure

```
extension-inkscape/
├── inx/                    # Inkscape extension UI definition
│   └── math_formula.inx
├── src/                    # Source code
│   └── math_formula_core/
│       ├── __init__.py
│       ├── math_formula.py # Main extension file
│       ├── renderer.py     # Formula rendering logic
│       └── utils.py       # Utility functions
├── scripts/                # Python environment tools
│   ├── inkscape-pythonSelect.sh
│   └── inkscape-pythonSelect-README.md
├── tests/                  # Unit tests
│   └── test_renderer.py
├── pyproject.toml         # Project configuration
└── README.md
```

## Technical Notes

**The core functionality of this plugin (formula rendering) does not depend on** **`inkex`** **at all**, only on `ziamath`. `inkex` is only needed when the plugin interacts with Inkscape (reading documents, inserting elements).

Inkscape 1.x already has the `inkex` library built-in. When the plugin is invoked by Inkscape, the Python interpreter has already loaded `inkex`, so the plugin can work normally without installing `inkex` in the virtual environment.

## Contributing

Issues and Pull Requests are welcome!
