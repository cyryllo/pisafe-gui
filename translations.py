"""Translation strings and language persistence for PiSafe GUI.

Add a new language by adding a new entry to LANGUAGES and a matching
dictionary (with the same keys as the "en" dictionary) to TRANSLATIONS.
"""

import json
import os

LANGUAGES = {
    "en": "English",
    "pl": "Polski",
}

DEFAULT_LANGUAGE = "en"

CONFIG_PATH = os.path.expanduser("~/.config/pisafe-gui/config.json")

TRANSLATIONS = {
    "en": {
        "window_title": "PiSafe GUI",
        "subtitle": "Graphical interface for the pisafe tool",
        "btn_refresh_disks": "⟳  Refresh disks",
        "tab_flash": "⚡  Flash image → SD",
        "tab_backup": "💾  Backup SD → image",
        "tab_list": "📋  Disk list",
        "grp_logs": "Logs",
        "btn_stop": "■  Stop",
        "btn_clear_logs": "Clear logs",

        "grp_flash_image": "Image file (.img / .iso / .zip / .xz / .gz / .zst)",
        "flash_img_placeholder": "Select or type the path to the image file…",
        "btn_browse": "📂  Browse",
        "grp_flash_target": "Target disk (SD / USB)",
        "label_disk": "Disk:",
        "flash_warning": "⚠️  Warning: the selected disk's contents will be PERMANENTLY overwritten!",
        "btn_flash": "⚡  Flash image to disk",

        "grp_backup_source": "Source disk (SD to back up)",
        "grp_backup_output": "Output image file",
        "label_dir": "Directory:",
        "btn_dir": "📂  Folder",
        "label_filename": "File name:",
        "label_compression": "Compression:",
        "btn_backup": "💾  Create disk image",

        "btn_refresh_list": "🔄  Refresh disk list",

        "dlg_choose_image_title": "Choose image",
        "dlg_choose_image_filter": "Images (*.img *.iso *.zip *.xz *.gz *.zst);;All files (*)",
        "dlg_choose_dir_title": "Choose target directory",

        "warn_system_disks": "Warning: could not check system disks: {error}",
        "hidden_system_disks": "Hidden system disks: {disks}",
        "hidden_non_removable_disks": "Hidden non-USB/SD disks: {disks}",
        "no_disks_available": "(no disks available)",
        "lsblk_error": "lsblk error: {error}",
        "disks_refreshed": "Disk list refreshed.\n",
        "list_error": "Error: {error}",

        "error_title": "Error",
        "error_invalid_image_path": "Provide a valid path to the image file.",
        "error_select_target_disk": "Select a target disk.",
        "error_select_source_disk": "Select a source disk.",
        "error_filename_required": "Provide an output file name.",

        "confirm_flash_title": "Confirm operation",
        "confirm_flash_text": (
            "WARNING! All data on {dev} will be PERMANENTLY erased!\n\n"
            "Image: {img}\nDisk: {dev}\n\nDo you really want to continue?"
        ),
        "confirm_backup_title": "Confirm backup",
        "confirm_backup_text": (
            "Creating image:\n  Disk: {dev}\n  File: {out_path}\n\nContinue?"
        ),

        "busy_title": "Busy",
        "busy_text": "Another task is running. Wait or stop it first.",
        "task_stopped": "\n⛔ Task stopped by the user.\n",

        "worker_success": "Completed successfully.",
        "worker_error": "Error (code {code}).",

        "pisafe_missing_title": "pisafe not found",
        "pisafe_missing_text": (
            "The 'pisafe' tool is not installed.\n\n"
            "Install it with:\n"
            "wget https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O pisafe\n"
            "bash pisafe install"
        ),

        "language_label": "Language:",
        "restart_required_title": "Restart required",
        "restart_required_text": "The application will now restart to apply the new language.",
    },
    "pl": {
        "window_title": "PiSafe GUI",
        "subtitle": "Graficzny interfejs dla narzędzia pisafe",
        "btn_refresh_disks": "⟳  Odśwież dyski",
        "tab_flash": "⚡  Flash obrazu → SD",
        "tab_backup": "💾  Backup SD → obraz",
        "tab_list": "📋  Lista dysków",
        "grp_logs": "Logi",
        "btn_stop": "■  Zatrzymaj",
        "btn_clear_logs": "Wyczyść logi",

        "grp_flash_image": "Plik obrazu (.img / .iso / .zip / .xz / .gz / .zst)",
        "flash_img_placeholder": "Wybierz lub wpisz ścieżkę do pliku obrazu…",
        "btn_browse": "📂  Przeglądaj",
        "grp_flash_target": "Dysk docelowy (SD / USB)",
        "label_disk": "Dysk:",
        "flash_warning": "⚠️  Uwaga: zawartość wybranego dysku zostanie TRWALE nadpisana!",
        "btn_flash": "⚡  Flash obrazu na dysk",

        "grp_backup_source": "Dysk źródłowy (SD do backupu)",
        "grp_backup_output": "Plik wyjściowy obrazu",
        "label_dir": "Katalog:",
        "btn_dir": "📂  Folder",
        "label_filename": "Nazwa pliku:",
        "label_compression": "Kompresja:",
        "btn_backup": "💾  Utwórz obraz dysku",

        "btn_refresh_list": "🔄  Odśwież listę dysków",

        "dlg_choose_image_title": "Wybierz obraz",
        "dlg_choose_image_filter": "Obrazy (*.img *.iso *.zip *.xz *.gz *.zst);;Wszystkie (*)",
        "dlg_choose_dir_title": "Wybierz katalog docelowy",

        "warn_system_disks": "Ostrzeżenie: nie można sprawdzić dysków systemowych: {error}",
        "hidden_system_disks": "Ukryto dyski systemowe: {disks}",
        "hidden_non_removable_disks": "Ukryto dyski niebędące USB/SD: {disks}",
        "no_disks_available": "(brak dostępnych dysków)",
        "lsblk_error": "Błąd lsblk: {error}",
        "disks_refreshed": "Odświeżono listę dysków.\n",
        "list_error": "Błąd: {error}",

        "error_title": "Błąd",
        "error_invalid_image_path": "Podaj prawidłową ścieżkę do pliku obrazu.",
        "error_select_target_disk": "Wybierz dysk docelowy.",
        "error_select_source_disk": "Wybierz dysk źródłowy.",
        "error_filename_required": "Podaj nazwę pliku wyjściowego.",

        "confirm_flash_title": "Potwierdź operację",
        "confirm_flash_text": (
            "UWAGA! Wszystkie dane na {dev} zostaną TRWALE usunięte!\n\n"
            "Obraz: {img}\nDysk: {dev}\n\nCzy na pewno chcesz kontynuować?"
        ),
        "confirm_backup_title": "Potwierdź backup",
        "confirm_backup_text": (
            "Tworzenie obrazu:\n  Dysk: {dev}\n  Plik: {out_path}\n\nKontynuować?"
        ),

        "busy_title": "Zajęty",
        "busy_text": "Trwa inne zadanie. Poczekaj lub je zatrzymaj.",
        "task_stopped": "\n⛔ Zadanie przerwane przez użytkownika.\n",

        "worker_success": "Zakończono pomyślnie.",
        "worker_error": "Błąd (kod {code}).",

        "pisafe_missing_title": "pisafe nie znalezione",
        "pisafe_missing_text": (
            "Narzędzie 'pisafe' nie jest zainstalowane.\n\n"
            "Zainstaluj je poleceniem:\n"
            "wget https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O pisafe\n"
            "bash pisafe install"
        ),

        "language_label": "Język:",
        "restart_required_title": "Wymagany restart",
        "restart_required_text": "Aplikacja zostanie ponownie uruchomiona, aby zastosować nowy język.",
    },
}

_current_language = DEFAULT_LANGUAGE


def set_language(code):
    global _current_language
    _current_language = code if code in TRANSLATIONS else DEFAULT_LANGUAGE


def get_language():
    return _current_language


def tr(key, **kwargs):
    text = TRANSLATIONS.get(_current_language, {}).get(key)
    if text is None:
        text = TRANSLATIONS[DEFAULT_LANGUAGE].get(key, key)
    return text.format(**kwargs) if kwargs else text


def get_saved_language():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            lang = data.get("language")
            return lang if lang in TRANSLATIONS else None
    except (OSError, json.JSONDecodeError):
        return None


def save_language(code):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"language": code}, f, indent=2)
