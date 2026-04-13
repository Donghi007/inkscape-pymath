# Inkscape 数学公式扩展 (Math Formula Extension)

这是一个为矢量图形软件 Inkscape 开发的扩展插件，允许用户在画布中插入由 **ziamath** 渲染的数学公式。

## 核心特性
- **纯 Python 实现**: 不依赖 LaTeX 环境 (如 TeX Live, MiKTeX)，完全使用 Python 渲染。
- **支持 LaTeX & MathML**: 使用 LaTeX 语法 (例如 `\frac{1}{2}`) 或标准的 MathML。
- **SVG 矢量输出**: 公式渲染为 SVG 路径，保持高清晰度且可缩放。
- **样式自定义**: 支持设置字号、颜色和字体 (内置 STIX Two Math)。

## 环境要求
- Inkscape 1.0+ (自带 inkex 库，无需额外安装)
- Python 3.12+
- `uv` 包管理工具 (推荐)

## 安装方法

### 1. 安装系统依赖 (可选，仅本地开发测试需要)
如果需要在本地 Python 环境中运行测试（不通过 Inkscape），需要安装 GTK 开发库：
```bash
# Ubuntu/Debian
sudo apt install libgirepository1.0-dev libcairo2-dev gir1.2-gtk-3.0

# Fedora
sudo dnf install gobject-introspection cairo-gobject-devel
```

### 2. 克隆并安装依赖
```bash
git clone https://github.com/your-repo/inkscape-math-formula.git
cd inkscape-math-formula
uv sync
```

如需在本地开发环境中包含 `inkex`（用于完整测试），可选择安装：
```bash
uv sync --all-extras
```

### 3. 部署到 Inkscape
运行安装脚本，将插件链接到 Inkscape 的扩展目录：
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

安装脚本会自动检测并适配以下平台：
- **Linux**: 原生安装 (`~/.config/inkscape/extensions/`)
- **Linux Flatpak**: Flatpak 安装 (`~/.var/app/org.inkscape.Inkscape/config/inkscape/extensions/`)
- **Linux Snap**: Snap 安装 (`~/snap/inkscape/current/.config/inkscape/extensions/`)
- **Windows**: (`%LOCALAPPDATA%` 或 `%APPDATA%\inkscape\extensions\`)
- **macOS**: (`~/Library/Application Support/inkscape/extensions/` 或 `~/.config/inkscape/extensions/`)

### 4. 卸载
如需卸载插件，运行卸载脚本：
```bash
chmod +x scripts/uninstall.sh
./scripts/uninstall.sh
```

### 5. 重要说明
**此插件的核心功能（公式渲染）完全不依赖 `inkex`**，仅依赖 `ziamath`。`inkex` 仅在插件与 Inkscape 进行交互（读取文档、插入元素）时需要。

Inkscape 1.x 已经内置了 `inkex` 库。当插件被 Inkscape 调用时，Python 解释器已经加载了 `inkex`，因此插件可以正常工作，无需在虚拟环境中安装 `inkex`。

## 使用说明
1. 打开 Inkscape。
2. 菜单栏点击: **扩展 > 文本 > 数学公式 (Math Formula)**。
3. 在弹出的对话框中输入公式。
4. 点击 **应用** 即可将公式插入画布。

## 单元测试
项目包含针对公式渲染逻辑的单元测试。
```bash
uv run pytest
```

## 贡献
欢迎提交 Issue 和 Pull Request！
