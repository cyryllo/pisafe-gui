# PiSafe GUI 🫐

A graphical interface (PyQt5) for the [pisafe](https://github.com/RichardMidnight/pi-safe) tool — an easy way to flash system images onto SD/USB drives and create backups of them, without using the terminal.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Raspberry%20Pi%20OS-lightgrey.svg)
![License](https://img.shields.io/badge/license-GPLv3-yellow.svg)

---

## 📸 Preview

![PiSafe GUI interface](https://github.com/cyryllo/pisafe-gui/raw/main/doc/screenshot.png)

---

## ✨ Features

- **⚡ Flash image → SD/USB** — pick an image file (`.img`, `.zip`, `.xz`, `.gz`, `.zst`) and a target drive, flash it in one click
- **💾 Backup SD/USB → image** — create backups of SD cards with your choice of compression format
- **🗂️ Image version management** — group backups into named projects with their own base folder, tag each one with a free-text version label (v1, v2, "stable", ...), and browse/delete them in a dedicated tab (SQLite-backed)
- **✅ Checksum verification** — optionally verify a flash by comparing the SHA256 of the source `.img`/`.iso` against what was actually written to the disk, reported automatically as a match/mismatch
- **🔎 Downloaded image check** — check a downloaded image's integrity before flashing it: auto-detects a `.sha256`/`.sha256sum`/`.md5` file next to it, or lets you paste the expected checksum from the download page
- **📀 Flash to multiple disks at once** — add up to 8 target disks with `+`/`-` and flash the same image to all of them in parallel, with a per-disk progress row and a final success/failure summary
- **🔧 Disk tools** — inspect any disk except optical drives (detected OS, partition layout, free space); quick-format (FAT32/exFAT/NTFS/ext4) is only enabled for USB/SD disks, same protection as flashing
- **🛡️ System disk protection** — the app automatically detects and **hides** disks where the system is mounted (`/`, `/boot`, `/home`, etc.), so there's no risk of accidentally overwriting your own system
- **📋 Disk list** — full overview of connected block devices (`lsblk`)
- **📜 Real-time logs** — full command output visible inside the app
- **🎨 Dark theme** — interface styled after Catppuccin Mocha

---

## 🌐 Languages

The interface is available in:

- 🇬🇧 English (default)
- 🇵🇱 Polski
- 🇪🇸 Español

Switch language from the dropdown in the app's header — the app restarts to apply the change. Translations live in [`translations.py`](translations.py) as plain key → text dictionaries, so adding a new language doesn't require touching any UI code. Want to add yours? See [Contributing](#-contributing) below.

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

From the application menu: Accessories/Utilities > PiSafe GUI

From the terminal:

```bash
python3 pisafe_gui.py
```

> Flash/backup operations require administrator privileges, since `pisafe` operates directly on block devices. The app runs them via `pkexec` (PolicyKit), which shows a native graphical password prompt — no terminal needed. `pkexec` is installed automatically by `install.sh` (package `policykit-1`).

---

## 📁 Project structure

```
pisafe-gui/
├── pisafe_gui.py          # Main PyQt5 application
├── translations.py        # i18n strings and language persistence
├── db.py                  # SQLite storage for image version management
├── requirements.txt       # Python dependencies
├── install.sh             # Installation script
└── README.md
```

---

## 🗺️ Planned features (TODO)

- [ ] Debian (`.deb`) package

---

## 🤝 Contributing

Pull requests and issues are welcome! If you find a bug or have a feature idea, please open an issue in this repository.

**Adding a translation:** open [`translations.py`](translations.py), add your language code and name to `LANGUAGES`, then copy the `"en"` dictionary under a new key and translate the values (keep the `{placeholders}` as they are). That's it — no other code changes needed. PRs for new languages are very welcome!

---

## 📄 License

This project is available under the [GNU GPLv3](https://github.com/cyryllo/pisafe-gui/blob/main/LICENSE) license.

Built on top of [pisafe](https://github.com/RichardMidnight/pi-safe) by RichardMidnight (also GPLv3).

---

## 🙏 Acknowledgments

- [RichardMidnight](https://github.com/RichardMidnight) — for creating the `pisafe` tool
- [Catppuccin](https://github.com/catppuccin/catppuccin) — for the theme's color palette
