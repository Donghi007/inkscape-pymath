# Inkscape Python 解释器切换工具

[English Version](#inkscape-python-interpreter-switcher) | [English Version](#inkscape-python-interpreter-switcher-1)

## 功能特点

- **设置 Python 解释器**: 为 Inkscape 设置自定义的 Python 解释器路径
- **重置默认解释器**: 移除自定义配置，恢复 Inkscape 默认设置
- **跨平台支持**: 支持 Linux (原生/Flatpak)、macOS、Windows
- **自动备份**: 修改配置前自动创建备份
- **交互式操作**: 友好的中文交互界面

## 安装

### 方法 1: 直接下载使用

```bash
# 克隆或下载项目
git clone <repository-url>
cd path/to/inkscape-pythonSelect.sh

# 添加执行权限
chmod +x inkscape-pythonSelect.sh
```

然后执行脚本脚本
```bash
./inkscape-pythonSelect.sh
```

### 操作流程

```
1. 选择功能
   - 选项 1: 设置 Python 解释器 (默认)
   - 选项 2: 重置为默认解释器

2. 选择 Inkscape 安装类型
   - 1) Linux (原生安装)
   - 2) Linux (Flatpak)
   - 3) macOS
   - 4) Windows
   - 5) 自定义路径

3. 输入 Python 解释器路径(支持conda虚拟环境路径)
   - 可直接回车使用自动检测的路径
   - 或输入自定义路径，如:
     /home/user/.venv/bin/python
     C:\Python312\python.exe

4. 确认并应用
   - 查看配置摘要
   - 选择是否立即启动 Inkscape
```


## 实现原理

### 配置文件位置

Inkscape 将扩展设置存储在 `preferences.xml` 文件中：

| 平台 | 路径 |
|------|------|
| Linux (原生) | `~/.config/inkscape/preferences.xml` |
| Linux (Flatpak 推荐！) | `~/.var/app/org.inkscape.Inkscape/config/inkscape/preferences.xml` |
| macOS | `~/Library/Application Support/inkscape/preferences.xml` |
| Windows | `%APPDATA%\inkscape\preferences.xml` |

### Python 解释器配置

Inkscape 通过 `<group id="extensions">` 中的 `python-interpreter` 属性来确定使用的 Python：

```xml
<group
   id="extensions"
   python-interpreter="/path/to/python"
   other-settings="value" />
```
如果是faltpak版本，还可以配合使用flatseal工具来管理配置文python路径无需运行此脚本：
**步骤：**
1. **安装 Flatseal**（如尚未安装）：
   ```bash
   flatpak install flathub com.endlessm.Flatseal
   ```
2. **打开 Flatseal**在左侧选择 `Inkscape`，

3. **设置环境变量**：
   - 滚动到 **"Environment variables"** 部分
   - 点击右侧的 **+** 按钮添加新变量
   - 添加以下环境变量：

   | 变量名 | 值 |
   |--------|-----|
   | `PYTHONPATH` | `/path/to/your/project/.venv/bin/python` |

### 工作原理

1. **检测平台**: 脚本自动检测操作系统和 Inkscape 安装类型
2. **定位配置**: 根据平台确定 `preferences.xml` 文件位置
3. **备份文件**: 修改前自动创建带时间戳的备份
4. **修改配置**:
   - 如果已有 `python-interpreter` 属性 → 更新其值
   - 如果没有 → 在 `extensions` 组中添加新属性
5. **验证结果**: 修改后自动验证写入是否成功

### 备份文件

备份文件保存在配置目录中，命名格式：
```
preferences.backup_YYYYMMDD_HHMMSS.xml
```

例如: `~/.config/inkscape/preferences.backup_20250420_143000.xml`

## --Flatpak 注意事项--


Flatpak 版本的 Inkscape 运行在沙箱环境中：

| 模式 | 路径 | 说明 |
|------|------|------|
| 沙箱路径 | `~/.var/app/org.inkscape.Inkscape/config/inkscape/` | 默认沙箱隔离 |


## 故障排除

### 配置未生效

1. 确认 `preferences.xml` 文件路径正确
2. 检查 Inkscape 是否完全关闭后重启
3. 查看备份文件确认修改已写入

### 恢复默认设置

```bash
# 运行脚本选择选项 2
./scripts/inkscape-wrapper.sh
# 选择 2) Reset to default interpreter
```

### 手动恢复备份

```bash
# 停止 Inkscape
# 复制备份文件
cp ~/.config/inkscape/preferences.backup_*.xml ~/.config/inkscape/preferences.xml
# 重启 Inkscape
```

## 注意事项

**⚠️ 操作前请关闭 Inkscape！**

1. 脚本修改 `preferences.xml` 时，Inkscape 必须完全关闭
2. 建议首次使用前备份原始配置文件
3. 如果 Inkscape 启动后设置被重置，可能需要使用 wrapper 脚本代替直接启动

## 项目结构

```
extension-inkscape-intr/
├── scripts/
│   └── inkscape-wrapper.sh    # 主脚本 (唯一的文件)
└── README.md                  # 本文档
```

---

# Inkscape Python Interpreter Switcher

[中文版本](#inkscape-python-解释器切换工具) | [Chinese Version](#inkscape-python-解释器切换工具)

## Features

- **Set Python Interpreter**: Set a custom Python interpreter path for Inkscape
- **Reset to Default**: Remove custom configuration and restore Inkscape default settings
- **Cross-Platform**: Supports Linux (native/Flatpak), macOS, Windows
- **Auto Backup**: Automatically creates backup before modifying configuration
- **Interactive**: User-friendly Chinese/English interactive interface

## Installation

### Method 1: Direct Download

```bash
# Clone or download the project
git clone <repository-url>
cd path/to/inkscape-pythonSelect.sh

# Add execute permission
chmod +x inkscape-pythonSelect.sh
```
Then run:

```bash
./inkscape-pythonSelect.sh
```

### Operation Flow

```
1. Select function
   - Option 1: Set Python interpreter (default)
   - Option 2: Reset to default interpreter

2. Select Inkscape installation type
   - 1) Linux (native installation)
   - 2) Linux (Flatpak, recommended!)
   - 3) macOS
   - 4) Windows
   - 5) Custom path

3. Enter Python interpreter path (Support conda path)
   - Press Enter to use auto-detected path
   - Or enter custom path, such as:
     /home/user/.venv/bin/python
     C:\Python312\python.exe

4. Confirm and apply
   - Review configuration summary
   - Choose whether to launch Inkscape immediately
```


## Implementation Principle

### Config File Location

Inkscape stores extension settings in `preferences.xml`:

| Platform | Path |
|----------|------|
| Linux (native) | `~/.config/inkscape/preferences.xml` |
| Linux (Flatpak) | `~/.var/app/org.inkscape.Inkscape/config/inkscape/preferences.xml` |
| macOS | `~/Library/Application Support/inkscape/preferences.xml` |
| Windows | `%APPDATA%\inkscape\preferences.xml` |

### Python Interpreter Configuration

Inkscape uses the `python-interpreter` attribute in `<group id="extensions">` to determine which Python to use:

```xml
<group
   id="extensions"
   python-interpreter="/path/to/python"
   other-settings="value" />
```

### How It Works

1. **Platform Detection**: Script automatically detects OS and Inkscape installation type
2. **Locate Config**: Determines `preferences.xml` location based on platform
3. **Backup**: Creates timestamped backup before modification
4. **Modify Config**:
   - If `python-interpreter` attribute exists → Update its value
   - If not → Add new attribute to `extensions` group
5. **Verify Result**: Automatically verifies write success after modification

### Backup Files

Backups are saved in the config directory with naming format:
```
preferences.backup_YYYYMMDD_HHMMSS.xml
```

Example: `~/.config/inkscape/preferences.backup_20250420_143000.xml`

## Flatpak Notes


Flatpak version of Inkscape runs in a sandbox environment:

| Mode | Path | Description |
|------|------|-------------|
| Sandbox path | `~/.var/app/org.inkscape.Inkscape/config/inkscape/` | Default sandbox isolation |


## Troubleshooting

### Config Not Taking Effect

1. Confirm `preferences.xml` file path is correct
2. Ensure Inkscape is completely closed before restart
3. Check backup files to verify modifications were written

### Restore Default Settings

```bash
# Run script and select option 2
./scripts/inkscape-wrapper.sh
# Select 2) Reset to default interpreter
```

### Manually Restore Backup

```bash
# Stop Inkscape
# Copy backup file
cp ~/.config/inkscape/preferences.backup_*.xml ~/.config/inkscape/preferences.xml
# Restart Inkscape
```

## Important Notes

**⚠️ Before running, please CLOSE Inkscape completely!**

1. When the script modifies `preferences.xml`, Inkscape must be completely closed
2. It is recommended to backup the original config file before first use
3. If settings are reset after Inkscape starts, you may need to use the wrapper script instead of launching directly

## Project Structure

```
extension-inkscape-intr/
├── scripts/
│   └── inkscape-wrapper.sh    # Main script (the only file needed)
└── README.md                  # This document
```

---

## License

MIT License
