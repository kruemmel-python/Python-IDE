import os
import sys
import shutil
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QMessageBox

def open_project(console):
    project_dir = QFileDialog.getExistingDirectory(console, 'Open Project', os.getcwd())
    if project_dir:
        console.project_files.clear()
        sys.path.insert(0, project_dir)  # Fügen Sie das Projektverzeichnis zu sys.path hinzu
        for root, _, files in os.walk(project_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    console.project_files.addItem(file_path)

def new_project(console):
    project_dir = QFileDialog.getExistingDirectory(console, 'Select Directory for New Project', os.getcwd())
    if project_dir:
        project_name, ok = QInputDialog.getText(console, 'New Project', 'Bitte geben Sie den Namen des neuen Projekts ein:')
        if ok and project_name:
            new_project_path = os.path.join(project_dir, project_name)
            try:
                os.makedirs(new_project_path)
                console.terminal.appendPlainText(f"Created new project at: {new_project_path}")
                # Optional: Grundlegende Projektstruktur anlegen
                with open(os.path.join(new_project_path, 'main.py'), 'w', encoding='utf-8') as main_file:
                    main_file.write("# Start your new project here\n")
                console.project_files.clear()
                console.project_files.addItem(os.path.join(new_project_path, 'main.py'))
            except Exception as e:
                console.terminal.appendPlainText(f"Failed to create new project: {str(e)}")

def create_new_file(console):
    if console.project_files.currentItem():
        current_path = console.project_files.currentItem().text()
        if os.path.isdir(current_path):
            directory = current_path
        else:
            directory = os.path.dirname(current_path)
    else:
        directory = os.getcwd()

    file_name, ok = QInputDialog.getText(console, 'New File', 'Bitte geben Sie den Namen der neuen Datei ein:')
    if ok and file_name:
        new_file_path = os.path.join(directory, file_name)
        try:
            with open(new_file_path, 'w', encoding='utf-8') as new_file:
                new_file.write("")
            console.terminal.appendPlainText(f"Neue Datei: {new_file_path}")
            console.project_files.addItem(new_file_path)
        except Exception as e:
            console.terminal.appendPlainText(f"Fehler: Keine neue Datei erstellt: {str(e)}")

def create_new_folder(console):
    if console.project_files.currentItem():
        current_path = console.project_files.currentItem().text()
        if os.path.isdir(current_path):
            directory = current_path
        else:
            directory = os.path.dirname(current_path)
    else:
        directory = os.getcwd()

    folder_name, ok = QInputDialog.getText(console, 'Neuer Ordner', 'Bitte geben Sie den Namen des neuen Ordners ein:')
    if ok and folder_name:
        new_folder_path = os.path.join(directory, folder_name)
        try:
            os.makedirs(new_folder_path)
            console.terminal.appendPlainText(f"Neuer Ordner erstellt: {new_folder_path}")
            console.project_files.addItem(new_folder_path)
        except Exception as e:
            console.terminal.appendPlainText(f"Fehler; Es konnte kein Ordner erstellt werden: {str(e)}")

def delete_item(console):
    if console.project_files.currentItem():
        item_path = console.project_files.currentItem().text()
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
            console.terminal.appendPlainText(f"Markiertes Löschen: {item_path}")
            console.project_files.takeItem(console.project_files.currentRow())
        except Exception as e:
            console.terminal.appendPlainText(f"Fehler Löschen erfolglos: {str(e)}")

def load_file(console, item):
    file_path = item.text()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            console.code_editor.setPlainText(file.read())
        console.code_editor.current_file = file_path
        console.terminal.appendPlainText(f"Datei geladen: {file_path}")
        console.update_todo_list()
    except Exception as e:
        console.terminal.appendPlainText(f"konnte Datei nicht laden: {file_path}\n{str(e)}")

def save_file(console):
    if console.code_editor.current_file:
        try:
            with open(console.code_editor.current_file, 'w', encoding='utf-8') as file:
                file.write(console.code_editor.toPlainText())
            console.terminal.appendPlainText(f"Datei gespeichert: {console.code_editor.current_file}")
        except Exception as e:
            console.terminal.appendPlainText(f"Fehler beim Speichern: {console.code_editor.current_file}\n{str(e)}")
    else:
        console.terminal.appendPlainText("Keine Datei zum speichern geladen.")
