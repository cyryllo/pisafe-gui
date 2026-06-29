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
    QAbstractItemView, QHeaderView, QCheckBox, QScrollArea, QToolButton,
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QPointF, QRectF
from PyQt5.QtGui import (
    QFont, QColor, QPalette, QIcon, QTextCursor, QPainter, QPen, QPixmap,
)

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


def _draw_arrow_left(p, s):
    p.drawPolyline(QPointF(s * 0.62, s * 0.2), QPointF(s * 0.3, s * 0.5), QPointF(s * 0.62, s * 0.8))


def _draw_arrow_right(p, s):
    p.drawPolyline(QPointF(s * 0.38, s * 0.2), QPointF(s * 0.7, s * 0.5), QPointF(s * 0.38, s * 0.8))


def _draw_arrow_up(p, s):
    p.drawPolyline(QPointF(s * 0.2, s * 0.62), QPointF(s * 0.5, s * 0.3), QPointF(s * 0.8, s * 0.62))


def _draw_new_folder(p, s):
    p.drawRoundedRect(QRectF(s * 0.15, s * 0.32, s * 0.7, s * 0.5), 2, 2)
    p.drawLine(QPointF(s * 0.5, s * 0.45), QPointF(s * 0.5, s * 0.72))
    p.drawLine(QPointF(s * 0.37, s * 0.585), QPointF(s * 0.63, s * 0.585))


def _draw_list_view(p, s):
    for frac in (0.28, 0.5, 0.72):
        p.drawLine(QPointF(s * 0.18, s * frac), QPointF(s * 0.82, s * frac))


def _draw_detail_view(p, s):
    for frac in (0.28, 0.5, 0.72):
        p.drawEllipse(QPointF(s * 0.22, s * frac), s * 0.04, s * 0.04)
        p.drawLine(QPointF(s * 0.36, s * frac), QPointF(s * 0.82, s * frac))


_DIALOG_ICON_DRAWERS = {
    "backButton": _draw_arrow_left,
    "forwardButton": _draw_arrow_right,
    "toParentButton": _draw_arrow_up,
    "newFolderButton": _draw_new_folder,
    "listModeButton": _draw_list_view,
    "detailModeButton": _draw_detail_view,
}


def _make_dialog_icon(draw_fn, size=18, color="#cdd6f4"):
    # Some desktop icon themes render the QFileDialog toolbar icons
    # (back/forward/up/new folder/view mode) in a dark color that's
    # invisible against our dark theme, so we draw our own instead.
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    pen = QPen(QColor(color))
    pen.setWidthF(1.6)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.NoBrush)
    draw_fn(p, size)
    p.end()
    return QIcon(pm)


APP_VERSION = _read_version()
ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
PISAFE_BIN = shutil.which("pisafe") or "/usr/local/bin/pisafe"

VERIFY_SCRIPT = (
    'set -e\n'
    'SRC_HASH=$(pv "$1" | sha256sum | cut -d\' \' -f1)\n'
    'echo "SRC_HASH=$SRC_HASH"\n'
    'DST_HASH=$(head -c "$3" "$2" | pv -s "$3" | sha256sum | cut -d\' \' -f1)\n'
    'echo "DST_HASH=$DST_HASH"\n'
    'if [ "$SRC_HASH" = "$DST_HASH" ]; then echo "VERIFY_RESULT=MATCH"; '
    'else echo "VERIFY_RESULT=MISMATCH"; fi\n'
)

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
    MAX_FLASH_TARGETS = 8

    def __init__(self):
        super().__init__()
        self.setWindowTitle(tr("window_title"))
        self.setMinimumSize(1020, 980)
        self.worker = None
        self._finalizing = False
        self._active_project = None
        self._pending_db_entry = None
        self._pending_verify = None
        self._verifying = False
        self._checking_image = False
        self._expected_image_hash = None
        self._last_output_lines = []
        self.target_rows = []
        self.multi_jobs = []
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
        tabs.addTab(self._tab_versions(), tr("tab_versions"))
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
        self.btn_check_image = QPushButton(tr("btn_check_image"))
        self.btn_check_image.clicked.connect(self.check_image)
        row.addWidget(self.flash_img_path, 1)
        row.addWidget(btn_browse)
        row.addWidget(self.btn_check_image)
        gl.addLayout(row)
        lay.addWidget(grp)

        grp2 = QGroupBox(tr("grp_flash_target"))
        gl2 = QVBoxLayout(grp2)

        self.targets_container = QWidget()
        self.targets_layout = QVBoxLayout(self.targets_container)
        self.targets_layout.setContentsMargins(0, 0, 0, 0)
        self.targets_layout.setSpacing(4)
        targets_scroll = QScrollArea()
        targets_scroll.setWidgetResizable(True)
        targets_scroll.setWidget(self.targets_container)
        targets_scroll.setMaximumHeight(130)
        targets_scroll.setFrameShape(QFrame.NoFrame)
        gl2.addWidget(targets_scroll)

        targets_btn_row = QHBoxLayout()
        self.btn_add_target = QPushButton(tr("btn_add_target"))
        self.btn_add_target.clicked.connect(self._add_target_row)
        btn_refresh1 = QPushButton(tr("btn_refresh_disks"))
        btn_refresh1.clicked.connect(self.refresh_disks)
        targets_btn_row.addWidget(self.btn_add_target)
        targets_btn_row.addWidget(btn_refresh1)
        targets_btn_row.addStretch()
        gl2.addLayout(targets_btn_row)

        lbl_warn = QLabel(tr("flash_warning"))
        lbl_warn.setStyleSheet("color: #f38ba8; font-weight: bold;")
        gl2.addWidget(lbl_warn)
        self.verify_checkbox = QCheckBox(tr("verify_checkbox_label"))
        gl2.addWidget(self.verify_checkbox)
        lay.addWidget(grp2)

        self._add_target_row()

        self.grp_multi_progress = QGroupBox(tr("grp_multi_progress"))
        self.grp_multi_progress.setVisible(False)
        gl3 = QVBoxLayout(self.grp_multi_progress)
        self.multi_progress_container = QWidget()
        self.multi_progress_layout = QVBoxLayout(self.multi_progress_container)
        self.multi_progress_layout.setContentsMargins(0, 0, 0, 0)
        self.multi_progress_layout.setSpacing(4)
        multi_scroll = QScrollArea()
        multi_scroll.setWidgetResizable(True)
        multi_scroll.setWidget(self.multi_progress_container)
        multi_scroll.setMaximumHeight(130)
        multi_scroll.setFrameShape(QFrame.NoFrame)
        gl3.addWidget(multi_scroll)
        self.btn_stop_multi = QPushButton(tr("btn_stop_multi"))
        self.btn_stop_multi.setEnabled(False)
        self.btn_stop_multi.clicked.connect(self.stop_multi_flash)
        gl3.addWidget(self.btn_stop_multi, 0, Qt.AlignRight)
        lay.addWidget(self.grp_multi_progress)

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

        grp_tools = QGroupBox(tr("grp_disk_tools"))
        gl_tools = QVBoxLayout(grp_tools)
        row_disk = QHBoxLayout()
        self.tools_disk_combo = QComboBox()
        self.tools_disk_combo.setMinimumWidth(300)
        row_disk.addWidget(QLabel(tr("label_disk")))
        row_disk.addWidget(self.tools_disk_combo, 1)
        btn_refresh3 = QPushButton(tr("btn_refresh_disks"))
        btn_refresh3.clicked.connect(self.refresh_disks)
        row_disk.addWidget(btn_refresh3)
        gl_tools.addLayout(row_disk)

        self.btn_disk_details = QPushButton(tr("btn_disk_details"))
        self.btn_disk_details.clicked.connect(self.show_disk_details)
        gl_tools.addWidget(self.btn_disk_details)

        lbl_erase_warn = QLabel(tr("erase_warning"))
        lbl_erase_warn.setStyleSheet("color: #f38ba8; font-weight: bold;")
        gl_tools.addWidget(lbl_erase_warn)

        row_erase = QHBoxLayout()
        self.erase_fmt_combo = QComboBox()
        self.erase_fmt_combo.addItems(["fat32", "exfat", "ntfs", "ext4"])
        row_erase.addWidget(QLabel(tr("label_format")))
        row_erase.addWidget(self.erase_fmt_combo)
        self.btn_erase = QPushButton(tr("btn_erase"))
        self.btn_erase.clicked.connect(self.do_erase)
        row_erase.addWidget(self.btn_erase)
        row_erase.addStretch()
        gl_tools.addLayout(row_erase)
        lay.addWidget(grp_tools)

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

    def _add_target_row(self):
        if len(self.target_rows) >= self.MAX_FLASH_TARGETS:
            return
        row_widget = QWidget()
        row_lay = QHBoxLayout(row_widget)
        row_lay.setContentsMargins(0, 0, 0, 0)
        combo = QComboBox()
        combo.setMinimumWidth(260)
        combo.addItems(getattr(self, "_disk_cache", []))
        btn_remove = QPushButton("-")
        btn_remove.setFixedWidth(30)
        btn_remove.clicked.connect(lambda: self._remove_target_row(row_widget))
        row_lay.addWidget(QLabel(tr("label_disk")))
        row_lay.addWidget(combo, 1)
        row_lay.addWidget(btn_remove)
        self.targets_layout.addWidget(row_widget)
        self.target_rows.append({"widget": row_widget, "combo": combo, "remove_btn": btn_remove})
        self._update_target_row_buttons()

    def _remove_target_row(self, row_widget):
        entry = next((e for e in self.target_rows if e["widget"] is row_widget), None)
        if not entry or len(self.target_rows) <= 1:
            return
        self.target_rows.remove(entry)
        row_widget.setParent(None)
        row_widget.deleteLater()
        self._update_target_row_buttons()

    def _update_target_row_buttons(self):
        self.btn_add_target.setEnabled(len(self.target_rows) < self.MAX_FLASH_TARGETS)
        only_one = len(self.target_rows) <= 1
        for entry in self.target_rows:
            entry["remove_btn"].setEnabled(not only_one)

    def change_language(self, index):
        code = self.lang_combo.itemData(index)
        if code and code != get_language():
            save_language(code)
            QMessageBox.information(self, tr("restart_required_title"), tr("restart_required_text"))
            os.execv(sys.executable, [sys.executable] + sys.argv)

    def _sized_dialog(self, dlg):
        # The native file dialog can come back oddly sized/clipped on some
        # desktop environments, so we use Qt's own dialog, size it ourselves
        # with a margin from the screen edges, and center it.
        dlg.setOption(QFileDialog.DontUseNativeDialog, True)
        screen = QApplication.primaryScreen().availableGeometry()
        margin = 40
        w = min(900, screen.width() - 2 * margin)
        h = min(600, screen.height() - 2 * margin)
        dlg.resize(w, h)
        dlg.move(screen.center().x() - w // 2, screen.center().y() - h // 2)
        if dlg.layout():
            dlg.layout().setContentsMargins(14, 14, 14, 14)
            dlg.layout().setSpacing(8)
        for name, draw_fn in _DIALOG_ICON_DRAWERS.items():
            btn = dlg.findChild(QToolButton, name)
            if btn:
                btn.setIcon(_make_dialog_icon(draw_fn))
        return dlg

    def _pick_open_file(self, title, directory, filter_):
        dlg = self._sized_dialog(QFileDialog(self, title, directory, filter_))
        dlg.setFileMode(QFileDialog.ExistingFile)
        if dlg.exec_() == QDialog.Accepted and dlg.selectedFiles():
            return dlg.selectedFiles()[0]
        return ""

    def _pick_directory(self, title, directory):
        dlg = self._sized_dialog(QFileDialog(self, title, directory))
        dlg.setFileMode(QFileDialog.Directory)
        dlg.setOption(QFileDialog.ShowDirsOnly, True)
        if dlg.exec_() == QDialog.Accepted and dlg.selectedFiles():
            return dlg.selectedFiles()[0]
        return ""

    def browse_image(self):
        path = self._pick_open_file(
            tr("dlg_choose_image_title"), os.path.expanduser("~"), tr("dlg_choose_image_filter")
        )
        if path:
            self.flash_img_path.setText(path)

    def browse_out_dir(self):
        d = self._pick_directory(tr("dlg_choose_dir_title"), self.backup_dir.text())
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
        folder = self._pick_directory(tr("new_project_folder_title"), os.path.expanduser("~"))
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
        self._disk_cache = disks
        for entry in self.target_rows:
            entry["combo"].clear()
            entry["combo"].addItems(disks)
        self.backup_disk_combo.clear()
        self.backup_disk_combo.addItems(disks)
        self.tools_disk_combo.clear()
        self.tools_disk_combo.addItems(disks)
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

    def _find_checksum_file(self, img):
        basename = os.path.basename(img)
        for path in (img + ".sha256", img + ".sha256sum", img + ".md5"):
            if not os.path.isfile(path):
                continue
            try:
                content = open(path, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            lines = [l for l in content.splitlines() if basename in l] or content.splitlines()
            for line in lines:
                m = re.search(r"\b([0-9a-fA-F]{64}|[0-9a-fA-F]{32})\b", line)
                if m:
                    token = m.group(1)
                    algo = "sha256" if len(token) == 64 else "md5"
                    return token.lower(), algo
        return None, None

    def check_image(self):
        img = self.flash_img_path.text().strip()
        if not img or not os.path.isfile(img):
            QMessageBox.warning(self, tr("error_title"), tr("error_invalid_image_path"))
            return
        if self._is_busy():
            QMessageBox.warning(self, tr("busy_title"), tr("busy_text"))
            return
        expected, algo = self._find_checksum_file(img)
        if not expected:
            text, ok = QInputDialog.getText(self, tr("checksum_paste_title"), tr("checksum_paste_label"))
            if not ok or not text.strip():
                return
            expected = text.strip().lower()
            algo = "sha256" if len(expected) == 64 else "md5" if len(expected) == 32 else None
            if not algo:
                QMessageBox.warning(self, tr("error_title"), tr("error_invalid_checksum"))
                return
        self._expected_image_hash = expected.lower()
        self._checking_image = True
        self.log_line(tr("checksum_running", algo=algo.upper()), "#89b4fa")
        self._run(["bash", "-c", f'pv "$1" | {algo}sum', "bash", img])

    def _is_busy(self):
        if self.worker and self.worker.isRunning():
            return True
        return any(not job["done"] for job in self.multi_jobs)

    def do_flash(self):
        img = self.flash_img_path.text().strip()
        if not img or not os.path.isfile(img):
            QMessageBox.warning(self, tr("error_title"), tr("error_invalid_image_path"))
            return
        if self._is_busy():
            QMessageBox.warning(self, tr("busy_title"), tr("busy_text"))
            return

        devices, seen, dupes = [], set(), False
        for entry in self.target_rows:
            dev = self._dev_from_combo(entry["combo"])
            if not dev:
                continue
            if dev in seen:
                dupes = True
                continue
            devices.append(dev)
            seen.add(dev)
        if dupes:
            QMessageBox.warning(self, tr("error_title"), tr("error_duplicate_targets"))
            return
        if not devices:
            QMessageBox.warning(self, tr("error_title"), tr("error_select_target_disk"))
            return

        if len(devices) == 1:
            confirm_text = tr("confirm_flash_text", dev=devices[0], img=img)
        else:
            confirm_text = tr("confirm_flash_text_multi", devices=", ".join(devices), img=img)
        ret = QMessageBox.warning(
            self, tr("confirm_flash_title"), confirm_text,
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return

        if len(devices) == 1:
            dev = devices[0]
            if self.verify_checkbox.isChecked():
                if os.path.splitext(img)[1].lower() in (".img", ".iso"):
                    self._pending_verify = {"img": img, "dev": dev, "size": os.path.getsize(img)}
                else:
                    self.log_line(tr("verify_unsupported_format"), "#f9e2af")
            self._run(["pkexec", PISAFE_BIN, "restore", img, dev, "-y"])
            return

        if self.verify_checkbox.isChecked():
            self.log_line(tr("verify_unsupported_multi"), "#f9e2af")
        self._start_multi_flash(img, devices)

    def _clear_multi_progress_rows(self):
        while self.multi_progress_layout.count():
            item = self.multi_progress_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

    def _start_multi_flash(self, img, devices):
        self.btn_flash.setEnabled(False)
        self.btn_check_image.setEnabled(False)
        self.btn_disk_details.setEnabled(False)
        self.btn_erase.setEnabled(False)
        self._clear_multi_progress_rows()
        self.grp_multi_progress.setVisible(True)
        self.multi_jobs = []
        for dev in devices:
            row_widget = QWidget()
            row_lay = QHBoxLayout(row_widget)
            row_lay.setContentsMargins(0, 0, 0, 0)
            lbl_dev = QLabel(dev)
            lbl_dev.setMinimumWidth(110)
            pbar = QProgressBar()
            pbar.setRange(0, 100)
            pbar.setValue(0)
            lbl_status = QLabel("⏳")
            row_lay.addWidget(lbl_dev)
            row_lay.addWidget(pbar, 1)
            row_lay.addWidget(lbl_status)
            self.multi_progress_layout.addWidget(row_widget)

            worker = WorkerThread(["pkexec", PISAFE_BIN, "restore", img, dev, "-y"])
            job = {
                "dev": dev, "worker": worker, "progress": pbar, "status": lbl_status,
                "finalizing": False, "done": False, "ok": None,
            }
            worker.output.connect(lambda text, d=dev: self.log_line(f"[{d}] {text}"))
            worker.progress.connect(lambda v, j=job: self._on_multi_progress(j, v))
            worker.finished.connect(lambda ok, msg, j=job: self._on_multi_finished(j, ok, msg))
            self.multi_jobs.append(job)

        self.btn_stop_multi.setEnabled(True)
        self.log_line(
            tr("multi_flash_started", n=len(devices), devices=", ".join(devices)) + "\n", "#89b4fa"
        )
        for job in self.multi_jobs:
            job["worker"].start()

    def _on_multi_progress(self, job, value):
        if value >= 100:
            if not job["finalizing"]:
                job["finalizing"] = True
                job["progress"].setRange(0, 0)
        else:
            job["progress"].setRange(0, 100)
            job["progress"].setValue(value)

    def _on_multi_finished(self, job, ok, msg):
        job["done"] = True
        job["ok"] = ok
        job["progress"].setRange(0, 100)
        job["progress"].setValue(100 if ok else 0)
        job["status"].setText("✅" if ok else "❌")
        self.log_line(f"[{job['dev']}] {'✅' if ok else '❌'} {msg}\n", "#a6e3a1" if ok else "#f38ba8")
        if all(j["done"] for j in self.multi_jobs):
            self._finish_multi_flash()

    def _finish_multi_flash(self):
        ok_count = sum(1 for j in self.multi_jobs if j["ok"])
        fail_count = len(self.multi_jobs) - ok_count
        self.log_line(
            tr("multi_flash_summary", ok=ok_count, fail=fail_count) + "\n",
            "#a6e3a1" if fail_count == 0 else "#f38ba8",
        )
        self.btn_flash.setEnabled(True)
        self.btn_check_image.setEnabled(True)
        self.btn_disk_details.setEnabled(True)
        self.btn_erase.setEnabled(True)
        self.btn_stop_multi.setEnabled(False)

    def stop_multi_flash(self):
        for job in self.multi_jobs:
            if not job["done"]:
                job["worker"].stop()
        self.log_line(tr("task_stopped"))

    def do_backup(self):
        if self._is_busy():
            QMessageBox.warning(self, tr("busy_title"), tr("busy_text"))
            return
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

    def show_disk_details(self):
        dev = self._dev_from_combo(self.tools_disk_combo)
        if not dev:
            QMessageBox.warning(self, tr("error_title"), tr("error_select_target_disk"))
            return
        if self._is_busy():
            QMessageBox.warning(self, tr("busy_title"), tr("busy_text"))
            return
        self._run(["pkexec", PISAFE_BIN, "details", dev])

    def do_erase(self):
        dev = self._dev_from_combo(self.tools_disk_combo)
        fmt = self.erase_fmt_combo.currentText()
        if not dev:
            QMessageBox.warning(self, tr("error_title"), tr("error_select_target_disk"))
            return
        if self._is_busy():
            QMessageBox.warning(self, tr("busy_title"), tr("busy_text"))
            return
        ret = QMessageBox.warning(
            self, tr("confirm_erase_title"), tr("confirm_erase_text", dev=dev, fmt=fmt),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if ret != QMessageBox.Yes:
            return
        self._run(["pkexec", PISAFE_BIN, "erase", dev, fmt, "-y"])

    def _restyle(self, widget):
        widget.style().unpolish(widget)
        widget.style().polish(widget)

    def _run(self, cmd):
        if self._is_busy():
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
        self.btn_check_image.setEnabled(False)
        self.btn_disk_details.setEnabled(False)
        self.btn_erase.setEnabled(False)
        self._last_output_lines = []
        self.worker = WorkerThread(cmd)
        self.worker.output.connect(self.log_line)
        self.worker.output.connect(self._last_output_lines.append)
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
                if self._checking_image or self._verifying:
                    self.log_line(tr("finalizing_checksum") + "\n", "#f9e2af")
                else:
                    self.log_line(tr("finalizing_write") + "\n", "#f9e2af")
        else:
            self.progress.setRange(0, 100)
            self.progress.setValue(value)

    def on_finished(self, ok, msg):
        if self._checking_image:
            self._checking_image = False
            combined = "".join(self._last_output_lines)
            m = re.search(r"\b([0-9a-fA-F]{64}|[0-9a-fA-F]{32})\b", combined)
            expected = self._expected_image_hash
            self._expected_image_hash = None
            if not ok or not m:
                self._finish_ui(False, tr("checksum_error_full"))
            elif m.group(1).lower() == expected:
                self._finish_ui(True, tr("checksum_match_full"))
            else:
                self._finish_ui(False, tr("checksum_mismatch_full"))
            return

        if self._verifying:
            self._verifying = False
            combined = "".join(self._last_output_lines)
            verify_match = re.search(r"VERIFY_RESULT=(MATCH|MISMATCH)", combined)
            if not ok or not verify_match:
                self._finish_ui(False, tr("verify_error_full"))
            elif verify_match.group(1) == "MATCH":
                self._finish_ui(True, tr("verify_match_full"))
            else:
                self._finish_ui(False, tr("verify_mismatch_full"))
            return

        if ok and self._pending_verify:
            info = self._pending_verify
            self._pending_verify = None
            self._verifying = True
            self.log_line(tr("verify_running"), "#89b4fa")
            cmd = ["pkexec", "/bin/bash", "-c", VERIFY_SCRIPT, "bash",
                   info["img"], info["dev"], str(info["size"])]
            self._run(cmd)
            return

        self._pending_verify = None
        self._finish_ui(ok, msg)

        if ok and self._pending_db_entry:
            entry = self._pending_db_entry
            try:
                entry["size_bytes"] = os.path.getsize(entry["file_path"])
            except OSError:
                entry["size_bytes"] = None
            db.add_image(**entry)
            self.refresh_images_table()
        self._pending_db_entry = None

    def _finish_ui(self, ok, msg):
        self.btn_stop.setEnabled(False)
        self.btn_flash.setEnabled(True)
        self.btn_backup.setEnabled(True)
        self.btn_check_image.setEnabled(True)
        self.btn_disk_details.setEnabled(True)
        self.btn_erase.setEnabled(True)
        self.progress.setRange(0, 100)
        self.progress.setValue(100 if ok else 0)
        self.btn_stop.setObjectName("btn_result_ok" if ok else "btn_result_fail")
        self.btn_stop.setText(tr("btn_result_ok") if ok else tr("btn_result_fail"))
        self._restyle(self.btn_stop)
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
