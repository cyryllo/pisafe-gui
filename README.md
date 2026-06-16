# PiSafe GUI 🫐

A graphical interface (PyQt5) for the [pisafe](https://github.com/RichardMidnight/pi-safe) tool — an easy way to flash system images onto SD/USB drives and create backups of them, without using the terminal.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Raspberry%20Pi%20OS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

---

## 📸 Preview

![PiSafe GUI interface](https://github.com/cyryllo/pisafe-gui/raw/main/doc/screenshot.png)

---

## ✨ Features

- **⚡ Flash image → SD/USB** — pick an image file (`.img`, `.zip`, `.xz`, `.gz`, `.zst`) and a target drive, flash it in one click
- **💾 Backup SD/USB → image** — create backups of SD cards with your choice of compression format
- **🛡️ System disk protection** — the app automatically detects and **hides** disks where the system is mounted (`/`, `/boot`, `/home`, etc.), so there's no risk of accidentally overwriting your own system
- **📋 Disk list** — full overview of connected block devices (`lsblk`)
- **📜 Real-time logs** — full command output visible inside the app
- **🎨 Dark theme** — interface styled after Catppuccin Mocha

---

## 🖥️ Requirements

- Linux / Raspberry Pi OS
- Python 3.7+
- [PyQt5](https://pypi.org/project/PyQt5/)
- [pisafe](https://github.com/RichardMidnight/pi-safe) (the underlying tool, installed automatically by `install.sh`)

---

## 🚀 Installation

```bash
git clone https://github.com/cyryllo/pisafe-gui.git
cd pisafe-gui
bash install.sh
```

The `install.sh` script:

1. Installs `python3-pyqt5` and `pv`
2. Installs the `pisafe` tool if it's not already present on the system
3. Creates an application shortcut in the system menu

---

## ▶️ Running the app

From the system menu: System > PiSafe GUI

From the terminal:

```bash
python3 pisafe_gui.py
```

> Flash/backup operations require `sudo` privileges, since `pisafe` operates directly on block devices. The app will prompt for a password when running the command.

---

## 📁 Project structure

```
pisafe-gui/
├── pisafe_gui.py          # Main PyQt5 application
├── requirements.txt       # Python dependencies
├── install.sh             # Installation script
└── README.md
```

---

## ⚠️ Known limitations

- The progress bar doesn't show a real-time percentage — this depends on whether `pisafe`/`dd` outputs progress data to stdout. Currently the bar jumps from 0% to 100% once the operation finishes.

---

## 🗺️ Planned features (TODO)

- [ ] Real progress bar (e.g. via `pv` or by monitoring output file size)
- [ ] Image checksum verification (MD5/SHA256)
- [ ] History of recent operations
- [ ] System notification when a task finishes
- [ ] Support for multiple disks at once
- [ ] CLI mode (no GUI)

---

## 🤝 Contributing

Pull requests and issues are welcome! If you find a bug or have a feature idea, please open an issue in this repository.

---

## 📄 License

This project is available under the [MIT](https://github.com/cyryllo/pisafe-gui/blob/main/LICENSE) license.

Built on top of [pisafe](https://github.com/RichardMidnight/pi-safe) by RichardMidnight.

---

## 🙏 Acknowledgments

- [RichardMidnight](https://github.com/RichardMidnight) — for creating the `pisafe` tool
- [Catppuccin](https://github.com/catppuccin/catppuccin) — for the theme's color palette
