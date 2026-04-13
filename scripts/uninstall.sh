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

echo "=== Inkscape Math Formula 卸载脚本 ==="
echo ""

EXT_DIR_INFO="$(get_extensions_dir)"
EXT_DIR="${EXT_DIR_INFO%%|*}"
INSTALL_MODE="${EXT_DIR_INFO##*|}"

if [[ -z "$EXT_DIR" ]]; then
    echo "错误: 无法检测 Inkscape 扩展目录。"
    exit 1
fi

echo "检测到安装模式: $INSTALL_MODE"
echo "扩展目录: $EXT_DIR"
echo ""

if [[ "$INSTALL_MODE" == "Flatpak" ]]; then
    echo "提示: 对于 Flatpak 安装的 Inkscape，扩展可能安装在用户配置目录："
    echo "  ~/.config/inkscape/extensions/"
    echo ""
fi

if [[ ! -d "$EXT_DIR" ]]; then
    echo "扩展目录不存在，插件可能未安装。"
    exit 0
fi

remove_file() {
    local file="$1"
    if [[ -L "$file" || -f "$file" ]]; then
        rm -f "$file"
        echo "  ✓ 已删除: $(basename "$file")"
    fi
}

echo "正在卸载扩展文件..."

remove_file "$EXT_DIR/${EXTENSION_NAME}.inx"
remove_file "$EXT_DIR/${EXTENSION_NAME}_core"

echo ""
echo "卸载完成！"
echo ""
echo "请重启 Inkscape 以使更改生效。"
