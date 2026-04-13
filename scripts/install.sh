#!/bin/bash

set -e

EXTENSION_NAME="math_formula"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

get_extensions_dir() {
    local dir=""
    local install_mode=""

    if [[ "$OSTYPE" == "darwin"* ]]; then
        if [[ -d "$HOME/Library/Application Support/inkscape/extensions" ]]; then
            dir="$HOME/Library/Application Support/inkscape/extensions"
            install_mode="macOS"
        else
            dir="$HOME/.config/inkscape/extensions"
            install_mode="macOS (XDG)"
        fi
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        if [[ -n "$LOCALAPPDATA" ]]; then
            dir="$LOCALAPPDATA/inkscape/extensions"
        elif [[ -n "$APPDATA" ]]; then
            dir="$APPDATA/inkscape/extensions"
        fi
        install_mode="Windows"
    else
        if [[ -f "/usr/bin/flatpak" ]] && flatpak info org.inkscape.Inkscape &>/dev/null; then
            dir="$HOME/.var/app/org.inkscape.Inkscape/config/inkscape/extensions"
            install_mode="Flatpak"
        elif [[ -d "/snap/inkscape/current" ]]; then
            dir="$HOME/snap/inkscape/current/.config/inkscape/extensions"
            install_mode="Snap"
        else
            dir="$HOME/.config/inkscape/extensions"
            install_mode="Linux"
        fi
    fi

    echo "$dir|$install_mode"
}

echo "=== Inkscape Math Formula 安装脚本 ==="
echo ""

EXT_DIR_INFO="$(get_extensions_dir)"
EXT_DIR="${EXT_DIR_INFO%%|*}"
INSTALL_MODE="${EXT_DIR_INFO##*|}"

if [[ -z "$EXT_DIR" ]]; then
    echo "错误: 无法检测 Inkscape 扩展目录。请手动设置 INKSCAPE_EXT_DIR 环境变量。"
    exit 1
fi

echo "检测到安装模式: $INSTALL_MODE"
echo "扩展目录: $EXT_DIR"

if [[ "$INSTALL_MODE" == "Flatpak" ]]; then
    if [[ ! -w "$EXT_DIR" ]]; then
        echo ""
        echo "警告: Flatpak 扩展目录是只读的。"
        echo ""
        echo "Flatpak 安装的 Inkscape 需要通过以下方式安装扩展："
        echo ""
        echo "方法 1: 使用 flatpak override 命令授予扩展目录写入权限"
        echo "  flatpak override --user --filesystem=xdg-config/inkscape org.inkscape.Inkscape"
        echo ""
        echo "方法 2: 将扩展复制到用户配置目录（推荐）"
        echo "  mkdir -p ~/.config/inkscape/extensions"
        echo "  cp inx/math_formula.inx ~/.config/inkscape/extensions/"
        echo "  cp -r src/math_formula ~/.config/inkscape/extensions/"
        echo ""
        echo "方法 3: 重新安装 Inkscape 为非 Flatpak 版本"
        exit 1
    fi
fi

mkdir -p "$EXT_DIR"

echo ""
echo "正在安装扩展文件..."

ln -sf "$PROJECT_ROOT/inx/${EXTENSION_NAME}.inx" "$EXT_DIR/${EXTENSION_NAME}.inx"
ln -sf "$PROJECT_ROOT/src/${EXTENSION_NAME}" "$EXT_DIR/${EXTENSION_NAME}"

echo "  ✓ ${EXTENSION_NAME}.inx"
echo "  ✓ ${EXTENSION_NAME}/"

echo ""
echo "安装完成！"
echo ""
echo "请重启 Inkscape，然后前往: 扩展 > 文本 > 数学公式"
