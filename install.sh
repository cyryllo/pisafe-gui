#!/bin/bash
set -e
echo "==> Instalacja zależności systemowych..."
sudo apt-get update -q
sudo apt-get install -y python3-pyqt5 pv

echo "==> Sprawdzanie pisafe..."
if ! command -v pisafe &> /dev/null; then
    echo "==> Pobieranie i instalacja pisafe..."
    wget -q https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O /tmp/pisafe
    bash /tmp/pisafe install
else
    echo "==> pisafe już zainstalowane."
fi

INSTALL_DIR="$HOME/.local/share/pisafe-gui"
mkdir -p "$INSTALL_DIR"
cp pisafe_gui.py translations.py "$INSTALL_DIR/"
mkdir -p "$HOME/.local/share/applications"
cat > "$HOME/.local/share/applications/pisafe-gui.desktop" << DESKTOP
[Desktop Entry]
Name=PiSafe GUI
Comment=Graficzny interfejs dla narzędzia pisafe
Exec=python3 $INSTALL_DIR/pisafe_gui.py
Icon=media-flash
Terminal=false
Type=Application
Categories=Utility;System;
DESKTOP

echo ""
echo "✅ Gotowe! Uruchom: python3 pisafe_gui.py"
