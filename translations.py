"""Translation strings and language persistence for PiSafe GUI.

Add a new language by adding a new entry to LANGUAGES and a matching
dictionary (with the same keys as the "en" dictionary) to TRANSLATIONS.
"""

import json
import os

LANGUAGES = {
    "en": "English",
    "pl": "Polski",
    "es": "Español",
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
        "btn_result_ok": "✓  Done",
        "btn_result_fail": "✗  Failed",
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
        "finalizing_write": "⏳ Data sent, finalizing write to disk (can take a while on slow USB/SD media)...",

        "worker_success": "Completed successfully.",
        "worker_error": "Error (code {code}).",

        "pisafe_missing_title": "pisafe not found",
        "pisafe_missing_text": (
            "The 'pisafe' tool is not installed.\n\n"
            "Install it with:\n"
            "wget https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O pisafe\n"
            "bash pisafe install"
        ),

        "pkexec_missing_title": "pkexec not found",
        "pkexec_missing_text": (
            "The 'pkexec' tool (PolicyKit) is not installed. It's required to run "
            "flash/backup operations with administrator rights.\n\n"
            "Install it with:\n"
            "sudo apt-get install policykit-1"
        ),

        "language_label": "Language:",
        "restart_required_title": "Restart required",
        "restart_required_text": "The application will now restart to apply the new language.",

        "tab_versions": "🗂️  Versions",
        "grp_projects": "Projects",
        "grp_images": "Images",
        "btn_new_project": "+  New project",
        "btn_delete_project": "Delete project",
        "btn_refresh_images": "⟳  Refresh",
        "btn_open_folder": "📂  Open folder",
        "btn_delete_entry": "Delete entry",
        "col_version": "Version",
        "col_file": "File",
        "col_date": "Date",
        "col_size": "Size",
        "col_source_disk": "Source disk",
        "col_notes": "Notes",

        "grp_backup_project": "Project (optional)",
        "project_combo_none": "— no project —",

        "new_project_title": "New project",
        "new_project_name_label": "Project name:",
        "new_project_folder_title": "Choose the project's base folder",
        "project_name_exists": "A project with this name already exists.",

        "version_dialog_title": "New image version",
        "version_dialog_project_label": "Project: {name}",
        "version_dialog_label_field": "Version label:",
        "version_dialog_notes_field": "Notes (optional):",

        "confirm_delete_project_title": "Delete project",
        "confirm_delete_project_text": (
            "Delete project '{name}' and all its version entries from the database?\n\n"
            "Image files on disk will NOT be deleted."
        ),
        "confirm_delete_image_title": "Delete entry",
        "confirm_delete_image_text": "Delete this version entry?",
        "btn_delete_entry_only": "Delete entry only",
        "btn_delete_entry_and_file": "Delete entry and file",

        "no_project_selected": "Select a project first.",
        "no_image_selected": "Select an image entry first.",
        "project_folder_missing": "This project's folder no longer exists: {folder}",
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
        "btn_result_ok": "✓  Gotowe",
        "btn_result_fail": "✗  Błąd",
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
        "finalizing_write": "⏳ Dane wysłane, finalizowanie zapisu na dysk (na wolnym USB/SD może to potrwać)...",

        "worker_success": "Zakończono pomyślnie.",
        "worker_error": "Błąd (kod {code}).",

        "pisafe_missing_title": "pisafe nie znalezione",
        "pisafe_missing_text": (
            "Narzędzie 'pisafe' nie jest zainstalowane.\n\n"
            "Zainstaluj je poleceniem:\n"
            "wget https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O pisafe\n"
            "bash pisafe install"
        ),

        "pkexec_missing_title": "Brak pkexec",
        "pkexec_missing_text": (
            "Narzędzie 'pkexec' (PolicyKit) nie jest zainstalowane. Jest potrzebne do "
            "wykonywania operacji flash/backup z prawami administratora.\n\n"
            "Zainstaluj je poleceniem:\n"
            "sudo apt-get install policykit-1"
        ),

        "language_label": "Język:",
        "restart_required_title": "Wymagany restart",
        "restart_required_text": "Aplikacja zostanie ponownie uruchomiona, aby zastosować nowy język.",

        "tab_versions": "🗂️  Wersje",
        "grp_projects": "Projekty",
        "grp_images": "Obrazy",
        "btn_new_project": "+  Nowy projekt",
        "btn_delete_project": "Usuń projekt",
        "btn_refresh_images": "⟳  Odśwież",
        "btn_open_folder": "📂  Otwórz folder",
        "btn_delete_entry": "Usuń wpis",
        "col_version": "Wersja",
        "col_file": "Plik",
        "col_date": "Data",
        "col_size": "Rozmiar",
        "col_source_disk": "Dysk źródłowy",
        "col_notes": "Notatki",

        "grp_backup_project": "Projekt (opcjonalnie)",
        "project_combo_none": "— bez projektu —",

        "new_project_title": "Nowy projekt",
        "new_project_name_label": "Nazwa projektu:",
        "new_project_folder_title": "Wybierz folder bazowy projektu",
        "project_name_exists": "Projekt o tej nazwie już istnieje.",

        "version_dialog_title": "Nowa wersja obrazu",
        "version_dialog_project_label": "Projekt: {name}",
        "version_dialog_label_field": "Etykieta wersji:",
        "version_dialog_notes_field": "Notatki (opcjonalnie):",

        "confirm_delete_project_title": "Usuń projekt",
        "confirm_delete_project_text": (
            "Usunąć projekt '{name}' i wszystkie jego wpisy wersji z bazy?\n\n"
            "Pliki obrazów na dysku NIE zostaną usunięte."
        ),
        "confirm_delete_image_title": "Usuń wpis",
        "confirm_delete_image_text": "Usunąć ten wpis wersji?",
        "btn_delete_entry_only": "Usuń tylko wpis",
        "btn_delete_entry_and_file": "Usuń wpis i plik",

        "no_project_selected": "Najpierw wybierz projekt.",
        "no_image_selected": "Najpierw wybierz wpis obrazu.",
        "project_folder_missing": "Folder tego projektu już nie istnieje: {folder}",
    },
    "es": {
        "window_title": "PiSafe GUI",
        "subtitle": "Interfaz gráfica para la herramienta pisafe",
        "btn_refresh_disks": "⟳  Actualizar discos",
        "tab_flash": "⚡  Grabar imagen → SD",
        "tab_backup": "💾  Backup SD → imagen",
        "tab_list": "📋  Lista de discos",
        "grp_logs": "Registros",
        "btn_stop": "■  Detener",
        "btn_result_ok": "✓  Hecho",
        "btn_result_fail": "✗  Error",
        "btn_clear_logs": "Borrar registros",

        "grp_flash_image": "Archivo de imagen (.img / .iso / .zip / .xz / .gz / .zst)",
        "flash_img_placeholder": "Selecciona o escribe la ruta del archivo de imagen…",
        "btn_browse": "📂  Examinar",
        "grp_flash_target": "Disco de destino (SD / USB)",
        "label_disk": "Disco:",
        "flash_warning": "⚠️  Advertencia: ¡el contenido del disco seleccionado se sobrescribirá PERMANENTEMENTE!",
        "btn_flash": "⚡  Grabar imagen en el disco",

        "grp_backup_source": "Disco de origen (SD a respaldar)",
        "grp_backup_output": "Archivo de imagen de salida",
        "label_dir": "Carpeta:",
        "btn_dir": "📂  Carpeta",
        "label_filename": "Nombre de archivo:",
        "label_compression": "Compresión:",
        "btn_backup": "💾  Crear imagen de disco",

        "btn_refresh_list": "🔄  Actualizar lista de discos",

        "dlg_choose_image_title": "Elegir imagen",
        "dlg_choose_image_filter": "Imágenes (*.img *.iso *.zip *.xz *.gz *.zst);;Todos los archivos (*)",
        "dlg_choose_dir_title": "Elegir carpeta de destino",

        "warn_system_disks": "Advertencia: no se pudieron comprobar los discos del sistema: {error}",
        "hidden_system_disks": "Discos del sistema ocultos: {disks}",
        "hidden_non_removable_disks": "Discos no USB/SD ocultos: {disks}",
        "no_disks_available": "(no hay discos disponibles)",
        "lsblk_error": "Error de lsblk: {error}",
        "disks_refreshed": "Lista de discos actualizada.\n",
        "list_error": "Error: {error}",

        "error_title": "Error",
        "error_invalid_image_path": "Indica una ruta válida al archivo de imagen.",
        "error_select_target_disk": "Selecciona un disco de destino.",
        "error_select_source_disk": "Selecciona un disco de origen.",
        "error_filename_required": "Indica un nombre de archivo de salida.",

        "confirm_flash_title": "Confirmar operación",
        "confirm_flash_text": (
            "¡ADVERTENCIA! ¡Todos los datos en {dev} se borrarán PERMANENTEMENTE!\n\n"
            "Imagen: {img}\nDisco: {dev}\n\n¿Realmente deseas continuar?"
        ),
        "confirm_backup_title": "Confirmar backup",
        "confirm_backup_text": (
            "Creando imagen:\n  Disco: {dev}\n  Archivo: {out_path}\n\n¿Continuar?"
        ),

        "busy_title": "Ocupado",
        "busy_text": "Hay otra tarea en curso. Espera o detenla primero.",
        "task_stopped": "\n⛔ Tarea detenida por el usuario.\n",
        "finalizing_write": "⏳ Datos enviados, finalizando la escritura en el disco (puede tardar en medios USB/SD lentos)...",

        "worker_success": "Completado correctamente.",
        "worker_error": "Error (código {code}).",

        "pisafe_missing_title": "pisafe no encontrado",
        "pisafe_missing_text": (
            "La herramienta 'pisafe' no está instalada.\n\n"
            "Instálala con:\n"
            "wget https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O pisafe\n"
            "bash pisafe install"
        ),

        "pkexec_missing_title": "pkexec no encontrado",
        "pkexec_missing_text": (
            "La herramienta 'pkexec' (PolicyKit) no está instalada. Es necesaria para "
            "ejecutar operaciones de grabado/backup con permisos de administrador.\n\n"
            "Instálala con:\n"
            "sudo apt-get install policykit-1"
        ),

        "language_label": "Idioma:",
        "restart_required_title": "Reinicio necesario",
        "restart_required_text": "La aplicación se reiniciará ahora para aplicar el nuevo idioma.",

        "tab_versions": "🗂️  Versiones",
        "grp_projects": "Proyectos",
        "grp_images": "Imágenes",
        "btn_new_project": "+  Nuevo proyecto",
        "btn_delete_project": "Eliminar proyecto",
        "btn_refresh_images": "⟳  Actualizar",
        "btn_open_folder": "📂  Abrir carpeta",
        "btn_delete_entry": "Eliminar entrada",
        "col_version": "Versión",
        "col_file": "Archivo",
        "col_date": "Fecha",
        "col_size": "Tamaño",
        "col_source_disk": "Disco de origen",
        "col_notes": "Notas",

        "grp_backup_project": "Proyecto (opcional)",
        "project_combo_none": "— sin proyecto —",

        "new_project_title": "Nuevo proyecto",
        "new_project_name_label": "Nombre del proyecto:",
        "new_project_folder_title": "Elige la carpeta base del proyecto",
        "project_name_exists": "Ya existe un proyecto con este nombre.",

        "version_dialog_title": "Nueva versión de imagen",
        "version_dialog_project_label": "Proyecto: {name}",
        "version_dialog_label_field": "Etiqueta de versión:",
        "version_dialog_notes_field": "Notas (opcional):",

        "confirm_delete_project_title": "Eliminar proyecto",
        "confirm_delete_project_text": (
            "¿Eliminar el proyecto '{name}' y todas sus entradas de versión de la base de datos?\n\n"
            "Los archivos de imagen en el disco NO se eliminarán."
        ),
        "confirm_delete_image_title": "Eliminar entrada",
        "confirm_delete_image_text": "¿Eliminar esta entrada de versión?",
        "btn_delete_entry_only": "Eliminar solo la entrada",
        "btn_delete_entry_and_file": "Eliminar entrada y archivo",

        "no_project_selected": "Selecciona primero un proyecto.",
        "no_image_selected": "Selecciona primero una entrada de imagen.",
        "project_folder_missing": "La carpeta de este proyecto ya no existe: {folder}",
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
