# Benutzerhandbuch

Dieses Benutzerhandbuch beschreibt die Funktionen und die Verwendung der Python IDE.

## Menüleiste

### Code
- **Interaktives Programm ausführen**: Führt den aktuellen Python-Code im Editor interaktiv aus.
- **Lint Code**: Analysiert den Code auf Stilfehler und zeigt Verbesserungsmöglichkeiten an.
- **Git Commit**: Führt einen Git-Commit mit einer angegebenen Nachricht durch.
- **Snippet hinzufügen**: Fügt den aktuellen Code als Snippet hinzu.
- **Unit Tests ausführen**: Führt Unit-Tests für das aktuelle Projekt aus und zeigt die Ergebnisse im Konsolen-Output.
- **Code Refactoring**: Hilft bei der Umstrukturierung des Codes, wie dem Ersetzen von Variablen im gesamten Code.
- **Debugger starten**: Startet den Debugger und ermöglicht das Setzen von Breakpoints und das schrittweise Durchgehen des Codes.
  
  Hier sind die grundlegenden Schritte zur Verwendung des PDB-Debuggers:
1.	Befehle in der PDB-Shell:
o	n (next): Führt die nächste Zeile aus und hält danach an.
o	c (continue): Führt den Code weiter bis zum nächsten Haltepunkt aus.
o	s (step): Tritt in Funktionen ein und führt diese Zeile für Zeile aus.
o	q (quit): Beendet den Debugger.
o	l (list): Zeigt den Quellcode um den aktuellen Haltepunkt an.
2.	Durch den Code navigieren:
o	Um die nächste Zeile auszuführen und zum nächsten Haltepunkt zu gelangen, geben Sie n ein.
o	Um den Code bis zum nächsten Haltepunkt oder Ende auszuführen, geben Sie c ein.
o	Um in Funktionen einzutreten und diese Schritt für Schritt auszuführen, geben Sie s ein.
3.	Variablen inspizieren:
o	Geben Sie den Namen einer Variablen ein, um ihren aktuellen Wert zu sehen.
o	Verwenden Sie den Befehl p gefolgt von einem Ausdruck, um den Ausdruck zu drucken, z.B. p variable_name.
4.	Haltepunkte setzen:
o	Haltepunkte können direkt im Code durch das Einfügen der Zeile import pdb; pdb.set_trace() gesetzt werden.


### Programm erstellen
- **Erstellen**: Erstellt eine ausführbare Datei aus dem aktuellen Python-Code im Editor.

### Konsole
- **Ausgabe löschen**: Löscht den Inhalt der Konsolenausgabe.
- **Interaktive Konsole löschen**: Löscht den Inhalt der interaktiven Konsole.

### Info
- **Info**: Zeigt Informationen über die Syntaxhervorhebung und die Bedeutung der Farben an.
- **Tastenkürzel**: Zeigt eine Liste der verfügbaren Tastenkürzel an.
- **Text übersetzen**: Übersetzt den ausgewählten Text im Editor.

### Bibliotheken
- **Neues Paket installieren**: Ermöglicht die Installation neuer Python-Pakete über pip.
- **Paket aktualisieren**: Ermöglicht die Aktualisierung eines bestehenden Python-Pakets.
- **Paket deinstallieren**: Ermöglicht die Deinstallation eines bestehenden Python-Pakets.

### Projekt
- **Projekt öffnen**: Öffnet ein bestehendes Projektverzeichnis.
- **Projekt erstellen**: Erstellt ein neues Projektverzeichnis.

### Speichern
- **Geladenen Code speichern**: Speichert den aktuellen Code im Editor in der geladenen Datei.

### Ansicht
- **Sichtbar Fenster Projekt**: Blendet das Projektfenster ein oder aus.
- **Sichtbar Code editor**: Blendet den Code-Editor ein oder aus.
- **Sichtbar Konsole**: Blendet die Konsole ein oder aus.
- **Sichtbar Todo Liste**: Blendet die TODO-Liste ein oder aus.
- **Sichtbar Interaktive Konsole**: Blendet die interaktive Konsole ein oder aus.

### Einstellungen
- **Layout speichern**: Speichert das aktuelle Layout der IDE.

### Plugins
- **Plugin aktivieren/deaktivieren**: Aktiviert oder deaktiviert ein Plugin aus der Liste der verfügbaren Plugins.

## Projektverwaltung

### Neue Datei erstellen
1. Rechtsklicken Sie im Projektfenster.
2. Wählen Sie "New File" und geben Sie den Namen der neuen Datei ein.
3. Die Datei wird im aktuellen Verzeichnis erstellt.

### Neuen Ordner erstellen
1. Rechtsklicken Sie im Projektfenster.
2. Wählen Sie "New Folder" und geben Sie den Namen des neuen Ordners ein.
3. Der Ordner wird im aktuellen Verzeichnis erstellt.

### Datei oder Ordner löschen
1. Rechtsklicken Sie auf die Datei oder den Ordner im Projektfenster.
2. Wählen Sie "Delete".
3. Die Datei oder der Ordner wird gelöscht.

## TODO-Liste
Die TODO-Liste zeigt alle TODO-Kommentare im aktuellen Code an. Klicken Sie auf einen Eintrag, um zur entsprechenden Zeile im Code zu springen.

## Code-Vervollständigung
Die IDE verwendet Jedi für die Code-Vervollständigung. Beginnen Sie mit der Eingabe, und es werden Vorschläge angezeigt. Wählen Sie einen Vorschlag aus der Liste aus, um ihn zu verwenden.

## Dokumentation anzeigen
Wenn ein Wort im Code markiert ist und Sie `Strg` und `D` drücken, wird die zugehörige Dokumentation angezeigt.

## Syntaxhervorhebung
Die IDE hebt verschiedene Elemente des Python-Codes hervor:
- **Keywords**: Blau und fett.
- **Strings**: Rot.
- **Zahlen**: Orange.
- **Kommentare**: Grün.
- **Funktionen und Klassen**: Blau und fett.
- **Operatoren**: Lila.
- **Klammern**: Gelb.

## Fehlerbehebung
Falls Sie Probleme mit der IDE haben, überprüfen Sie bitte die `ide.log`-Datei im Hauptverzeichnis. Diese Datei enthält Informationen zu Fehlern und anderen Ereignissen, die bei der Verwendung der IDE aufgetreten sind.

## Weitere Informationen
Für weitere Informationen und die neuesten Updates besuchen Sie bitte das [GitHub-Repository](https://github.com/kruemmel-python/Python-IDE).

## Plugin-Erstellung
Für Informationen zur Erstellung und Nutzung von Plugins, lesen Sie bitte die [Plugin-Anleitung](plugin_anleitung.md).
