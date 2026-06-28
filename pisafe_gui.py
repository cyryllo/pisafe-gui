#!/usr/bin/env python3
"""
PiSafe GUI – graficzny interfejs dla narzędzia pisafe
Wymagania: pip install PyQt5
Wymagane narzędzie: pisafe (zainstalowane w /usr/local/bin/pisafe)
"""

import sys
import os
import pty
import re
import shutil
import sqlite3
import subprocess
import json
from datetime import datetime

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QComboBox, QFileDialog, QTextEdit,
    QTabWidget, QLineEdit, QMessageBox, QProgressBar, QFrame,
    QGroupBox, QSizePolicy, QInputDialog, QDialog, QDialogButtonBox,
    QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem,
    QAbstractItemView, QHeaderView,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QTextCursor

import db
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


def _slugify(text):
    text = re.sub(r"\s+", "_", text.strip())
    text = re.sub(r"[^A-Za-z0-9_-]", "", text)
    return text or "x"


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
    padding: 10px 26px;
    min-width: 190px;
    border-radius: 4px;
    margin: 2px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background: #313244;
    color: #cba6f7;
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
QPushButton#btn_result_ok, QPushButton#btn_result_ok:disabled {
    background-color: #a6e3a1;
    color: #1e1e2e;
    font-weight: bold;
}
QPushButton#btn_result_fail, QPushButton#btn_result_fail:disabled {
    background-color: #f38ba8;
    color: #1e1e2e;
    font-weight: bold;
}
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


class VersionNameDialog(QDialog):
    def __init__(self, project_name, suggested_label, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("version_dialog_title"))
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel(tr("version_dialog_project_label", name=project_name)))

        lay.addWidget(QLabel(tr("version_dialog_label_field")))
        self.label_edit = QLineEdit(suggested_label)
        lay.addWidget(self.label_edit)

        lay.addWidget(QLabel(tr("version_dialog_notes_field")))
        self.notes_edit = QLineEdit()
        lay.addWidget(self.notes_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

    def values(self):
        return self.label_edit.text().strip(), self.notes_edit.text().strip()


class PiSafeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("window_title"))
        self.setMinimumSize(1020, 800)
        self.worker = None
        self._finalizing = False
        self._active_project = None
        self._pending_db_entry = None
        self._build_ui()
        self.refresh_disks()
        self.refresh_projects()

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
        tabs.addTab(self._tab_versions(), tr("tab_versions"))
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

        grp_proj = QGroupBox(tr("grp_backup_project"))
        gl_proj = QHBoxLayout(grp_proj)
        self.project_combo = QComboBox()
        self.project_combo.setMinimumWidth(260)
        self.project_combo.currentIndexChanged.connect(self.on_project_combo_changed)
        gl_proj.addWidget(self.project_combo, 1)
        btn_new_project = QPushButton(tr("btn_new_project"))
        btn_new_project.clicked.connect(self.add_project)
        gl_proj.addWidget(btn_new_project)
        lay.addWidget(grp_proj)

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

    def _tab_versions(self):
        w = QWidget()
        lay = QHBoxLayout(w)

        grp_proj = QGroupBox(tr("grp_projects"))
        gl_proj = QVBoxLayout(grp_proj)
        self.projects_list = QListWidget()
        self.projects_list.currentItemChanged.connect(lambda *_: self.refresh_images_table())
        gl_proj.addWidget(self.projects_list, 1)
        proj_btn_row = QHBoxLayout()
        btn_new = QPushButton(tr("btn_new_project"))
        btn_new.clicked.connect(self.add_project)
        btn_del_proj = QPushButton(tr("btn_delete_project"))
        btn_del_proj.clicked.connect(self.delete_selected_project)
        proj_btn_row.addWidget(btn_new)
        proj_btn_row.addWidget(btn_del_proj)
        gl_proj.addLayout(proj_btn_row)
        lay.addWidget(grp_proj, 1)

        grp_img = QGroupBox(tr("grp_images"))
        gl_img = QVBoxLayout(grp_img)
        self.images_table = QTableWidget(0, 6)
        self.images_table.setHorizontalHeaderLabels([
            tr("col_version"), tr("col_file"), tr("col_date"),
            tr("col_size"), tr("col_source_disk"), tr("col_notes"),
        ])
        self.images_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.images_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.images_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        gl_img.addWidget(self.images_table, 1)
        img_btn_row = QHBoxLayout()
        btn_refresh_img = QPushButton(tr("btn_refresh_images"))
        btn_refresh_img.clicked.connect(self.refresh_images_table)
        btn_open_folder = QPushButton(tr("btn_open_folder"))
        btn_open_folder.clicked.connect(self.open_project_folder)
        btn_del_img = QPushButton(tr("btn_delete_entry"))
        btn_del_img.clicked.connect(self.delete_selected_image)
        img_btn_row.addWidget(btn_refresh_img)
        img_btn_row.addWidget(btn_open_folder)
        img_btn_row.addWidget(btn_del_img)
        gl_img.addLayout(img_btn_row)
        lay.addWidget(grp_img, 3)

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

    def refresh_projects(self):
        projects = db.list_projects()
        self.project_combo.blockSignals(True)
        self.project_combo.clear()
        self.project_combo.addItem(tr("project_combo_none"), None)
        for p in projects:
            self.project_combo.addItem(p["name"], p["id"])
        self.project_combo.blockSignals(False)

        current_proj_id = None
        current_item = self.projects_list.currentItem()
        if current_item:
            current_proj_id = current_item.data(Qt.UserRole)
        self.projects_list.clear()
        for p in projects:
            item = QListWidgetItem(p["name"])
            item.setData(Qt.UserRole, p["id"])
            self.projects_list.addItem(item)
            if p["id"] == current_proj_id:
                self.projects_list.setCurrentItem(item)

    def on_project_combo_changed(self, index):
        project_id = self.project_combo.itemData(index)
        if project_id is None:
            self._active_project = None
            return
        project = db.get_project(project_id)
        suggested = db.next_version_label(project_id)
        dlg = VersionNameDialog(project["name"], suggested, self)
        if dlg.exec_() != QDialog.Accepted:
            self.project_combo.blockSignals(True)
            self.project_combo.setCurrentIndex(0)
            self.project_combo.blockSignals(False)
            self._active_project = None
            return
        label, notes = dlg.values()
        if not label:
            label = suggested
        self.backup_dir.setText(project["folder"])
        self.backup_name.setText(f"{_slugify(project['name'])}_{_slugify(label)}")
        self._active_project = {
            "id": project_id, "version_label": label, "notes": notes or None,
        }

    def add_project(self):
        name, ok = QInputDialog.getText(self, tr("new_project_title"), tr("new_project_name_label"))
        if not ok or not name.strip():
            return
        folder = QFileDialog.getExistingDirectory(self, tr("new_project_folder_title"), os.path.expanduser("~"))
        if not folder:
            return
        try:
            db.create_project(name.strip(), folder)
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, tr("error_title"), tr("project_name_exists"))
            return
        self.refresh_projects()

    def _selected_project_id(self):
        item = self.projects_list.currentItem()
        return item.data(Qt.UserRole) if item else None

    def delete_selected_project(self):
        project_id = self._selected_project_id()
        if project_id is None:
            QMessageBox.warning(self, tr("error_title"), tr("no_project_selected"))
            return
        project = db.get_project(project_id)
        ret = QMessageBox.question(
            self, tr("confirm_delete_project_title"),
            tr("confirm_delete_project_text", name=project["name"]),
            QMessageBox.Yes | QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        db.delete_project(project_id)
        self.refresh_projects()
        self.images_table.setRowCount(0)

    def refresh_images_table(self):
        project_id = self._selected_project_id()
        self.images_table.setRowCount(0)
        if project_id is None:
            return
        for row, img in enumerate(db.list_images(project_id)):
            self.images_table.insertRow(row)
            size = img["size_bytes"]
            size_str = f"{size / (1024 * 1024):.1f} MB" if size else ""
            values = [
                img["version_label"], img["file_path"], img["created_at"],
                size_str, img["source_disk"] or "", img["notes"] or "",
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                if col == 0:
                    item.setData(Qt.UserRole, img["id"])
                self.images_table.setItem(row, col, item)

    def open_project_folder(self):
        project_id = self._selected_project_id()
        if project_id is None:
            QMessageBox.warning(self, tr("error_title"), tr("no_project_selected"))
            return
        project = db.get_project(project_id)
        if not os.path.isdir(project["folder"]):
            QMessageBox.warning(self, tr("error_title"), tr("project_folder_missing", folder=project["folder"]))
            return
        subprocess.Popen(["xdg-open", project["folder"]])

    def delete_selected_image(self):
        row = self.images_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, tr("error_title"), tr("no_image_selected"))
            return
        image_id = self.images_table.item(row, 0).data(Qt.UserRole)

        box = QMessageBox(self)
        box.setWindowTitle(tr("confirm_delete_image_title"))
        box.setText(tr("confirm_delete_image_text"))
        btn_only = box.addButton(tr("btn_delete_entry_only"), QMessageBox.AcceptRole)
        btn_with_file = box.addButton(tr("btn_delete_entry_and_file"), QMessageBox.DestructiveRole)
        box.addButton(QMessageBox.Cancel)
        box.exec_()
        clicked = box.clickedButton()
        if clicked == btn_only:
            db.delete_image(image_id, delete_file=False)
        elif clicked == btn_with_file:
            db.delete_image(image_id, delete_file=True)
        else:
            return
        self.refresh_images_table()

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
        if self._active_project:
            self._pending_db_entry = {
                "project_id": self._active_project["id"],
                "version_label": self._active_project["version_label"],
                "file_path": out_path,
                "source_disk": dev,
                "notes": self._active_project["notes"],
            }
            self._active_project = None
            self.project_combo.blockSignals(True)
            self.project_combo.setCurrentIndex(0)
            self.project_combo.blockSignals(False)
        self._run(["pkexec", PISAFE_BIN, "backup", dev, out_path, "-y"])

    def _restyle(self, widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def _run(self, cmd):
        if self.worker and self.worker.isRunning():
            QMessageBox.warning(self, tr("busy_title"), tr("busy_text"))
            return
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self._finalizing = False
        self.btn_stop.setObjectName("btn_stop")
        self.btn_stop.setText(tr("btn_stop"))
        self._restyle(self.btn_stop)
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
        self.btn_stop.setObjectName("btn_result_ok" if ok else "btn_result_fail")
        self.btn_stop.setText(tr("btn_result_ok") if ok else tr("btn_result_fail"))
        self._restyle(self.btn_stop)
        self.log_line(f"\n{'✅' if ok else '❌'} {msg}\n", "#a6e3a1" if ok else "#f38ba8")

        if ok and self._pending_db_entry:
            entry = self._pending_db_entry
            try:
                entry["size_bytes"] = os.path.getsize(entry["file_path"])
            except OSError:
                entry["size_bytes"] = None
            db.add_image(**entry)
            self.refresh_images_table()
        self._pending_db_entry = None

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
