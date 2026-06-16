#!/usr/bin/env python3
"""
PiSafe GUI – graficzny interfejs dla narzędzia pisafe
Wymagania: pip install PyQt5
Wymagane narzędzie: pisafe (zainstalowane w /usr/local/bin/pisafe)
"""

import sys
import os
import subprocess
import json
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QFileDialog, QTextEdit,
    QTabWidget, QLineEdit, QMessageBox, QProgressBar, QFrame,
    QGroupBox, QSizePolicy
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QTextCursor

DARK_STYLE = """
QMainWindow, QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}
QTabWidget::pane {
    border: 1px solid #313244;
    background: #1e1e2e;
    border-radius: 6px;
}
QTabBar::tab {
    background: #181825;
    color: #a6adc8;
    padding: 10px 22px;
    border-radius: 4px;
    margin: 2px;
}
QTabBar::tab:selected {
    background: #313244;
    color: #cba6f7;
    font-weight: bold;
}
QGroupBox {
    border: 1px solid #313244;
    border-radius: 8px;
    margin-top: 12px;
    padding: 10px;
    color: #cba6f7;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px;
}
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: none;
    border-radius: 6px;
    padding: 8px 18px;
    font-size: 13px;
}
QPushButton:hover { background-color: #45475a; }
QPushButton:pressed { background-color: #585b70; }
QPushButton#btn_flash {
    background-color: #a6e3a1;
    color: #1e1e2e;
    font-weight: bold;
    font-size: 14px;
    padding: 10px 24px;
}
QPushButton#btn_flash:hover { background-color: #94e2a0; }
QPushButton#btn_flash:disabled { background-color: #313244; color: #6c7086; }
QPushButton#btn_backup {
    background-color: #89b4fa;
    color: #1e1e2e;
    font-weight: bold;
    font-size: 14px;
    padding: 10px 24px;
}
QPushButton#btn_backup:hover { background-color: #74c7ec; }
QPushButton#btn_backup:disabled { background-color: #313244; color: #6c7086; }
QPushButton#btn_stop {
    background-color: #f38ba8;
    color: #1e1e2e;
    font-weight: bold;
}
QPushButton#btn_stop:hover { background-color: #eba0ac; }
QComboBox {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px 10px;
}
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView {
    background-color: #313244;
    color: #cdd6f4;
    selection-background-color: #45475a;
}
QLineEdit {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px 10px;
}
QTextEdit {
    background-color: #11111b;
    color: #a6e3a1;
    border: 1px solid #313244;
    border-radius: 6px;
    font-family: 'Courier New', monospace;
    font-size: 12px;
}
QProgressBar {
    background-color: #313244;
    color: #cdd6f4;
    border: none;
    border-radius: 6px;
    height: 18px;
    text-align: center;
}
QProgressBar::chunk {
    background-color: #cba6f7;
    border-radius: 6px;
}
QLabel#lbl_title {
    color: #cba6f7;
    font-size: 18px;
    font-weight: bold;
}
QLabel#lbl_subtitle {
    color: #6c7086;
    font-size: 11px;
}
"""

class WorkerThread(QThread):
    output = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, cmd, parent=None):
        super().__init__(parent)
        self.cmd = cmd
        self.proc = None

    def run(self):
        self.output.emit(f"$ {' '.join(self.cmd)}\n")
        try:
            self.proc = subprocess.Popen(
                self.cmd, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, bufsize=1
            )
            for line in self.proc.stdout:
                self.output.emit(line)
                if "%" in line:
                    for tok in line.split():
                        tok = tok.strip("%")
                        if tok.isdigit():
                            self.progress.emit(int(tok))
                            break
            self.proc.wait()
            ok = self.proc.returncode == 0
            self.finished.emit(ok, "Zakończono pomyślnie." if ok else f"Błąd (kod {self.proc.returncode}).")
        except Exception as e:
            self.finished.emit(False, str(e))

    def stop(self):
        if self.proc:
            self.proc.terminate()


class PiSafeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PiSafe GUI")
        self.setMinimumSize(820, 640)
        self.worker = None
        self._build_ui()
        self.refresh_disks()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(10)

        hdr = QHBoxLayout()
        ico = QLabel("🫐")
        ico.setFont(QFont("Segoe UI Emoji", 26))
        title_col = QVBoxLayout()
        lbl_t = QLabel("PiSafe GUI")
        lbl_t.setObjectName("lbl_title")
        lbl_s = QLabel("Graficzny interfejs dla narzędzia pisafe")
        lbl_s.setObjectName("lbl_subtitle")
        title_col.addWidget(lbl_t)
        title_col.addWidget(lbl_s)
        hdr.addWidget(ico)
        hdr.addSpacing(8)
        hdr.addLayout(title_col)
        hdr.addStretch()
        btn_refresh = QPushButton("⟳  Odśwież dyski")
        btn_refresh.clicked.connect(self.refresh_disks)
        hdr.addWidget(btn_refresh)
        root.addLayout(hdr)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #313244;")
        root.addWidget(sep)

        tabs = QTabWidget()
        tabs.addTab(self._tab_flash(), "⚡  Flash obrazu → SD")
        tabs.addTab(self._tab_backup(), "💾  Backup SD → obraz")
        tabs.addTab(self._tab_list(), "📋  Lista dysków")
        root.addWidget(tabs, 1)

        grp_log = QGroupBox("Logi")
        log_lay = QVBoxLayout(grp_log)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(140)
        log_lay.addWidget(self.log)

        bar_row = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.btn_stop = QPushButton("■  Zatrzymaj")
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_task)
        bar_row.addWidget(self.progress, 1)
        bar_row.addWidget(self.btn_stop)
        log_lay.addLayout(bar_row)

        btn_clear = QPushButton("Wyczyść logi")
        btn_clear.clicked.connect(self.log.clear)
        log_lay.addWidget(btn_clear)
        root.addWidget(grp_log)

    def _tab_flash(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(12)

        grp = QGroupBox("Plik obrazu (.img / .zip / .xz / .gz / .zst)")
        gl = QVBoxLayout(grp)
        row = QHBoxLayout()
        self.flash_img_path = QLineEdit()
        self.flash_img_path.setPlaceholderText("Wybierz lub wpisz ścieżkę do pliku obrazu…")
        btn_browse = QPushButton("📂  Przeglądaj")
        btn_browse.clicked.connect(self.browse_image)
        row.addWidget(self.flash_img_path, 1)
        row.addWidget(btn_browse)
        gl.addLayout(row)
        lay.addWidget(grp)

        grp2 = QGroupBox("Dysk docelowy (SD / USB)")
        gl2 = QVBoxLayout(grp2)
        row2 = QHBoxLayout()
        self.flash_disk_combo = QComboBox()
        self.flash_disk_combo.setMinimumWidth(300)
        row2.addWidget(QLabel("Dysk:"))
        row2.addWidget(self.flash_disk_combo, 1)
        gl2.addLayout(row2)
        lbl_warn = QLabel("⚠️  Uwaga: zawartość wybranego dysku zostanie TRWALE nadpisana!")
        lbl_warn.setStyleSheet("color: #f38ba8; font-weight: bold;")
        gl2.addWidget(lbl_warn)
        lay.addWidget(grp2)

        lay.addStretch()
        self.btn_flash = QPushButton("⚡  Flash obrazu na dysk")
        self.btn_flash.setObjectName("btn_flash")
        self.btn_flash.clicked.connect(self.do_flash)
        lay.addWidget(self.btn_flash, 0, Qt.AlignRight)
        return w

    def _tab_backup(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(12)

        grp = QGroupBox("Dysk źródłowy (SD do backupu)")
        gl = QVBoxLayout(grp)
        row = QHBoxLayout()
        self.backup_disk_combo = QComboBox()
        self.backup_disk_combo.setMinimumWidth(300)
        row.addWidget(QLabel("Dysk:"))
        row.addWidget(self.backup_disk_combo, 1)
        gl.addLayout(row)
        lay.addWidget(grp)

        grp2 = QGroupBox("Plik wyjściowy obrazu")
        gl2 = QVBoxLayout(grp2)
        row_dir = QHBoxLayout()
        self.backup_dir = QLineEdit(os.path.expanduser("~"))
        btn_dir = QPushButton("📂  Folder")
        btn_dir.clicked.connect(self.browse_out_dir)
        row_dir.addWidget(QLabel("Katalog:"))
        row_dir.addWidget(self.backup_dir, 1)
        row_dir.addWidget(btn_dir)
        gl2.addLayout(row_dir)

        row_name = QHBoxLayout()
        self.backup_name = QLineEdit(f"backup_{datetime.now().strftime('%Y%m%d_%H%M')}")
        row_name.addWidget(QLabel("Nazwa pliku:"))
        row_name.addWidget(self.backup_name, 1)
        gl2.addLayout(row_name)

        row_fmt = QHBoxLayout()
        self.backup_fmt = QComboBox()
        self.backup_fmt.addItems([".img", ".zip", ".gz", ".xz", ".zst"])
        row_fmt.addWidget(QLabel("Kompresja:"))
        row_fmt.addWidget(self.backup_fmt)
        row_fmt.addStretch()
        gl2.addLayout(row_fmt)
        lay.addWidget(grp2)

        lay.addStretch()
        self.btn_backup = QPushButton("💾  Utwórz obraz dysku")
        self.btn_backup.setObjectName("btn_backup")
        self.btn_backup.clicked.connect(self.do_backup)
        lay.addWidget(self.btn_backup, 0, Qt.AlignRight)
        return w

    def _tab_list(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        self.list_output = QTextEdit()
        self.list_output.setReadOnly(True)
        lay.addWidget(self.list_output)
        btn = QPushButton("🔄  Odśwież listę dysków")
        btn.clicked.connect(self.show_disk_list)
        lay.addWidget(btn)
        QTimer.singleShot(500, self.show_disk_list)
        return w

    def browse_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Wybierz obraz", os.path.expanduser("~"),
            "Obrazy (*.img *.zip *.xz *.gz *.zst);;Wszystkie (*)"
        )
        if path:
            self.flash_img_path.setText(path)

    def browse_out_dir(self):
        d = QFileDialog.getExistingDirectory(self, "Wybierz katalog docelowy", self.backup_dir.text())
        if d:
            self.backup_dir.setText(d)

    def _get_system_disks(self):
        system_devs = set()
        try:
            out = subprocess.check_output(
                ["lsblk", "-o", "NAME,MOUNTPOINT", "--json"], text=True
            )
            data = json.loads(out)

            def check_device(dev, parent_name=None):
                name = dev.get("name", "")
                mnt = dev.get("mountpoint") or ""
                children = dev.get("children") or []
                if mnt in ("/", "/boot", "/boot/firmware", "/usr", "/var", "/home"):
                    if parent_name:
                        system_devs.add(parent_name)
                    else:
                        system_devs.add(name)
                for child in children:
                    check_device(child, parent_name=name)

            for dev in data.get("blockdevices", []):
                check_device(dev)
        except Exception as e:
            self.log_line(f"Ostrzeżenie: nie można sprawdzić dysków systemowych: {e}\n", "#f9e2af")
        return system_devs

    def _get_disks(self):
        try:
            system_disks = self._get_system_disks()
            out = subprocess.check_output(
                ["lsblk", "-d", "-o", "NAME,SIZE,MODEL,TRAN", "--json"], text=True
            )
            data = json.loads(out)
            result = []
            skipped = []
            for dev in data.get("blockdevices", []):
                name = dev.get("name", "")
                size = dev.get("size", "")
                model = dev.get("model") or ""
                tran = dev.get("tran") or ""
                if name in system_disks:
                    skipped.append(f"/dev/{name}")
                    continue
                label = f"/dev/{name}  [{size}]  {model.strip()}  {tran.upper()}"
                result.append(label)
            if skipped:
                self.log_line(f"Ukryto dyski systemowe: {', '.join(skipped)}\n", "#f9e2af")
            return result if result else ["(brak dostępnych dysków)"]
        except Exception as e:
            return [f"Błąd lsblk: {e}"]

    def refresh_disks(self):
        disks = self._get_disks()
        for combo in (self.flash_disk_combo, self.backup_disk_combo):
            combo.clear()
            combo.addItems(disks)
        self.log_line("Odświeżono listę dysków.\n")

    def _dev_from_combo(self, combo):
        txt = combo.currentText().strip()
        if txt.startswith("/dev/"):
            return txt.split()[0]
        return None

    def show_disk_list(self):
        self.list_output.clear()
        try:
            out = subprocess.check_output(
                ["lsblk", "-o", "NAME,SIZE,TYPE,FSTYPE,LABEL,MOUNTPOINT,MODEL"], text=True
            )
            self.list_output.setPlainText(out)
        except Exception as e:
            self.list_output.setPlainText(f"Błąd: {e}")

    def do_flash(self):
        img = self.flash_img_path.text().strip()
        dev = self._dev_from_combo(self.flash_disk_combo)
        if not img or not os.path.isfile(img):
            QMessageBox.warning(self, "Błąd", "Podaj prawidłową ścieżkę do pliku obrazu.")
            return
        if not dev:
            QMessageBox.warning(self, "Błąd", "Wybierz dysk docelowy.")
            return
        ret = QMessageBox.warning(
            self, "Potwierdź operację",
            f"UWAGA! Wszystkie dane na {dev} zostaną TRWALE usunięte!\n\n"
            f"Obraz: {img}\nDysk: {dev}\n\nCzy na pewno chcesz kontynuować?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        self._run(["sudo", "pisafe", "restore", img, dev, "-y"])

    def do_backup(self):
        dev = self._dev_from_combo(self.backup_disk_combo)
        out_dir = self.backup_dir.text().strip()
        name = self.backup_name.text().strip()
        fmt = self.backup_fmt.currentText()
        if not dev:
            QMessageBox.warning(self, "Błąd", "Wybierz dysk źródłowy.")
            return
        if not name:
            QMessageBox.warning(self, "Błąd", "Podaj nazwę pliku wyjściowego.")
            return
        out_path = os.path.join(out_dir, name + fmt)
        ret = QMessageBox.question(
            self, "Potwierdź backup",
            f"Tworzenie obrazu:\n  Dysk: {dev}\n  Plik: {out_path}\n\nKontynuować?",
            QMessageBox.Yes | QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        self._run(["sudo", "pisafe", "backup", dev, out_path, "-y"])

    def _run(self, cmd):
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, "Zajęty", "Trwa inne zadanie. Poczekaj lub je zatrzymaj.")
            return
        self.progress.setValue(0)
        self.btn_stop.setEnabled(True)
        self.btn_flash.setEnabled(False)
        self.btn_backup.setEnabled(False)
        self.worker = WorkerThread(cmd)
        self.worker.output.connect(self.log_line)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def stop_task(self):
        if self.worker:
            self.worker.stop()
            self.log_line("\n⛔ Zadanie przerwane przez użytkownika.\n")

    def on_finished(self, ok, msg):
        self.btn_stop.setEnabled(False)
        self.btn_flash.setEnabled(True)
        self.btn_backup.setEnabled(True)
        self.progress.setValue(100 if ok else 0)
        self.log_line(f"\n{'✅' if ok else '❌'} {msg}\n", "#a6e3a1" if ok else "#f38ba8")

    def log_line(self, text, color="#a6e3a1"):
        cursor = self.log.textCursor()
        cursor.movePosition(QTextCursor.End)
        fmt = cursor.charFormat()
        fmt.setForeground(QColor(color))
        cursor.setCharFormat(fmt)
        cursor.insertText(text)
        self.log.setTextCursor(cursor)
        self.log.ensureCursorVisible()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(DARK_STYLE)
    if subprocess.run(["which", "pisafe"], capture_output=True).returncode != 0:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("pisafe nie znalezione")
        msg.setText(
            "Narzędzie 'pisafe' nie jest zainstalowane.\n\n"
            "Zainstaluj je poleceniem:\n"
            "wget https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O pisafe\n"
            "bash pisafe install"
        )
        msg.exec_()
    win = PiSafeGUI()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
