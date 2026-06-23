#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/share/pisafe-gui"
NEW_VERSION="$(cat "$SCRIPT_DIR/VERSION" 2>/dev/null || echo "?")"

if [ -f "$INSTALL_DIR/VERSION" ]; then
    CURRENT_VERSION="$(cat "$INSTALL_DIR/VERSION")"
    if [ "$CURRENT_VERSION" = "$NEW_VERSION" ]; then
        echo "==> PiSafe GUI w wersji $CURRENT_VERSION jest już zainstalowane."
        read -r -p "Zainstalować ponownie? [t/N] " ODP
        case "$ODP" in
            [tTyY]*) ;;
            *) echo "Instalacja przerwana."; exit 0 ;;
        esac
    else
        echo "==> Wykryto zainstalowaną wersję: $CURRENT_VERSION"
        echo "==> Dostępna wersja: $NEW_VERSION"
        read -r -p "Zainstalować/zaktualizować? [T/n] " ODP
        case "$ODP" in
            [nN]*) echo "Instalacja przerwana."; exit 0 ;;
            *) ;;
        esac
    fi
else
    echo "==> Instalacja PiSafe GUI $NEW_VERSION"
fi

echo "==> Instalacja zależności systemowych..."
sudo apt-get update -q
sudo apt-get install -y python3-pyqt5 pv

echo "==> Instalacja PolicyKit (pkexec)..."
if ! sudo apt-get install -y polkitd pkexec; then
    # starsze systemy (Debian <12 / Ubuntu <23.04) mają to w jednym pakiecie
    sudo apt-get install -y policykit-1
fi

echo "==> Sprawdzanie pisafe..."
if ! command -v pisafe &> /dev/null; then
    echo "==> Pobieranie i instalacja pisafe..."
    wget -q https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O "$SCRIPT_DIR/pisafe"
    bash "$SCRIPT_DIR/pisafe" install
else
    echo "==> pisafe już zainstalowane."
fi

mkdir -p "$INSTALL_DIR"
cp "$SCRIPT_DIR/pisafe_gui.py" "$SCRIPT_DIR/translations.py" "$SCRIPT_DIR/VERSION" "$SCRIPT_DIR/icon.png" "$INSTALL_DIR/"
mkdir -p "$HOME/.local/share/applications"
cat > "$HOME/.local/share/applications/pisafe-gui.desktop" << DESKTOP
[Desktop Entry]
Name=PiSafe GUI
Comment=Graficzny interfejs dla narzędzia pisafe
Exec=python3 $INSTALL_DIR/pisafe_gui.py
Icon=$INSTALL_DIR/icon.png
Terminal=false
Type=Application
Categories=Utility;System;
DESKTOP

echo ""
echo "✅ Gotowe! Zainstalowano PiSafe GUI $NEW_VERSION."
echo "   Znajdziesz ją w menu aplikacji (System > PiSafe GUI) — sprawdź tam."
echo "   Można ją też uruchomić z terminala: python3 $INSTALL_DIR/pisafe_gui.py"
