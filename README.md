# Python IDE

Willkommen zur **Python IDE**, einer benutzerfreundlichen integrierten Entwicklungsumgebung (IDE) für Python. Diese IDE ermöglicht es Ihnen, Python-Code zu schreiben, zu bearbeiten, auszuführen und zu debuggen. Sie unterstützt Syntaxhervorhebung, Code-Vervollständigung, eine TODO-Liste und vieles mehr.

![image](https://github.com/kruemmel-python/Python-IDE/assets/169469747/e7a2be9f-cc84-4c5a-a560-0a80c4049c1c)


# Python IDE

Eine benutzerdefinierte Python-IDE mit integriertem Projekt-Explorer, Code-Editor, Konsole, interaktiver Konsole und Unterstützung für Plugins. Diese IDE ist darauf ausgelegt, sowohl mit einer systeminstallierten Python-Version als auch mit einer im Programmverzeichnis befindlichen eingebetteten Python-Version zu arbeiten.

## Funktionen

### Projekt-Explorer

- Projekte aus einem Verzeichnis laden
- Neue Projekte erstellen
- Neue Dateien und Ordner hinzufügen
- Dateien und Ordner löschen
- Doppelklick auf Dateien zum Öffnen im Code-Editor

### Code-Editor

- Syntaxhervorhebung
- Fehlerhervorhebung
- Autovervollständigung
- Linting mit pylint

### Konsole

- Anzeige des Programmoutputs
- Anzeige von Fehlermeldungen und Logs

### Interaktive Konsole

- Ausführen von Python-Code interaktiv

### Menüoptionen

#### Code-Menü

- **Interaktives Programm ausführen (Ctrl+I):** Führt das aktuelle Skript in der interaktiven Konsole aus
- **Lint Code (Ctrl+Shift+F):** Lintet das aktuelle Skript mit pylint
- **Git Commit (Ctrl+Shift+C):** Commits Änderungen in das lokale Git-Repository
- **Snippet hinzufügen (Ctrl+Shift+N):** Fügt den aktuellen Code als Snippet hinzu
- **Unit Tests ausführen (Ctrl+T):** Führt Unit-Tests für das aktuelle Projekt aus
- **Code Refactoring (Ctrl+Shift+R):** Refaktorisieren des Codes
- **Debugger starten (Ctrl+D):** Startet den Debugger

#### Programm erstellen-Menü

- **erstellen:** Erstellen einer ausführbaren Datei aus dem aktuellen Projekt

#### Konsole-Menü

- **Ausgabe löschen (Ctrl+L):** Löscht den Konsolenausgang
- **Interaktive Konsole löschen (Ctrl+Shift+L):** Löscht die interaktive Konsole

#### Info-Menü

- **Info (Ctrl+H):** Zeigt Informationen über die IDE an
- **Tastenkürzel (Ctrl+K):** Zeigt Tastenkürzel an
- **Text übersetzen (Ctrl+Shift+T):** Übersetzt den ausgewählten Text

#### Bibliotheken-Menü

- **Neues Paket installieren:** Installiert ein neues Python-Paket
- **Paket aktualisieren:** Aktualisiert ein vorhandenes Python-Paket
- **Paket deinstallieren:** Deinstalliert ein Python-Paket

#### Projekt-Menü

- **Projekt öffnen (Ctrl+O):** Öffnet ein vorhandenes Projekt
- **Projekt erstellen (Ctrl+N):** Erstellt ein neues Projekt

#### Speichern-Menü

- **geladenen Code speichern (Ctrl+S):** Speichert den aktuellen Code


#### Ansicht-Menü

- Sichtbarkeit der verschiedenen Dock-Widgets umschalten:
  - **Projekt Explorer (Ctrl+T)**
  - **Code Editor**
  - **Konsole**
  - **TODO Liste**
  - **Interaktive Konsole**

#### Einstellungen-Menü

- **Layout speichern (Ctrl+Shift+S):** Speichert die aktuellen Layouteinstellungen

### Plugin-Unterstützung

Die IDE unterstützt Plugins zur Erweiterung der Funktionalität. Plugins können erstellt und verwaltet werden, ohne den Kerncode der IDE zu ändern.

Siehe die [Plugin Anleitung](plugin_anleitung.md) für detaillierte Anweisungen zum Erstellen und Verwenden von Plugins.

### Systemanforderungen

- Die IDE kann sowohl mit einer systeminstallierten Python-Version als auch mit einer eingebetteten Python-Version arbeiten.
- Die eingebettete Python-Version sollte im Verzeichnis `python_embedded` innerhalb des Programmordners liegen.

## Erste Schritte

### Voraussetzungen

- Python 3.8 oder höher

### Installation

1. Klone das Repository:
   ```sh
   git clone https://github.com/kruemmel-python/Python-IDE


## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Informationen finden Sie in der [LICENSE](LICENSE.md).


## Entpacken sie die Pythonversion in ihren Programmordner und das Programm läuft unabhängig von der installierten Pythonversion. Somit ist es portable.
https://1drv.ms/u/s!AroxmBWhYNuLz3wVb_BnvkGO8_kn?e=3jGqrf
