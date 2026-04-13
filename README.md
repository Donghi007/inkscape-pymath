# Inkscape 数学公式扩展 (Math Formula Extension)

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

### 4. 配置 Python 环境（让 Inkscape 访问 uv 虚拟环境中的依赖）

Inkscape 使用自带的 Python 环境，而扩展所需的库（`ziamath` 等）安装在 uv 虚拟环境中。需要让 Inkscape 能访问这些库。

#### 方法 A：设置 PYTHONPATH（推荐）

在启动 Inkscape 前设置 `PYTHONPATH` 环境变量：

```bash
# 获取 uv 虚拟环境的 site-packages 路径
SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])")
echo $SITE_PACKAGES

# 临时方式：启动 Inkscape 前在终端执行
export PYTHONPATH="$SITE_PACKAGES:$PYTHONPATH"
inkscape

# 永久方式：添加到 ~/.bashrc 或 ~/.zshrc
echo 'export PYTHONPATH="$HOME/.cache/uv/sdists-v9/*/python3.13/site-packages:$PYTHONPATH"' >> ~/.bashrc
```

**注意**：uv 虚拟环境的路径可能在每次 `uv sync` 后变化。如果路径变化，需要更新 `PYTHONPATH`。

#### 方法 B：创建 Inkscape 启动脚本

创建一个便捷脚本来自动设置环境变量：

```bash
# 创建 ~/.local/bin/inkscape-mathext
mkdir -p ~/.local/bin
cat > ~/.local/bin/inkscape-mathext << 'EOF'
#!/bin/bash
SITE_PACKAGES=$(cd /home/donghi/Desktop/python/extension/extension-inkscape && uv run python -c "import site; print(site.getsitepackages()[0])")
export PYTHONPATH="$SITE_PACKAGES:$PYTHONPATH"
exec inkscape "$@"
EOF

chmod +x ~/.local/bin/inkscape-mathext
```

之后使用 `inkscape-mathext` 命令启动 Inkscape 即可。

#### 方法 C：使用符号链接（适用于 Flatpak）

对于 Flatpak 安装，可以将依赖库复制到 Inkscape 可访问的位置：

```bash
# Flatpak 方式：复制到用户配置目录
mkdir -p ~/.config/inkscape/extensions

# 复制扩展文件
cp inx/math_formula.inx ~/.config/inkscape/extensions/
cp -r src/math_formula_core ~/.config/inkscape/extensions/

# 复制依赖库
UV_SITE=$(uv run python -c "import site; print(site.getsitepackages()[0])")
mkdir -p ~/.config/inkscape/extensions/lib
for pkg in ziamath ziafont latex2mathml lxml; do
    cp -r $UV_SITE/$pkg ~/.config/inkscape/extensions/lib/ 2>/dev/null || true
done
```

然后在扩展目录创建 `startup.py` 文件，设置 `sys.path`：
```python
# ~/.config/inkscape/extensions/startup.py
import sys
import os
lib_dir = os.path.join(os.path.dirname(__file__), 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)
```

#### 方法 D：使用 Flatseal 设置环境变量（适用于 Flatpak）

[Flatseal](https://flathub.org/apps/com.endlessm.Flatseal) 是一个图形化工具，用于管理 Flatpak 应用的权限和环境变量。

**步骤：**

1. **安装 Flatseal**（如尚未安装）：
   ```bash
   flatpak install flathub com.endlessm.Flatseal
   ```

2. **打开 Flatseal**，在左侧选择 `org.inkscape.Inkscape`

3. **设置环境变量**：
   - 滚动到 **"Environment variables"** 部分
   - 点击右侧的 **+** 按钮添加新变量
   - 添加以下环境变量：

   | 变量名 | 值 |
   |--------|-----|
   | `PYTHONPATH` | `/home/donghi/Desktop/python/extension/extension-inkscape/.venv/lib/python3.13/site-packages` |

4. **点击右下角 "Restart"** 按钮重启 Inkscape

5. **安装扩展文件**（如果尚未安装）：
   ```bash
   mkdir -p ~/.config/inkscape/extensions
   cp inx/math_formula.inx ~/.config/inkscape/extensions/
   cp -r src/math_formula_core ~/.config/inkscape/extensions/
   ```

**注意**：如果项目路径或 uv 环境发生变化，需要在 Flatseal 中更新 `PYTHONPATH` 的值。

### 5. 卸载
如需卸载插件，运行卸载脚本：
```bash
chmod +x scripts/uninstall.sh
./scripts/uninstall.sh
```

### 6. 重要说明
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
