#!/bin/bash

echo ""
echo "================================================"
echo "  Inkscape Python Interpreter Switcher Wrapper"
echo "================================================"
echo ""
echo "IMPORTANT: Please CLOSE Inkscape before running!"
echo ""
echo "================================================"
echo ""

detect_preferences_file() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if [[ -f "$HOME/Library/Application Support/inkscape/preferences.xml" ]]; then
            echo "$HOME/Library/Application Support/inkscape/preferences.xml"
        else
            echo "$HOME/.config/inkscape/preferences.xml"
        fi
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
        if [[ -n "$APPDATA" && -f "$APPDATA/inkscape/preferences.xml" ]]; then
            echo "$APPDATA/inkscape/preferences.xml"
        elif [[ -n "$LOCALAPPDATA" && -f "$LOCALAPPDATA/inkscape/preferences.xml" ]]; then
            echo "$LOCALAPPDATA/inkscape/preferences.xml"
        else
            echo "$APPDATA/inkscape/preferences.xml"
        fi
    else
        if [[ -f "$HOME/.config/inkscape/preferences.xml" ]]; then
            echo "$HOME/.config/inkscape/preferences.xml"
        elif [[ -f "$HOME/.var/app/org.inkscape.Inkscape/config/inkscape/preferences.xml" ]]; then
            echo "$HOME/.var/app/org.inkscape.Inkscape/config/inkscape/preferences.xml"
        else
            echo "$HOME/.config/inkscape/preferences.xml"
        fi
    fi
}

echo "Main Menu"
echo "---------"
echo ""
echo "Please select an option:"
echo ""
echo "  1) Set Python interpreter (default)"
echo "  2) Reset to default interpreter (remove python-interpreter)"
echo ""
echo "Please enter your choice [1]: "

read -r main_choice
main_choice="${main_choice:-1}"

if [[ "$main_choice" == "2" ]]; then
    echo ""
    echo "Step 1: Select Inkscape Installation Type (for reset)"
    echo "----------------------------------------------------"
    echo ""
    echo "Please select your Inkscape installation:"
    echo ""
    echo "  1) Linux (native)"
    echo "  2) Linux (Flatpak)"
    echo "  3) macOS"
    echo "  4) Windows"
    echo "  5) Custom path"
    echo ""
    echo "Please enter your choice [1]: "
    
    read -r choice
    choice="${choice:-1}"
    
    case "$choice" in
        1)
            PREFERENCES_FILE="$HOME/.config/inkscape/preferences.xml"
            echo ""
            echo ">>> Using Linux native path"
            ;;
        2)
            echo ""
            echo "Flatpak: Do you want to use host filesystem or sandbox path?"
            echo ""
            echo "  1) Host filesystem - ~/.config/inkscape/ (recommended)"
            echo "  2) Sandboxed - ~/.var/app/org.inkscape.Inkscape/config/inkscape/"
            echo ""
            echo "Please enter your choice [1]: "
            read -r flatpak_choice
            flatpak_choice="${flatpak_choice:-1}"
            
            if [[ "$flatpak_choice" == "2" ]]; then
                PREFERENCES_FILE="$HOME/.var/app/org.inkscape.Inkscape/config/inkscape/preferences.xml"
            else
                PREFERENCES_FILE="$HOME/.config/inkscape/preferences.xml"
            fi
            echo ""
            echo ">>> Using Linux Flatpak path"
            ;;
        3)
            PREFERENCES_FILE="$HOME/Library/Application Support/inkscape/preferences.xml"
            echo ""
            echo ">>> Using macOS path"
            ;;
        4)
            if [[ -n "$LOCALAPPDATA" ]]; then
                PREFERENCES_FILE="$LOCALAPPDATA/inkscape/preferences.xml"
            else
                PREFERENCES_FILE="$APPDATA/inkscape/preferences.xml"
            fi
            echo ""
            echo ">>> Using Windows path"
            ;;
        5)
            echo ""
            echo "Please enter the full path to your Inkscape preferences.xml file:"
            read -r PREFERENCES_FILE
            echo ""
            echo ">>> Using custom path: $PREFERENCES_FILE"
            ;;
        *)
            PREFERENCES_FILE="$HOME/.config/inkscape/preferences.xml"
            echo ""
            echo ">>> Using default Linux path"
            ;;
    esac
    
    PREFERENCES_FILE="${PREFERENCES_FILE/#\~/$HOME}"
    
    echo ""
    echo "================================================"
    echo "  Resetting to Default Interpreter"
    echo "================================================"
    echo ""
    
    if [[ -f "$PREFERENCES_FILE" ]]; then
        BACKUP_FILE="${PREFERENCES_FILE%.xml}.backup_$(date +%Y%m%d_%H%M%S).xml"
        cp "$PREFERENCES_FILE" "$BACKUP_FILE"
        echo "[OK] Backup created: $BACKUP_FILE"
        
        if grep -q 'python-interpreter=' "$PREFERENCES_FILE"; then
            sed -i 's| python-interpreter="[^"]*"||g' "$PREFERENCES_FILE"
            sed -i 's| python-interpreter='\''[^'\'']*'\''||g' "$PREFERENCES_FILE"
            echo "[OK] Removed python-interpreter from preferences.xml"
        else
            echo "[OK] No python-interpreter found in preferences.xml"
        fi
        
        echo ""
        echo "================================================"
        echo "  Reset Complete!"
        echo "================================================"
        echo ""
        echo "Preferences file: $PREFERENCES_FILE"
        echo ""
        echo "Inkscape will now use its default Python interpreter."
        echo "Please restart Inkscape for changes to take effect."
    else
        echo "[OK] Preferences file does not exist."
        echo "    Nothing to reset."
        echo ""
        echo "Preferences file: $PREFERENCES_FILE"
    fi
    exit 0
fi

echo "Step 1: Select Inkscape Installation Type"
echo "----------------------------------------"
echo ""
echo "Please select your Inkscape installation:"
echo ""
echo "  1) Linux (native)"
echo "  2) Linux (Flatpak)"
echo "  3) macOS"
echo "  4) Windows"
echo "  5) Custom path"
echo ""
echo "Please enter your choice [1]: "

read -r choice
choice="${choice:-1}"

case "$choice" in
    1)
        PREFERENCES_FILE="$HOME/.config/inkscape/preferences.xml"
        echo ""
        echo ">>> Using Linux native path"
        ;;
    2)
        echo ""
        echo "Flatpak: Do you want to use host filesystem or sandbox path?"
        echo ""
        echo "  1) Host filesystem - ~/.config/inkscape/"
        echo "  2) Sandboxed - ~/.var/app/org.inkscape.Inkscape/config/inkscape/ (recommended!)"
        echo ""
        echo "Please enter your choice [1]: "
        read -r flatpak_choice
        flatpak_choice="${flatpak_choice:-1}"
        
        if [[ "$flatpak_choice" == "2" ]]; then
            PREFERENCES_FILE="$HOME/.var/app/org.inkscape.Inkscape/config/inkscape/preferences.xml"
        else
            PREFERENCES_FILE="$HOME/.config/inkscape/preferences.xml"
        fi
        echo ""
        echo ">>> Using Linux Flatpak path"
        ;;
    3)
        PREFERENCES_FILE="$HOME/Library/Application Support/inkscape/preferences.xml"
        echo ""
        echo ">>> Using macOS path"
        ;;
    4)
        if [[ -n "$LOCALAPPDATA" ]]; then
            PREFERENCES_FILE="$LOCALAPPDATA/inkscape/preferences.xml"
        else
            PREFERENCES_FILE="$APPDATA/inkscape/preferences.xml"
        fi
        echo ""
        echo ">>> Using Windows path"
        ;;
    5)
        echo ""
        echo "Please enter the full path to your Inkscape preferences.xml file:"
        echo "(e.g., ~/.config/inkscape/preferences.xml)"
        echo ""
        read -r PREFERENCES_FILE
        echo ""
        echo ">>> Using custom path: $PREFERENCES_FILE"
        ;;
    *)
        PREFERENCES_FILE="$HOME/.config/inkscape/preferences.xml"
        echo ""
        echo ">>> Using default Linux path"
        ;;
    esac

echo ""
echo "Step 2: Set Python Interpreter Path"
echo "------------------------------------"
echo ""
echo "Please enter the full path to your Python interpreter:"
echo ""
echo "Examples(Support conda path):"
echo "  - /usr/bin/python3"
echo "  - /home/user/.venv/bin/python"
echo "  - C:\\Python312\\python.exe"
echo ""
echo "Or press Enter to use the auto-detected path:"
echo ""

DEFAULT_PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null || echo "")
if [[ -n "$DEFAULT_PYTHON" ]]; then
    echo "Detected: $DEFAULT_PYTHON"
fi

echo ""
read -r PYTHON_PATH

if [[ -z "$PYTHON_PATH" ]]; then
    if [[ -n "$DEFAULT_PYTHON" ]]; then
        PYTHON_PATH="$DEFAULT_PYTHON"
    else
        echo ""
        echo "ERROR: No Python interpreter specified and none detected."
        echo "Please enter a valid Python path."
        exit 1
    fi
fi

PYTHON_PATH="${PYTHON_PATH/#\~/$HOME}"

echo ""
echo "Step 3: Summary"
echo "---------------"
echo ""
echo "Python interpreter: $PYTHON_PATH"
echo "Preferences file:   $PREFERENCES_FILE"
echo ""

if [[ ! -f "$PREFERENCES_FILE" ]]; then
    echo "WARNING: Preferences file does not exist."
    echo "It will be created when Inkscape runs for the first time."
    echo ""
fi

echo "Step 4: Launch Inkscape"
echo "----------------------"
echo ""
echo "Do you want to launch Inkscape after applying settings?"
echo ""
echo "  1) No (default)"
echo "  2) Yes"
echo ""
echo "Please enter your choice [1]: "

read -r launch_choice
launch_choice="${launch_choice:-1}"

echo ""
echo "================================================"
echo "  Applying Settings"
echo "================================================"
echo ""

PREFERENCES_FILE="${PREFERENCES_FILE/#\~/$HOME}"
PYTHON_PATH="${PYTHON_PATH/#\~/$HOME}"

if [[ -f "$PREFERENCES_FILE" ]]; then
    BACKUP_FILE="${PREFERENCES_FILE%.xml}.backup_$(date +%Y%m%d_%H%M%S).xml"
    cp "$PREFERENCES_FILE" "$BACKUP_FILE"
    echo "[OK] Backup created: $BACKUP_FILE"
    
    python3 -c "
import re

prefs_file = '$PREFERENCES_FILE'
python_path = '$PYTHON_PATH'

with open(prefs_file, 'r', encoding='utf-8') as f:
    content = f.read()

if 'python-interpreter=' in content:
    content = re.sub(
        r'python-interpreter=\"[^\"]*\"',
        f'python-interpreter=\"{python_path}\"',
        content
    )
    print('[OK] Updated python-interpreter in preferences.xml')
else:
    content = re.sub(
        r'(<group[^>]*\n\s+id=\"extensions\")',
        r'\1\n     python-interpreter=\"' + python_path + '\"',
        content
    )
    print('[OK] Added python-interpreter to preferences.xml')

with open(prefs_file, 'w', encoding='utf-8') as f:
    f.write(content)

with open(prefs_file, 'r', encoding='utf-8') as f:
    if 'python-interpreter=' in f.read():
        print('[OK] Verification: python-interpreter found in file')
    else:
        print('[ERROR] Verification failed: python-interpreter not found!')
"

else
    PARENT_DIR=$(dirname "$PREFERENCES_FILE")
    mkdir -p "$PARENT_DIR"
    
    cat > "$PREFERENCES_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<inkscape xmlns="http://www.inkscape.org/namespaces/inkscape" xmlns:xlink="http://www.w3.org/1999/xlink">
  <group id="extensions" python-interpreter="$PYTHON_PATH" />
</inkscape>
EOF
    echo "[OK] Created new preferences.xml with python-interpreter"
fi

echo ""
echo "================================================"
echo "  Configuration Complete!"
echo "================================================"
echo ""
echo "Preferences file: $PREFERENCES_FILE"
echo ""

if [[ "$launch_choice" == "2" ]]; then
    echo "Starting Inkscape..."
    echo ""
    
    if [[ "$choice" == "2" ]] && command -v flatpak &> /dev/null; then
        flatpak run org.inkscape.Inkscape "$@"
    elif command -v flatpak &> /dev/null && flatpak info org.inkscape.Inkscape &> /dev/null 2>&1; then
        flatpak run org.inkscape.Inkscape "$@"
    elif command -v inkscape &> /dev/null; then
        inkscape "$@"
    else
        echo "ERROR: Inkscape not found!"
        echo "Please install Inkscape or specify the Inkscape path."
        exit 1
    fi
else
    echo "Settings applied. You can start Inkscape manually later."
    echo ""
    echo "To start Inkscape, run:"
    echo "  inkscape"
    echo "or"
    echo "  flatpak run org.inkscape.Inkscape"
fi
