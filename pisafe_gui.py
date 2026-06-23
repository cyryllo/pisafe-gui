#!/usr/bin/env python3
"""
PiSafe GUI – graficzny interfejs dla narzędzia pisafe
Wymagania: pip install PyQt5
Wymagane narzędzie: pisafe (zainstalowane w /usr/local/bin/pisafe)
"""

import sys
import os
import pty
import shutil
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

from translations import (
    LANGUAGES, DEFAULT_LANGUAGE, tr, set_language, get_language,
    get_saved_language, save_language,
)

set_language(get_saved_language() or DEFAULT_LANGUAGE)


def _read_version():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION")
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return "?"


APP_VERSION = _read_version()
ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
PISAFE_BIN = shutil.which("pisafe") or "/usr/local/bin/pisafe"

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
QLabel#lbl_version {
    color: #45475a;
    font-size: 10px;
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

    def _handle_chunk(self, text):
        if not text:
            return
        self.output.emit(text + "\n")
        if "%" in text:
            for tok in text.split():
                tok = tok.strip("%")
                if tok.isdigit():
                    self.progress.emit(int(tok))
                    break

    def run(self):
        # Tools like `pv` only print progress if their stderr looks like a
        # real terminal, so the child runs attached to a pty instead of a
        # plain pipe.
        self.output.emit(f"$ {' '.join(self.cmd)}\n")
        master_fd, slave_fd = -1, -1
        try:
            master_fd, slave_fd = pty.openpty()
            self.proc = subprocess.Popen(
                self.cmd, stdout=slave_fd, stderr=slave_fd, close_fds=True
            )
            os.close(slave_fd)
            slave_fd = -1

            buf = ""
            while True:
                try:
                    chunk = os.read(master_fd, 4096)
                except OSError:
                    break
                if not chunk:
                    break
                buf += chunk.decode("utf-8", errors="replace")
                while True:
                    idx_candidates = [i for i in (buf.find("\n"), buf.find("\r")) if i != -1]
                    if not idx_candidates:
                        break
                    idx = min(idx_candidates)
                    piece, buf = buf[:idx], buf[idx + 1:]
                    self._handle_chunk(piece)
            self._handle_chunk(buf)

            self.proc.wait()
            ok = self.proc.returncode == 0
            self.finished.emit(ok, tr("worker_success") if ok else tr("worker_error", code=self.proc.returncode))
        except Exception as e:
            self.finished.emit(False, str(e))
        finally:
            for fd in (master_fd, slave_fd):
                if fd != -1:
                    try:
                        os.close(fd)
                    except OSError:
                        pass

    def stop(self):
        if self.proc:
            self.proc.terminate()


class PiSafeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("window_title"))
        self.setMinimumSize(820, 640)
        self.worker = None
        self._finalizing = False
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
        lbl_t = QLabel(tr("window_title"))
        lbl_t.setObjectName("lbl_title")
        lbl_s = QLabel(tr("subtitle"))
        lbl_s.setObjectName("lbl_subtitle")
        title_col.addWidget(lbl_t)
        title_col.addWidget(lbl_s)
        hdr.addWidget(ico)
        hdr.addSpacing(8)
        hdr.addLayout(title_col)
        hdr.addStretch()
        hdr.addWidget(QLabel(tr("language_label")))
        self.lang_combo = QComboBox()
        for code, name in LANGUAGES.items():
            self.lang_combo.addItem(name, code)
        idx = self.lang_combo.findData(get_language())
        if idx >= 0:
            self.lang_combo.setCurrentIndex(idx)
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        hdr.addWidget(self.lang_combo)
        root.addLayout(hdr)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #313244;")
        root.addWidget(sep)

        tabs = QTabWidget()
        tabs.addTab(self._tab_flash(), tr("tab_flash"))
        tabs.addTab(self._tab_backup(), tr("tab_backup"))
        tabs.addTab(self._tab_list(), tr("tab_list"))
        root.addWidget(tabs, 1)

        grp_log = QGroupBox(tr("grp_logs"))
        log_lay = QVBoxLayout(grp_log)
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(140)
        log_lay.addWidget(self.log)

        bar_row = QHBoxLayout()
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.btn_stop = QPushButton(tr("btn_stop"))
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.stop_task)
        bar_row.addWidget(self.progress, 1)
        bar_row.addWidget(self.btn_stop)
        log_lay.addLayout(bar_row)

        btn_clear = QPushButton(tr("btn_clear_logs"))
        btn_clear.clicked.connect(self.log.clear)
        log_lay.addWidget(btn_clear)
        root.addWidget(grp_log)

        lbl_version = QLabel(f"v{APP_VERSION}")
        lbl_version.setObjectName("lbl_version")
        root.addWidget(lbl_version, 0, Qt.AlignRight)

    def _tab_flash(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(12)

        grp = QGroupBox(tr("grp_flash_image"))
        gl = QVBoxLayout(grp)
        row = QHBoxLayout()
        self.flash_img_path = QLineEdit()
        self.flash_img_path.setPlaceholderText(tr("flash_img_placeholder"))
        btn_browse = QPushButton(tr("btn_browse"))
        btn_browse.clicked.connect(self.browse_image)
        row.addWidget(self.flash_img_path, 1)
        row.addWidget(btn_browse)
        gl.addLayout(row)
        lay.addWidget(grp)

        grp2 = QGroupBox(tr("grp_flash_target"))
        gl2 = QVBoxLayout(grp2)
        row2 = QHBoxLayout()
        self.flash_disk_combo = QComboBox()
        self.flash_disk_combo.setMinimumWidth(300)
        row2.addWidget(QLabel(tr("label_disk")))
        row2.addWidget(self.flash_disk_combo, 1)
        btn_refresh1 = QPushButton(tr("btn_refresh_disks"))
        btn_refresh1.clicked.connect(self.refresh_disks)
        row2.addWidget(btn_refresh1)
        gl2.addLayout(row2)
        lbl_warn = QLabel(tr("flash_warning"))
        lbl_warn.setStyleSheet("color: #f38ba8; font-weight: bold;")
        gl2.addWidget(lbl_warn)
        lay.addWidget(grp2)

        lay.addStretch()
        self.btn_flash = QPushButton(tr("btn_flash"))
        self.btn_flash.setObjectName("btn_flash")
        self.btn_flash.clicked.connect(self.do_flash)
        lay.addWidget(self.btn_flash, 0, Qt.AlignRight)
        return w

    def _tab_backup(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(12)

        grp = QGroupBox(tr("grp_backup_source"))
        gl = QVBoxLayout(grp)
        row = QHBoxLayout()
        self.backup_disk_combo = QComboBox()
        self.backup_disk_combo.setMinimumWidth(300)
        row.addWidget(QLabel(tr("label_disk")))
        row.addWidget(self.backup_disk_combo, 1)
        btn_refresh2 = QPushButton(tr("btn_refresh_disks"))
        btn_refresh2.clicked.connect(self.refresh_disks)
        row.addWidget(btn_refresh2)
        gl.addLayout(row)
        lay.addWidget(grp)

        grp2 = QGroupBox(tr("grp_backup_output"))
        gl2 = QVBoxLayout(grp2)
        row_dir = QHBoxLayout()
        self.backup_dir = QLineEdit(os.path.expanduser("~"))
        btn_dir = QPushButton(tr("btn_dir"))
        btn_dir.clicked.connect(self.browse_out_dir)
        row_dir.addWidget(QLabel(tr("label_dir")))
        row_dir.addWidget(self.backup_dir, 1)
        row_dir.addWidget(btn_dir)
        gl2.addLayout(row_dir)

        row_name = QHBoxLayout()
        self.backup_name = QLineEdit(f"backup_{datetime.now().strftime('%Y%m%d_%H%M')}")
        row_name.addWidget(QLabel(tr("label_filename")))
        row_name.addWidget(self.backup_name, 1)
        gl2.addLayout(row_name)

        row_fmt = QHBoxLayout()
        self.backup_fmt = QComboBox()
        self.backup_fmt.addItems([".img", ".iso", ".zip", ".gz", ".xz", ".zst"])
        row_fmt.addWidget(QLabel(tr("label_compression")))
        row_fmt.addWidget(self.backup_fmt)
        row_fmt.addStretch()
        gl2.addLayout(row_fmt)
        lay.addWidget(grp2)

        lay.addStretch()
        self.btn_backup = QPushButton(tr("btn_backup"))
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
        btn = QPushButton(tr("btn_refresh_list"))
        btn.clicked.connect(self.show_disk_list)
        lay.addWidget(btn)
        QTimer.singleShot(500, self.show_disk_list)
        return w

    def change_language(self, index):
        code = self.lang_combo.itemData(index)
        if code and code != get_language():
            save_language(code)
            QMessageBox.information(self, tr("restart_required_title"), tr("restart_required_text"))
            os.execv(sys.executable, [sys.executable] + sys.argv)

    def browse_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, tr("dlg_choose_image_title"), os.path.expanduser("~"),
            tr("dlg_choose_image_filter")
        )
        if path:
            self.flash_img_path.setText(path)

    def browse_out_dir(self):
        d = QFileDialog.getExistingDirectory(self, tr("dlg_choose_dir_title"), self.backup_dir.text())
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
            self.log_line(tr("warn_system_disks", error=e) + "\n", "#f9e2af")
        return system_devs

    REMOVABLE_TRANSPORTS = {"usb", "mmc"}

    def _get_disks(self):
        try:
            system_disks = self._get_system_disks()
            out = subprocess.check_output(
                ["lsblk", "-d", "-o", "NAME,SIZE,MODEL,TRAN", "--json"], text=True
            )
            data = json.loads(out)
            result = []
            skipped = []
            skipped_other = []
            for dev in data.get("blockdevices", []):
                name = dev.get("name", "")
                size = dev.get("size", "")
                model = dev.get("model") or ""
                tran = dev.get("tran") or ""
                if name in system_disks:
                    skipped.append(f"/dev/{name}")
                    continue
                if tran.lower() not in self.REMOVABLE_TRANSPORTS:
                    skipped_other.append(f"/dev/{name}")
                    continue
                label = f"/dev/{name}  [{size}]  {model.strip()}  {tran.upper()}"
                result.append(label)
            if skipped:
                self.log_line(tr("hidden_system_disks", disks=", ".join(skipped)) + "\n", "#f9e2af")
            if skipped_other:
                self.log_line(tr("hidden_non_removable_disks", disks=", ".join(skipped_other)) + "\n", "#f9e2af")
            return result if result else [tr("no_disks_available")]
        except Exception as e:
            return [tr("lsblk_error", error=e)]

    def refresh_disks(self):
        disks = self._get_disks()
        for combo in (self.flash_disk_combo, self.backup_disk_combo):
            combo.clear()
            combo.addItems(disks)
        self.log_line(tr("disks_refreshed"))

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
            self.list_output.setPlainText(tr("list_error", error=e))

    def do_flash(self):
        img = self.flash_img_path.text().strip()
        dev = self._dev_from_combo(self.flash_disk_combo)
        if not img or not os.path.isfile(img):
            QMessageBox.warning(self, tr("error_title"), tr("error_invalid_image_path"))
            return
        if not dev:
            QMessageBox.warning(self, tr("error_title"), tr("error_select_target_disk"))
            return
        ret = QMessageBox.warning(
            self, tr("confirm_flash_title"),
            tr("confirm_flash_text", dev=dev, img=img),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        self._run(["pkexec", PISAFE_BIN, "restore", img, dev, "-y"])

    def do_backup(self):
        dev = self._dev_from_combo(self.backup_disk_combo)
        out_dir = self.backup_dir.text().strip()
        name = self.backup_name.text().strip()
        fmt = self.backup_fmt.currentText()
        if not dev:
            QMessageBox.warning(self, tr("error_title"), tr("error_select_source_disk"))
            return
        if not name:
            QMessageBox.warning(self, tr("error_title"), tr("error_filename_required"))
            return
        out_path = os.path.join(out_dir, name + fmt)
        ret = QMessageBox.question(
            self, tr("confirm_backup_title"),
            tr("confirm_backup_text", dev=dev, out_path=out_path),
            QMessageBox.Yes | QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        self._run(["pkexec", PISAFE_BIN, "backup", dev, out_path, "-y"])

    def _run(self, cmd):
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, tr("busy_title"), tr("busy_text"))
            return
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self._finalizing = False
        self.btn_stop.setEnabled(True)
        self.btn_flash.setEnabled(False)
        self.btn_backup.setEnabled(False)
        self.worker = WorkerThread(cmd)
        self.worker.output.connect(self.log_line)
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def stop_task(self):
        if self.worker:
            self.worker.stop()
            self.log_line(tr("task_stopped"))

    def on_progress(self, value):
        if value >= 100:
            # pv only measures how fast it can feed dd, not how fast dd
            # actually flushes to a (often much slower) USB/SD device, so
            # 100% here doesn't mean the write is actually done yet.
            if not self._finalizing:
                self._finalizing = True
                self.progress.setRange(0, 0)
                self.log_line(tr("finalizing_write") + "\n", "#f9e2af")
        else:
            self.progress.setRange(0, 100)
            self.progress.setValue(value)

    def on_finished(self, ok, msg):
        self.btn_stop.setEnabled(False)
        self.btn_flash.setEnabled(True)
        self.btn_backup.setEnabled(True)
        self.progress.setRange(0, 100)
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
    if os.path.isfile(ICON_PATH):
        app.setWindowIcon(QIcon(ICON_PATH))
    if subprocess.run(["which", "pisafe"], capture_output=True).returncode != 0:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(tr("pisafe_missing_title"))
        msg.setText(tr("pisafe_missing_text"))
        msg.exec_()
    if not shutil.which("pkexec"):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(tr("pkexec_missing_title"))
        msg.setText(tr("pkexec_missing_text"))
        msg.exec_()
    win = PiSafeGUI()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
