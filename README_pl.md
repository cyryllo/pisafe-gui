# PiSafe GUI 🫐

Graficzny interfejs (PyQt5) dla narzędzia [pisafe](https://github.com/RichardMidnight/pi-safe) — prosty sposób na flashowanie obrazów systemowych na karty SD/USB oraz tworzenie ich kopii zapasowych, bez używania terminala.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Raspberry%20Pi%20OS-lightgrey.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

---

## 📸 Podgląd

![Interfejs PiSafe GUI](doc/screenshot.png)

---

## ✨ Funkcje

- **⚡ Flash obrazu → SD/USB** — wybierz plik obrazu (`.img`, `.zip`, `.xz`, `.gz`, `.zst`) i dysk docelowy, jednym kliknięciem
- **💾 Backup SD/USB → obraz** — twórz kopie zapasowe kart SD z wyborem formatu kompresji
- **🛡️ Ochrona dysków systemowych** — aplikacja automatycznie wykrywa i **ukrywa** dyski, na których zamontowany jest system (`/`, `/boot`, `/home` itd.), więc nie ma ryzyka przypadkowego nadpisania własnego systemu
- **📋 Lista dysków** — pełny podgląd podłączonych urządzeń blokowych (`lsblk`)
- **📜 Logi w czasie rzeczywistym** — pełny output komend widoczny w aplikacji
- **🎨 Ciemny motyw** — interfejs w stylu Catppuccin Mocha

---

## 🌐 Języki

Interfejs jest dostępny w wersjach:

- 🇬🇧 angielski (domyślny)
- 🇵🇱 polski

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

Z menu systemowego System>PiSafe GUI

Z konsoli

```bash
python3 pisafe_gui.py
```

> Operacje flash/backup wymagają uprawnień `sudo`, ponieważ `pisafe` operuje bezpośrednio na urządzeniach blokowych. Aplikacja poprosi o hasło w trakcie wykonywania komendy.

---

## 📁 Struktura projektu

```
pisafe-gui/
├── pisafe_gui.py          # Główna aplikacja PyQt5
├── requirements.txt       # Zależności Pythona
├── install.sh             # Skrypt instalacyjny
└── README.md
```

---

## 🗺️ Planowane funkcje (TODO)

- [ ] Weryfikacja sumy kontrolnej obrazu (MD5/SHA256)
- [ ] Historia ostatnich operacji
- [ ] Powiadomienie systemowe po zakończeniu zadania
- [ ] Obsługa wielu dysków jednocześnie
- [ ] Zarządzanie wersjami obrazów — przeglądanie wskazanego folderu z obrazami i tagowanie/wersjonowanie backupów (np. v1, v2, "stable"), żeby łatwo odróżnić starsze obrazy od najnowszych

---

## 🤝 Wsparcie i wkład

Pull requesty i zgłoszenia (issues) są mile widziane! Jeśli znajdziesz błąd lub masz propozycję funkcji, otwórz issue w tym repozytorium.

**Dodawanie tłumaczenia:** otwórz plik [`translations.py`](translations.py), dodaj kod i nazwę swojego języka do `LANGUAGES`, a następnie skopiuj słownik `"en"` pod nowym kluczem i przetłumacz wartości (zachowując `{placeholdery}` bez zmian). To wszystko — żadne inne zmiany w kodzie nie są potrzebne. PR-y z nowymi językami są bardzo mile widziane!

---

## 📄 Licencja

Ten projekt jest dostępny na licencji [MIT](LICENSE).

Bazuje na narzędziu [pisafe](https://github.com/RichardMidnight/pi-safe) autorstwa RichardMidnight.

---

## 🙏 Podziękowania

- [RichardMidnight](https://github.com/RichardMidnight) — za stworzenie narzędzia `pisafe`
- [Catppuccin](https://github.com/catppuccin/catppuccin) — za paletę kolorów motywu
