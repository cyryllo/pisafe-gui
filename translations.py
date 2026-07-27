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
    "pt": "Português",
    "it": "Italiano",
    "de": "Deutsch",
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
        "btn_check_image": "🔎  Check image",
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

        "grp_disk_tools": "Disk tools",
        "btn_erase": "⚠  Format disk",
        "label_format": "Format:",
        "erase_warning": "⚠️  Warning: formatting will PERMANENTLY erase all data on the selected disk!",
        "confirm_erase_title": "Confirm format",
        "confirm_erase_text": (
            "WARNING! All data on {dev} will be PERMANENTLY erased!\n\n"
            "Disk: {dev}\nFormat: {fmt}\n\nDo you really want to continue?"
        ),

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
        "error_duplicate_targets": "The same disk is selected more than once. Pick a different disk for each row.",

        "confirm_flash_title": "Confirm operation",
        "confirm_flash_text": (
            "WARNING! All data on {dev} will be PERMANENTLY erased!\n\n"
            "Image: {img}\nDisk: {dev}\n\nDo you really want to continue?"
        ),
        "confirm_flash_text_multi": (
            "WARNING! All data on these disks will be PERMANENTLY erased!\n\n"
            "Image: {img}\nDisks: {devices}\n\nDo you really want to continue?"
        ),
        "confirm_backup_title": "Confirm backup",
        "confirm_backup_text": (
            "Creating image:\n  Disk: {dev}\n  File: {out_path}\n\nContinue?"
        ),

        "busy_title": "Busy",
        "busy_text": "Another task is running. Wait or stop it first.",
        "task_stopped": "\n⛔ Task stopped by the user.\n",
        "finalizing_write": "⏳ Data sent, finalizing write to disk (can take a while on slow USB/SD media)...",
        "finalizing_checksum": "⏳ Data read, finalizing checksum calculation...",

        "verify_checkbox_label": "Verify write after flashing (.img/.iso only)",
        "verify_unsupported_format": "ℹ️ Verification only supports .img/.iso — skipped for this format.\n",
        "verify_unsupported_multi": "ℹ️ Verification only works with a single target disk — skipped for this multi-disk flash.\n",
        "verify_running": "🔍 Verifying write (computing SHA256 checksums, this can take a while)...\n",
        "verify_match_full": "Image written and verified — checksum matches.",
        "verify_mismatch_full": "Image written, but verification FAILED — checksum mismatch!",
        "verify_error_full": "Could not verify the write (error while computing checksums).",

        "btn_add_target": "+  Add disk",
        "btn_stop_multi": "■  Stop all",
        "grp_multi_progress": "Flashing progress",
        "multi_flash_started": "🚀 Started flashing {n} disks in parallel: {devices}",
        "multi_flash_summary": "Done: {ok} succeeded, {fail} failed.",

        "checksum_paste_title": "Paste checksum",
        "checksum_paste_label": "No checksum file found next to this image.\nPaste the expected SHA256 or MD5 checksum (e.g. from the download page):",
        "error_invalid_checksum": "The pasted text isn't a valid SHA256 (64 hex chars) or MD5 (32 hex chars) checksum.",
        "checksum_running": "🔍 Checking image ({algo} checksum, this can take a while)...\n",
        "checksum_match_full": "Image is valid — checksum matches.",
        "checksum_mismatch_full": "Image is CORRUPTED or invalid — checksum does NOT match!",
        "checksum_error_full": "Could not check the image's checksum (error while computing it).",

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
        "btn_check_image": "🔎  Sprawdź obraz",
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

        "grp_disk_tools": "Narzędzia dysku",
        "btn_erase": "⚠  Formatuj dysk",
        "label_format": "Format:",
        "erase_warning": "⚠️  Uwaga: formatowanie TRWALE usunie wszystkie dane na wybranym dysku!",
        "confirm_erase_title": "Potwierdź formatowanie",
        "confirm_erase_text": (
            "UWAGA! Wszystkie dane na {dev} zostaną TRWALE usunięte!\n\n"
            "Dysk: {dev}\nFormat: {fmt}\n\nCzy na pewno chcesz kontynuować?"
        ),

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
        "error_duplicate_targets": "Ten sam dysk wybrano więcej niż raz. Wybierz różne dyski dla każdej pozycji.",

        "confirm_flash_title": "Potwierdź operację",
        "confirm_flash_text": (
            "UWAGA! Wszystkie dane na {dev} zostaną TRWALE usunięte!\n\n"
            "Obraz: {img}\nDysk: {dev}\n\nCzy na pewno chcesz kontynuować?"
        ),
        "confirm_flash_text_multi": (
            "UWAGA! Wszystkie dane na tych dyskach zostaną TRWALE usunięte!\n\n"
            "Obraz: {img}\nDyski: {devices}\n\nCzy na pewno chcesz kontynuować?"
        ),
        "confirm_backup_title": "Potwierdź backup",
        "confirm_backup_text": (
            "Tworzenie obrazu:\n  Dysk: {dev}\n  Plik: {out_path}\n\nKontynuować?"
        ),

        "busy_title": "Zajęty",
        "busy_text": "Trwa inne zadanie. Poczekaj lub je zatrzymaj.",
        "task_stopped": "\n⛔ Zadanie przerwane przez użytkownika.\n",
        "finalizing_write": "⏳ Dane wysłane, finalizowanie zapisu na dysk (na wolnym USB/SD może to potrwać)...",
        "finalizing_checksum": "⏳ Dane odczytane, finalizowanie liczenia sumy kontrolnej...",

        "verify_checkbox_label": "Zweryfikuj zapis po flashowaniu (tylko .img/.iso)",
        "verify_unsupported_format": "ℹ️ Weryfikacja dostępna tylko dla .img/.iso — pominięto dla tego formatu.\n",
        "verify_unsupported_multi": "ℹ️ Weryfikacja działa tylko dla jednego dysku docelowego — pominięto dla flashowania wielu dysków.\n",
        "verify_running": "🔍 Weryfikowanie zapisu (liczenie sum kontrolnych SHA256, to może chwilę potrwać)...\n",
        "verify_match_full": "Obraz zapisany i zweryfikowany — suma kontrolna się zgadza.",
        "verify_mismatch_full": "Obraz zapisany, ale weryfikacja NIE powiodła się — suma kontrolna się różni!",
        "verify_error_full": "Nie udało się zweryfikować zapisu (błąd podczas liczenia sum kontrolnych).",

        "btn_add_target": "+  Dodaj dysk",
        "btn_stop_multi": "■  Zatrzymaj wszystkie",
        "grp_multi_progress": "Postęp wgrywania",
        "multi_flash_started": "🚀 Rozpoczęto flashowanie {n} dysków równolegle: {devices}",
        "multi_flash_summary": "Zakończono: {ok} udanych, {fail} nieudanych.",

        "checksum_paste_title": "Wklej sumę kontrolną",
        "checksum_paste_label": "Nie znaleziono pliku z sumą kontrolną w tym folderze.\nWklej oczekiwaną sumę SHA256 lub MD5 (np. ze strony pobierania):",
        "error_invalid_checksum": "Wklejony tekst nie jest poprawną sumą SHA256 (64 znaki hex) ani MD5 (32 znaki hex).",
        "checksum_running": "🔍 Sprawdzanie obrazu (suma {algo}, to może chwilę potrwać)...\n",
        "checksum_match_full": "Obraz jest poprawny — suma kontrolna się zgadza.",
        "checksum_mismatch_full": "Obraz USZKODZONY lub niepoprawny — suma kontrolna się NIE zgadza!",
        "checksum_error_full": "Nie udało się sprawdzić sumy kontrolnej obrazu (błąd podczas liczenia).",

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
        "btn_check_image": "🔎  Comprobar imagen",
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

        "grp_disk_tools": "Herramientas de disco",
        "btn_erase": "⚠  Formatear disco",
        "label_format": "Formato:",
        "erase_warning": "⚠️  ¡Advertencia! Formatear borrará PERMANENTEMENTE todos los datos del disco seleccionado.",
        "confirm_erase_title": "Confirmar formateo",
        "confirm_erase_text": (
            "¡ADVERTENCIA! ¡Todos los datos en {dev} se borrarán PERMANENTEMENTE!\n\n"
            "Disco: {dev}\nFormato: {fmt}\n\n¿Realmente deseas continuar?"
        ),

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
        "error_duplicate_targets": "El mismo disco está seleccionado más de una vez. Elige un disco distinto en cada fila.",

        "confirm_flash_title": "Confirmar operación",
        "confirm_flash_text": (
            "¡ADVERTENCIA! ¡Todos los datos en {dev} se borrarán PERMANENTEMENTE!\n\n"
            "Imagen: {img}\nDisco: {dev}\n\n¿Realmente deseas continuar?"
        ),
        "confirm_flash_text_multi": (
            "¡ADVERTENCIA! ¡Todos los datos en estos discos se borrarán PERMANENTEMENTE!\n\n"
            "Imagen: {img}\nDiscos: {devices}\n\n¿Realmente deseas continuar?"
        ),
        "confirm_backup_title": "Confirmar backup",
        "confirm_backup_text": (
            "Creando imagen:\n  Disco: {dev}\n  Archivo: {out_path}\n\n¿Continuar?"
        ),

        "busy_title": "Ocupado",
        "busy_text": "Hay otra tarea en curso. Espera o detenla primero.",
        "task_stopped": "\n⛔ Tarea detenida por el usuario.\n",
        "finalizing_write": "⏳ Datos enviados, finalizando la escritura en el disco (puede tardar en medios USB/SD lentos)...",
        "finalizing_checksum": "⏳ Datos leídos, finalizando el cálculo de la suma de comprobación...",

        "verify_checkbox_label": "Verificar escritura tras flashear (solo .img/.iso)",
        "verify_unsupported_format": "ℹ️ La verificación solo admite .img/.iso — omitida para este formato.\n",
        "verify_unsupported_multi": "ℹ️ La verificación solo funciona con un único disco de destino — omitida para este flasheo múltiple.\n",
        "verify_running": "🔍 Verificando la escritura (calculando sumas SHA256, puede tardar un poco)...\n",
        "verify_match_full": "Imagen escrita y verificada — la suma de comprobación coincide.",
        "verify_mismatch_full": "Imagen escrita, pero la verificación FALLÓ — la suma de comprobación no coincide.",
        "verify_error_full": "No se pudo verificar la escritura (error al calcular las sumas de comprobación).",

        "btn_add_target": "+  Añadir disco",
        "btn_stop_multi": "■  Detener todo",
        "grp_multi_progress": "Progreso de escritura",
        "multi_flash_started": "🚀 Iniciado el flasheo de {n} discos en paralelo: {devices}",
        "multi_flash_summary": "Finalizado: {ok} con éxito, {fail} fallidos.",

        "checksum_paste_title": "Pegar suma de comprobación",
        "checksum_paste_label": "No se encontró un archivo de suma de comprobación junto a esta imagen.\nPega la suma SHA256 o MD5 esperada (por ejemplo, de la página de descarga):",
        "error_invalid_checksum": "El texto pegado no es una suma SHA256 (64 caracteres hex) ni MD5 (32 caracteres hex) válida.",
        "checksum_running": "🔍 Comprobando imagen (suma {algo}, puede tardar un poco)...\n",
        "checksum_match_full": "La imagen es válida — la suma de comprobación coincide.",
        "checksum_mismatch_full": "Imagen CORRUPTA o inválida — ¡la suma de comprobación NO coincide!",
        "checksum_error_full": "No se pudo comprobar la suma de la imagen (error al calcularla).",

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
    "pt": {
        "window_title": "PiSafe GUI",
        "subtitle": "Interface gráfica para a ferramenta pisafe",
        "btn_refresh_disks": "⟳  Atualizar discos",
        "tab_flash": "⚡  Gravar imagem → SD",
        "tab_backup": "💾  Backup SD → imagem",
        "tab_list": "📋  Lista de discos",
        "grp_logs": "Registos",
        "btn_stop": "■  Parar",
        "btn_result_ok": "✓  Concluído",
        "btn_result_fail": "✗  Falhou",
        "btn_clear_logs": "Limpar registos",

        "grp_flash_image": "Ficheiro de imagem (.img / .iso / .zip / .xz / .gz / .zst)",
        "flash_img_placeholder": "Selecione ou escreva o caminho do ficheiro de imagem…",
        "btn_browse": "📂  Procurar",
        "btn_check_image": "🔎  Verificar imagem",
        "grp_flash_target": "Disco de destino (SD / USB)",
        "label_disk": "Disco:",
        "flash_warning": "⚠️  Aviso: o conteúdo do disco selecionado será PERMANENTEMENTE substituído!",
        "btn_flash": "⚡  Gravar imagem no disco",

        "grp_backup_source": "Disco de origem (SD a copiar)",
        "grp_backup_output": "Ficheiro de imagem de saída",
        "label_dir": "Pasta:",
        "btn_dir": "📂  Pasta",
        "label_filename": "Nome do ficheiro:",
        "label_compression": "Compressão:",
        "btn_backup": "💾  Criar imagem do disco",

        "btn_refresh_list": "🔄  Atualizar lista de discos",

        "grp_disk_tools": "Ferramentas de disco",
        "btn_erase": "⚠  Formatar disco",
        "label_format": "Formato:",
        "erase_warning": "⚠️  Aviso: a formatação irá apagar PERMANENTEMENTE todos os dados do disco selecionado!",
        "confirm_erase_title": "Confirmar formatação",
        "confirm_erase_text": (
            "AVISO! Todos os dados em {dev} serão PERMANENTEMENTE apagados!\n\n"
            "Disco: {dev}\nFormato: {fmt}\n\nDeseja mesmo continuar?"
        ),

        "dlg_choose_image_title": "Escolher imagem",
        "dlg_choose_image_filter": "Imagens (*.img *.iso *.zip *.xz *.gz *.zst);;Todos os ficheiros (*)",
        "dlg_choose_dir_title": "Escolher pasta de destino",

        "warn_system_disks": "Aviso: não foi possível verificar os discos do sistema: {error}",
        "hidden_system_disks": "Discos do sistema ocultos: {disks}",
        "hidden_non_removable_disks": "Discos não USB/SD ocultos: {disks}",
        "no_disks_available": "(nenhum disco disponível)",
        "lsblk_error": "Erro do lsblk: {error}",
        "disks_refreshed": "Lista de discos atualizada.\n",
        "list_error": "Erro: {error}",

        "error_title": "Erro",
        "error_invalid_image_path": "Indique um caminho válido para o ficheiro de imagem.",
        "error_select_target_disk": "Selecione um disco de destino.",
        "error_select_source_disk": "Selecione um disco de origem.",
        "error_filename_required": "Indique um nome para o ficheiro de saída.",
        "error_duplicate_targets": "O mesmo disco foi selecionado mais de uma vez. Escolha um disco diferente para cada linha.",

        "confirm_flash_title": "Confirmar operação",
        "confirm_flash_text": (
            "AVISO! Todos os dados em {dev} serão PERMANENTEMENTE apagados!\n\n"
            "Imagem: {img}\nDisco: {dev}\n\nDeseja mesmo continuar?"
        ),
        "confirm_flash_text_multi": (
            "AVISO! Todos os dados nestes discos serão PERMANENTEMENTE apagados!\n\n"
            "Imagem: {img}\nDiscos: {devices}\n\nDeseja mesmo continuar?"
        ),
        "confirm_backup_title": "Confirmar backup",
        "confirm_backup_text": (
            "A criar imagem:\n  Disco: {dev}\n  Ficheiro: {out_path}\n\nContinuar?"
        ),

        "busy_title": "Ocupado",
        "busy_text": "Outra tarefa está em execução. Aguarde ou pare-a primeiro.",
        "task_stopped": "\n⛔ Tarefa interrompida pelo utilizador.\n",
        "finalizing_write": "⏳ Dados enviados, a finalizar a escrita no disco (pode demorar em suportes USB/SD lentos)...",
        "finalizing_checksum": "⏳ Dados lidos, a finalizar o cálculo da soma de verificação...",

        "verify_checkbox_label": "Verificar escrita após gravar (apenas .img/.iso)",
        "verify_unsupported_format": "ℹ️ A verificação só suporta .img/.iso — ignorada para este formato.\n",
        "verify_unsupported_multi": "ℹ️ A verificação só funciona com um único disco de destino — ignorada para esta gravação múltipla.\n",
        "verify_running": "🔍 A verificar a escrita (a calcular somas SHA256, isto pode demorar um pouco)...\n",
        "verify_match_full": "Imagem gravada e verificada — a soma de verificação coincide.",
        "verify_mismatch_full": "Imagem gravada, mas a verificação FALHOU — a soma de verificação não coincide!",
        "verify_error_full": "Não foi possível verificar a escrita (erro ao calcular as somas de verificação).",

        "btn_add_target": "+  Adicionar disco",
        "btn_stop_multi": "■  Parar tudo",
        "grp_multi_progress": "Progresso da gravação",
        "multi_flash_started": "🚀 Iniciada a gravação de {n} discos em paralelo: {devices}",
        "multi_flash_summary": "Concluído: {ok} com sucesso, {fail} com falhas.",

        "checksum_paste_title": "Colar soma de verificação",
        "checksum_paste_label": "Não foi encontrado nenhum ficheiro de soma de verificação junto desta imagem.\nCole a soma SHA256 ou MD5 esperada (por exemplo, da página de download):",
        "error_invalid_checksum": "O texto colado não é uma soma SHA256 (64 carateres hex) nem MD5 (32 carateres hex) válida.",
        "checksum_running": "🔍 A verificar a imagem (soma {algo}, isto pode demorar um pouco)...\n",
        "checksum_match_full": "A imagem é válida — a soma de verificação coincide.",
        "checksum_mismatch_full": "Imagem CORROMPIDA ou inválida — a soma de verificação NÃO coincide!",
        "checksum_error_full": "Não foi possível verificar a soma da imagem (erro ao calculá-la).",

        "worker_success": "Concluído com sucesso.",
        "worker_error": "Erro (código {code}).",

        "pisafe_missing_title": "pisafe não encontrado",
        "pisafe_missing_text": (
            "A ferramenta 'pisafe' não está instalada.\n\n"
            "Instale-a com:\n"
            "wget https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O pisafe\n"
            "bash pisafe install"
        ),

        "pkexec_missing_title": "pkexec não encontrado",
        "pkexec_missing_text": (
            "A ferramenta 'pkexec' (PolicyKit) não está instalada. É necessária para "
            "executar operações de gravação/backup com privilégios de administrador.\n\n"
            "Instale-a com:\n"
            "sudo apt-get install policykit-1"
        ),

        "language_label": "Idioma:",
        "restart_required_title": "Reinício necessário",
        "restart_required_text": "A aplicação irá reiniciar agora para aplicar o novo idioma.",

        "tab_versions": "🗂️  Versões",
        "grp_projects": "Projetos",
        "grp_images": "Imagens",
        "btn_new_project": "+  Novo projeto",
        "btn_delete_project": "Eliminar projeto",
        "btn_refresh_images": "⟳  Atualizar",
        "btn_open_folder": "📂  Abrir pasta",
        "btn_delete_entry": "Eliminar entrada",
        "col_version": "Versão",
        "col_file": "Ficheiro",
        "col_date": "Data",
        "col_size": "Tamanho",
        "col_source_disk": "Disco de origem",
        "col_notes": "Notas",

        "grp_backup_project": "Projeto (opcional)",
        "project_combo_none": "— sem projeto —",

        "new_project_title": "Novo projeto",
        "new_project_name_label": "Nome do projeto:",
        "new_project_folder_title": "Escolha a pasta base do projeto",
        "project_name_exists": "Já existe um projeto com este nome.",

        "version_dialog_title": "Nova versão de imagem",
        "version_dialog_project_label": "Projeto: {name}",
        "version_dialog_label_field": "Etiqueta da versão:",
        "version_dialog_notes_field": "Notas (opcional):",

        "confirm_delete_project_title": "Eliminar projeto",
        "confirm_delete_project_text": (
            "Eliminar o projeto '{name}' e todas as suas entradas de versão da base de dados?\n\n"
            "Os ficheiros de imagem no disco NÃO serão eliminados."
        ),
        "confirm_delete_image_title": "Eliminar entrada",
        "confirm_delete_image_text": "Eliminar esta entrada de versão?",
        "btn_delete_entry_only": "Eliminar apenas a entrada",
        "btn_delete_entry_and_file": "Eliminar entrada e ficheiro",

        "no_project_selected": "Selecione primeiro um projeto.",
        "no_image_selected": "Selecione primeiro uma entrada de imagem.",
        "project_folder_missing": "A pasta deste projeto já não existe: {folder}",
    },
    "it": {
        "window_title": "PiSafe GUI",
        "subtitle": "Interfaccia grafica per lo strumento pisafe",
        "btn_refresh_disks": "⟳  Aggiorna dischi",
        "tab_flash": "⚡  Scrivi immagine → SD",
        "tab_backup": "💾  Backup SD → immagine",
        "tab_list": "📋  Elenco dischi",
        "grp_logs": "Log",
        "btn_stop": "■  Interrompi",
        "btn_result_ok": "✓  Completato",
        "btn_result_fail": "✗  Fallito",
        "btn_clear_logs": "Cancella log",

        "grp_flash_image": "File immagine (.img / .iso / .zip / .xz / .gz / .zst)",
        "flash_img_placeholder": "Seleziona o digita il percorso del file immagine…",
        "btn_browse": "📂  Sfoglia",
        "btn_check_image": "🔎  Verifica immagine",
        "grp_flash_target": "Disco di destinazione (SD / USB)",
        "label_disk": "Disco:",
        "flash_warning": "⚠️  Attenzione: il contenuto del disco selezionato verrà sovrascritto PERMANENTEMENTE!",
        "btn_flash": "⚡  Scrivi immagine sul disco",

        "grp_backup_source": "Disco di origine (SD da copiare)",
        "grp_backup_output": "File immagine di output",
        "label_dir": "Cartella:",
        "btn_dir": "📂  Cartella",
        "label_filename": "Nome file:",
        "label_compression": "Compressione:",
        "btn_backup": "💾  Crea immagine disco",

        "btn_refresh_list": "🔄  Aggiorna elenco dischi",

        "grp_disk_tools": "Strumenti disco",
        "btn_erase": "⚠  Formatta disco",
        "label_format": "Formato:",
        "erase_warning": "⚠️  Attenzione: la formattazione cancellerà PERMANENTEMENTE tutti i dati sul disco selezionato!",
        "confirm_erase_title": "Conferma formattazione",
        "confirm_erase_text": (
            "ATTENZIONE! Tutti i dati su {dev} verranno cancellati PERMANENTEMENTE!\n\n"
            "Disco: {dev}\nFormato: {fmt}\n\nVuoi davvero continuare?"
        ),

        "dlg_choose_image_title": "Scegli immagine",
        "dlg_choose_image_filter": "Immagini (*.img *.iso *.zip *.xz *.gz *.zst);;Tutti i file (*)",
        "dlg_choose_dir_title": "Scegli cartella di destinazione",

        "warn_system_disks": "Attenzione: impossibile verificare i dischi di sistema: {error}",
        "hidden_system_disks": "Dischi di sistema nascosti: {disks}",
        "hidden_non_removable_disks": "Dischi non USB/SD nascosti: {disks}",
        "no_disks_available": "(nessun disco disponibile)",
        "lsblk_error": "Errore lsblk: {error}",
        "disks_refreshed": "Elenco dischi aggiornato.\n",
        "list_error": "Errore: {error}",

        "error_title": "Errore",
        "error_invalid_image_path": "Indica un percorso valido per il file immagine.",
        "error_select_target_disk": "Seleziona un disco di destinazione.",
        "error_select_source_disk": "Seleziona un disco di origine.",
        "error_filename_required": "Indica un nome per il file di output.",
        "error_duplicate_targets": "Lo stesso disco è stato selezionato più di una volta. Scegli un disco diverso per ogni riga.",

        "confirm_flash_title": "Conferma operazione",
        "confirm_flash_text": (
            "ATTENZIONE! Tutti i dati su {dev} verranno cancellati PERMANENTEMENTE!\n\n"
            "Immagine: {img}\nDisco: {dev}\n\nVuoi davvero continuare?"
        ),
        "confirm_flash_text_multi": (
            "ATTENZIONE! Tutti i dati su questi dischi verranno cancellati PERMANENTEMENTE!\n\n"
            "Immagine: {img}\nDischi: {devices}\n\nVuoi davvero continuare?"
        ),
        "confirm_backup_title": "Conferma backup",
        "confirm_backup_text": (
            "Creazione immagine:\n  Disco: {dev}\n  File: {out_path}\n\nContinuare?"
        ),

        "busy_title": "Occupato",
        "busy_text": "È in corso un'altra operazione. Attendi o interrompila prima.",
        "task_stopped": "\n⛔ Operazione interrotta dall'utente.\n",
        "finalizing_write": "⏳ Dati inviati, completamento della scrittura sul disco (può richiedere tempo su supporti USB/SD lenti)...",
        "finalizing_checksum": "⏳ Dati letti, completamento del calcolo del checksum...",

        "verify_checkbox_label": "Verifica scrittura dopo la scrittura (solo .img/.iso)",
        "verify_unsupported_format": "ℹ️ La verifica supporta solo .img/.iso — saltata per questo formato.\n",
        "verify_unsupported_multi": "ℹ️ La verifica funziona solo con un singolo disco di destinazione — saltata per questa scrittura multipla.\n",
        "verify_running": "🔍 Verifica della scrittura in corso (calcolo dei checksum SHA256, può richiedere tempo)...\n",
        "verify_match_full": "Immagine scritta e verificata — il checksum corrisponde.",
        "verify_mismatch_full": "Immagine scritta, ma la verifica è FALLITA — il checksum non corrisponde!",
        "verify_error_full": "Impossibile verificare la scrittura (errore durante il calcolo dei checksum).",

        "btn_add_target": "+  Aggiungi disco",
        "btn_stop_multi": "■  Interrompi tutto",
        "grp_multi_progress": "Avanzamento scrittura",
        "multi_flash_started": "🚀 Avviata la scrittura di {n} dischi in parallelo: {devices}",
        "multi_flash_summary": "Completato: {ok} riusciti, {fail} falliti.",

        "checksum_paste_title": "Incolla checksum",
        "checksum_paste_label": "Nessun file di checksum trovato accanto a questa immagine.\nIncolla il checksum SHA256 o MD5 previsto (ad es. dalla pagina di download):",
        "error_invalid_checksum": "Il testo incollato non è un checksum SHA256 (64 caratteri hex) o MD5 (32 caratteri hex) valido.",
        "checksum_running": "🔍 Verifica dell'immagine in corso (checksum {algo}, può richiedere tempo)...\n",
        "checksum_match_full": "L'immagine è valida — il checksum corrisponde.",
        "checksum_mismatch_full": "Immagine CORROTTA o non valida — il checksum NON corrisponde!",
        "checksum_error_full": "Impossibile verificare il checksum dell'immagine (errore durante il calcolo).",

        "worker_success": "Completato con successo.",
        "worker_error": "Errore (codice {code}).",

        "pisafe_missing_title": "pisafe non trovato",
        "pisafe_missing_text": (
            "Lo strumento 'pisafe' non è installato.\n\n"
            "Installalo con:\n"
            "wget https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O pisafe\n"
            "bash pisafe install"
        ),

        "pkexec_missing_title": "pkexec non trovato",
        "pkexec_missing_text": (
            "Lo strumento 'pkexec' (PolicyKit) non è installato. È necessario per "
            "eseguire operazioni di scrittura/backup con privilegi di amministratore.\n\n"
            "Installalo con:\n"
            "sudo apt-get install policykit-1"
        ),

        "language_label": "Lingua:",
        "restart_required_title": "Riavvio necessario",
        "restart_required_text": "L'applicazione verrà ora riavviata per applicare la nuova lingua.",

        "tab_versions": "🗂️  Versioni",
        "grp_projects": "Progetti",
        "grp_images": "Immagini",
        "btn_new_project": "+  Nuovo progetto",
        "btn_delete_project": "Elimina progetto",
        "btn_refresh_images": "⟳  Aggiorna",
        "btn_open_folder": "📂  Apri cartella",
        "btn_delete_entry": "Elimina voce",
        "col_version": "Versione",
        "col_file": "File",
        "col_date": "Data",
        "col_size": "Dimensione",
        "col_source_disk": "Disco di origine",
        "col_notes": "Note",

        "grp_backup_project": "Progetto (opzionale)",
        "project_combo_none": "— nessun progetto —",

        "new_project_title": "Nuovo progetto",
        "new_project_name_label": "Nome progetto:",
        "new_project_folder_title": "Scegli la cartella base del progetto",
        "project_name_exists": "Esiste già un progetto con questo nome.",

        "version_dialog_title": "Nuova versione immagine",
        "version_dialog_project_label": "Progetto: {name}",
        "version_dialog_label_field": "Etichetta versione:",
        "version_dialog_notes_field": "Note (opzionale):",

        "confirm_delete_project_title": "Elimina progetto",
        "confirm_delete_project_text": (
            "Eliminare il progetto '{name}' e tutte le sue voci di versione dal database?\n\n"
            "I file immagine sul disco NON verranno eliminati."
        ),
        "confirm_delete_image_title": "Elimina voce",
        "confirm_delete_image_text": "Eliminare questa voce di versione?",
        "btn_delete_entry_only": "Elimina solo la voce",
        "btn_delete_entry_and_file": "Elimina voce e file",

        "no_project_selected": "Seleziona prima un progetto.",
        "no_image_selected": "Seleziona prima una voce immagine.",
        "project_folder_missing": "La cartella di questo progetto non esiste più: {folder}",
    },
    "de": {
        "window_title": "PiSafe GUI",
        "subtitle": "Grafische Oberfläche für das Werkzeug pisafe",
        "btn_refresh_disks": "⟳  Laufwerke aktualisieren",
        "tab_flash": "⚡  Image flashen → SD",
        "tab_backup": "💾  SD sichern → Image",
        "tab_list": "📋  Laufwerksliste",
        "grp_logs": "Protokoll",
        "btn_stop": "■  Stoppen",
        "btn_result_ok": "✓  Fertig",
        "btn_result_fail": "✗  Fehlgeschlagen",
        "btn_clear_logs": "Protokoll leeren",

        "grp_flash_image": "Image-Datei (.img / .iso / .zip / .xz / .gz / .zst)",
        "flash_img_placeholder": "Pfad zur Image-Datei auswählen oder eingeben…",
        "btn_browse": "📂  Durchsuchen",
        "btn_check_image": "🔎  Image prüfen",
        "grp_flash_target": "Ziellaufwerk (SD / USB)",
        "label_disk": "Laufwerk:",
        "flash_warning": "⚠️  Warnung: Der Inhalt des ausgewählten Laufwerks wird UNWIDERRUFLICH überschrieben!",
        "btn_flash": "⚡  Image auf Laufwerk schreiben",

        "grp_backup_source": "Quelllaufwerk (zu sichernde SD)",
        "grp_backup_output": "Ausgabe-Image-Datei",
        "label_dir": "Verzeichnis:",
        "btn_dir": "📂  Ordner",
        "label_filename": "Dateiname:",
        "label_compression": "Komprimierung:",
        "btn_backup": "💾  Laufwerksabbild erstellen",

        "btn_refresh_list": "🔄  Laufwerksliste aktualisieren",

        "grp_disk_tools": "Laufwerkswerkzeuge",
        "btn_erase": "⚠  Laufwerk formatieren",
        "label_format": "Format:",
        "erase_warning": "⚠️  Warnung: Beim Formatieren werden alle Daten auf dem ausgewählten Laufwerk UNWIDERRUFLICH gelöscht!",
        "confirm_erase_title": "Formatierung bestätigen",
        "confirm_erase_text": (
            "WARNUNG! Alle Daten auf {dev} werden UNWIDERRUFLICH gelöscht!\n\n"
            "Laufwerk: {dev}\nFormat: {fmt}\n\nMöchten Sie wirklich fortfahren?"
        ),

        "dlg_choose_image_title": "Image auswählen",
        "dlg_choose_image_filter": "Images (*.img *.iso *.zip *.xz *.gz *.zst);;Alle Dateien (*)",
        "dlg_choose_dir_title": "Zielverzeichnis auswählen",

        "warn_system_disks": "Warnung: Systemlaufwerke konnten nicht geprüft werden: {error}",
        "hidden_system_disks": "Ausgeblendete Systemlaufwerke: {disks}",
        "hidden_non_removable_disks": "Ausgeblendete Nicht-USB/SD-Laufwerke: {disks}",
        "no_disks_available": "(keine Laufwerke verfügbar)",
        "lsblk_error": "lsblk-Fehler: {error}",
        "disks_refreshed": "Laufwerksliste aktualisiert.\n",
        "list_error": "Fehler: {error}",

        "error_title": "Fehler",
        "error_invalid_image_path": "Geben Sie einen gültigen Pfad zur Image-Datei an.",
        "error_select_target_disk": "Wählen Sie ein Ziellaufwerk aus.",
        "error_select_source_disk": "Wählen Sie ein Quelllaufwerk aus.",
        "error_filename_required": "Geben Sie einen Namen für die Ausgabedatei an.",
        "error_duplicate_targets": "Dasselbe Laufwerk wurde mehrfach ausgewählt. Wählen Sie für jede Zeile ein anderes Laufwerk.",

        "confirm_flash_title": "Vorgang bestätigen",
        "confirm_flash_text": (
            "WARNUNG! Alle Daten auf {dev} werden UNWIDERRUFLICH gelöscht!\n\n"
            "Image: {img}\nLaufwerk: {dev}\n\nMöchten Sie wirklich fortfahren?"
        ),
        "confirm_flash_text_multi": (
            "WARNUNG! Alle Daten auf diesen Laufwerken werden UNWIDERRUFLICH gelöscht!\n\n"
            "Image: {img}\nLaufwerke: {devices}\n\nMöchten Sie wirklich fortfahren?"
        ),
        "confirm_backup_title": "Sicherung bestätigen",
        "confirm_backup_text": (
            "Image wird erstellt:\n  Laufwerk: {dev}\n  Datei: {out_path}\n\nFortfahren?"
        ),

        "busy_title": "Beschäftigt",
        "busy_text": "Ein anderer Vorgang läuft bereits. Bitte warten oder zuerst stoppen.",
        "task_stopped": "\n⛔ Vorgang vom Benutzer gestoppt.\n",
        "finalizing_write": "⏳ Daten gesendet, Schreibvorgang wird abgeschlossen (kann bei langsamen USB-/SD-Medien dauern)...",
        "finalizing_checksum": "⏳ Daten gelesen, Prüfsummenberechnung wird abgeschlossen...",

        "verify_checkbox_label": "Schreibvorgang nach dem Flashen überprüfen (nur .img/.iso)",
        "verify_unsupported_format": "ℹ️ Die Überprüfung unterstützt nur .img/.iso — für dieses Format übersprungen.\n",
        "verify_unsupported_multi": "ℹ️ Die Überprüfung funktioniert nur mit einem einzelnen Ziellaufwerk — für dieses Mehrfach-Flashen übersprungen.\n",
        "verify_running": "🔍 Schreibvorgang wird überprüft (SHA256-Prüfsummen werden berechnet, dies kann etwas dauern)...\n",
        "verify_match_full": "Image geschrieben und überprüft — Prüfsumme stimmt überein.",
        "verify_mismatch_full": "Image geschrieben, aber Überprüfung FEHLGESCHLAGEN — Prüfsumme stimmt nicht überein!",
        "verify_error_full": "Schreibvorgang konnte nicht überprüft werden (Fehler bei der Prüfsummenberechnung).",

        "btn_add_target": "+  Laufwerk hinzufügen",
        "btn_stop_multi": "■  Alle stoppen",
        "grp_multi_progress": "Flash-Fortschritt",
        "multi_flash_started": "🚀 Flashen von {n} Laufwerken parallel gestartet: {devices}",
        "multi_flash_summary": "Fertig: {ok} erfolgreich, {fail} fehlgeschlagen.",

        "checksum_paste_title": "Prüfsumme einfügen",
        "checksum_paste_label": "Neben diesem Image wurde keine Prüfsummendatei gefunden.\nFügen Sie die erwartete SHA256- oder MD5-Prüfsumme ein (z. B. von der Download-Seite):",
        "error_invalid_checksum": "Der eingefügte Text ist keine gültige SHA256- (64 Hex-Zeichen) oder MD5-Prüfsumme (32 Hex-Zeichen).",
        "checksum_running": "🔍 Image wird geprüft ({algo}-Prüfsumme, dies kann etwas dauern)...\n",
        "checksum_match_full": "Image ist gültig — Prüfsumme stimmt überein.",
        "checksum_mismatch_full": "Image ist BESCHÄDIGT oder ungültig — Prüfsumme stimmt NICHT überein!",
        "checksum_error_full": "Prüfsumme des Images konnte nicht überprüft werden (Fehler bei der Berechnung).",

        "worker_success": "Erfolgreich abgeschlossen.",
        "worker_error": "Fehler (Code {code}).",

        "pisafe_missing_title": "pisafe nicht gefunden",
        "pisafe_missing_text": (
            "Das Werkzeug 'pisafe' ist nicht installiert.\n\n"
            "Installieren Sie es mit:\n"
            "wget https://raw.githubusercontent.com/RichardMidnight/pi-safe/main/pisafe -O pisafe\n"
            "bash pisafe install"
        ),

        "pkexec_missing_title": "pkexec nicht gefunden",
        "pkexec_missing_text": (
            "Das Werkzeug 'pkexec' (PolicyKit) ist nicht installiert. Es wird benötigt, um "
            "Flash-/Sicherungsvorgänge mit Administratorrechten auszuführen.\n\n"
            "Installieren Sie es mit:\n"
            "sudo apt-get install policykit-1"
        ),

        "language_label": "Sprache:",
        "restart_required_title": "Neustart erforderlich",
        "restart_required_text": "Die Anwendung wird jetzt neu gestartet, um die neue Sprache anzuwenden.",

        "tab_versions": "🗂️  Versionen",
        "grp_projects": "Projekte",
        "grp_images": "Images",
        "btn_new_project": "+  Neues Projekt",
        "btn_delete_project": "Projekt löschen",
        "btn_refresh_images": "⟳  Aktualisieren",
        "btn_open_folder": "📂  Ordner öffnen",
        "btn_delete_entry": "Eintrag löschen",
        "col_version": "Version",
        "col_file": "Datei",
        "col_date": "Datum",
        "col_size": "Größe",
        "col_source_disk": "Quelllaufwerk",
        "col_notes": "Notizen",

        "grp_backup_project": "Projekt (optional)",
        "project_combo_none": "— kein Projekt —",

        "new_project_title": "Neues Projekt",
        "new_project_name_label": "Projektname:",
        "new_project_folder_title": "Basisordner des Projekts wählen",
        "project_name_exists": "Ein Projekt mit diesem Namen existiert bereits.",

        "version_dialog_title": "Neue Image-Version",
        "version_dialog_project_label": "Projekt: {name}",
        "version_dialog_label_field": "Versionsbezeichnung:",
        "version_dialog_notes_field": "Notizen (optional):",

        "confirm_delete_project_title": "Projekt löschen",
        "confirm_delete_project_text": (
            "Projekt '{name}' und alle zugehörigen Versionseinträge aus der Datenbank löschen?\n\n"
            "Image-Dateien auf dem Laufwerk werden NICHT gelöscht."
        ),
        "confirm_delete_image_title": "Eintrag löschen",
        "confirm_delete_image_text": "Diesen Versionseintrag löschen?",
        "btn_delete_entry_only": "Nur Eintrag löschen",
        "btn_delete_entry_and_file": "Eintrag und Datei löschen",

        "no_project_selected": "Wählen Sie zuerst ein Projekt aus.",
        "no_image_selected": "Wählen Sie zuerst einen Image-Eintrag aus.",
        "project_folder_missing": "Der Ordner dieses Projekts existiert nicht mehr: {folder}",
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
