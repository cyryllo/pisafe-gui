# PiSafe GUI 🫐

Graficzny interfejs (PyQt5) dla narzędzia [pisafe](https://github.com/RichardMidnight/pi-safe) — prosty sposób na flashowanie obrazów systemowych na karty SD/USB oraz tworzenie ich kopii zapasowych, bez używania terminala.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Raspberry%20Pi%20OS-lightgrey.svg)
![License](https://img.shields.io/badge/license-GPLv3-yellow.svg)

---

## 📸 Podgląd

![Interfejs PiSafe GUI](doc/screenshot.png)

---

## ✨ Funkcje

- **⚡ Flash obrazu → SD/USB** — wybierz plik obrazu (`.img`, `.zip`, `.xz`, `.gz`, `.zst`) i dysk docelowy, jednym kliknięciem
- **💾 Backup SD/USB → obraz** — twórz kopie zapasowe kart SD z wyborem formatu kompresji
- **🗂️ Zarządzanie wersjami obrazów** — grupuj backupy w nazwane projekty z własnym folderem bazowym, etykietuj każdy z nich dowolnym tekstem (v1, v2, "stable" itd.) i przeglądaj/usuwaj je w osobnej zakładce (baza SQLite)
- **✅ Weryfikacja sumy kontrolnej** — opcjonalnie zweryfikuj flashowanie porównując SHA256 pliku źródłowego `.img`/`.iso` z tym, co faktycznie zapisano na dysku, z automatycznym wynikiem zgodności/niezgodności
- **🔎 Sprawdzanie pobranego obrazu** — sprawdź integralność pobranego obrazu przed flashowaniem: aplikacja sama wykryje plik `.sha256`/`.sha256sum`/`.md5` obok obrazu albo pozwoli wkleić oczekiwaną sumę ze strony pobierania
- **📀 Flashowanie wielu dysków naraz** — dodaj do 8 dysków docelowych przyciskami `+`/`-` i wgraj ten sam obraz na wszystkie równolegle, z osobnym paskiem postępu dla każdego dysku i podsumowaniem na koniec
- **🔧 Narzędzia dysku** — sprawdź dysk (wykryty system, układ partycji, wolne miejsce) albo szybko go zformatuj (FAT32/exFAT/NTFS/ext4), ograniczone do dysków USB/SD tak jak przy flashowaniu
- **🛡️ Ochrona dysków systemowych** — aplikacja automatycznie wykrywa i **ukrywa** dyski, na których zamontowany jest system (`/`, `/boot`, `/home` itd.), więc nie ma ryzyka przypadkowego nadpisania własnego systemu
- **📋 Lista dysków** — pełny podgląd podłączonych urządzeń blokowych (`lsblk`)
- **📜 Logi w czasie rzeczywistym** — pełny output komend widoczny w aplikacji
- **🎨 Ciemny motyw** — interfejs w stylu Catppuccin Mocha

---

## 🌐 Języki

Interfejs jest dostępny w wersjach:

- 🇬🇧 angielski (domyślny)
- 🇵🇱 polski
- 🇪🇸 hiszpański

Język można zmienić z listy rozwijanej w nagłówku aplikacji — po zmianie aplikacja uruchamia się ponownie, aby zastosować nowy język. Tłumaczenia znajdują się w pliku [`translations.py`](translations.py) jako proste słowniki klucz → tekst, więc dodanie nowego języka nie wymaga zmian w kodzie interfejsu. Chcesz dodać swój język? Zobacz sekcję [Wsparcie i wkład](#-wsparcie-i-wkład) poniżej.

---

## 🖥️ Wymagania

- Linux / Raspberry Pi OS
- Python 3.7+
- [PyQt5](https://pypi.org/project/PyQt5/)
- [pisafe](https://github.com/RichardMidnight/pi-safe) (narzędzie bazowe, instalowane automatycznie przez `install.sh`)

---

## 🚀 Instalacja

```bash
git clone https://github.com/cyryllo/pisafe-gui.git
cd pisafe-gui
bash install.sh
```

Skrypt `install.sh`:
1. Instaluje `python3-pyqt5` i `pv`
2. Instaluje narzędzie `pisafe`, jeśli nie jest jeszcze obecne w systemie
3. Tworzy skrót aplikacji w menu systemowym

---

## ▶️ Uruchomienie

Z menu aplikacji: Akcesoria/Narzędzia > PiSafe GUI

Z konsoli

```bash
python3 pisafe_gui.py
```

> Operacje flash/backup wymagają uprawnień administratora, ponieważ `pisafe` operuje bezpośrednio na urządzeniach blokowych. Aplikacja uruchamia je przez `pkexec` (PolicyKit), który pokazuje natywne graficzne okno z prośbą o hasło — bez potrzeby terminala. `pkexec` jest instalowany automatycznie przez `install.sh` (pakiet `policykit-1`).

---

## 📁 Struktura projektu

```
pisafe-gui/
├── pisafe_gui.py          # Główna aplikacja PyQt5
├── translations.py        # Teksty i18n oraz zapis wybranego języka
├── db.py                  # Baza SQLite dla zarządzania wersjami obrazów
├── requirements.txt       # Zależności Pythona
├── install.sh             # Skrypt instalacyjny
└── README.md
```

---

## 🗺️ Planowane funkcje (TODO)

- [ ] Pakiet Debiana (`.deb`)

---

## 🤝 Wsparcie i wkład

Pull requesty i zgłoszenia (issues) są mile widziane! Jeśli znajdziesz błąd lub masz propozycję funkcji, otwórz issue w tym repozytorium.

**Dodawanie tłumaczenia:** otwórz plik [`translations.py`](translations.py), dodaj kod i nazwę swojego języka do `LANGUAGES`, a następnie skopiuj słownik `"en"` pod nowym kluczem i przetłumacz wartości (zachowując `{placeholdery}` bez zmian). To wszystko — żadne inne zmiany w kodzie nie są potrzebne. PR-y z nowymi językami są bardzo mile widziane!

---

## 📄 Licencja

Ten projekt jest dostępny na licencji [GNU GPLv3](LICENSE).

Bazuje na narzędziu [pisafe](https://github.com/RichardMidnight/pi-safe) autorstwa RichardMidnight (również GPLv3).

---

## 🙏 Podziękowania

- [RichardMidnight](https://github.com/RichardMidnight) — za stworzenie narzędzia `pisafe`
- [Catppuccin](https://github.com/catppuccin/catppuccin) — za paletę kolorów motywu
