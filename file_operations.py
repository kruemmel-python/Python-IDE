import os
import sys
import shutil
import subprocess
from PyQt5.QtWidgets import QFileDialog, QInputDialog

def open_project(console):
    project_dir = QFileDialog.getExistingDirectory(console, 'Open Project', os.getcwd())
    if project_dir:
        console.project_files.clear()
        sys.path.insert(0, project_dir)
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
                console.console_output.appendPlainText(f"Created new project at: {new_project_path}")
                # Optional: Grundlegende Projektstruktur anlegen
                with open(os.path.join(new_project_path, 'main.py'), 'w', encoding='utf-8') as main_file:
                    main_file.write("# Start your new project here\n")
                console.project_files.clear()
                console.project_files.addItem(os.path.join(new_project_path, 'main.py'))
            except Exception as e:
                console.console_output.appendPlainText(f"Failed to create new project: {str(e)}")

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
            console.console_output.appendPlainText(f"Neue Datei: {new_file_path}")
            console.project_files.addItem(new_file_path)
        except Exception as e:
            console.console_output.appendPlainText(f"Fehler: Keine neue Datei erstellt: {str(e)}")

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
            console.console_output.appendPlainText(f"Neuer Ordner erstellt: {new_folder_path}")
            console.project_files.addItem(new_folder_path)
        except Exception as e:
            console.console_output.appendPlainText(f"Fehler; Es konnte kein Ordner erstellt werden: {str(e)}")

def delete_item(console):
    if console.project_files.currentItem():
        item_path = console.project_files.currentItem().text()
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
            console.console_output.appendPlainText(f"Markiertes Löschen: {item_path}")
            console.project_files.takeItem(console.project_files.currentRow())
        except Exception as e:
            console.console_output.appendPlainText(f"Fehler Löschen erfolglos: {str(e)}")

def load_file(console, item):
    file_path = item.text()
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            console.code_editor.setPlainText(file.read())
        console.code_editor.current_file = file_path
        console.console_output.appendPlainText(f"Datei geladen: {file_path}")
        console.update_todo_list()
    except Exception as e:
        console.console_output.appendPlainText(f"konnte Datei nicht laden: {file_path}\n{str(e)}")

def save_file(console):
    if console.code_editor.current_file:
        try:
            with open(console.code_editor.current_file, 'w', encoding='utf-8') as file:
                file.write(console.code_editor.toPlainText())
            console.console_output.appendPlainText(f"Datei gespeichert: {console.code_editor.current_file}")
        except Exception as e:
            console.console_output.appendPlainText(f"Fehler beim Speichern: {console.code_editor.current_file}\n{str(e)}")
    else:
        console.console_output.appendPlainText("Keine Datei zum speichern geladen.")

def install_package(console):
    package_name, ok = QInputDialog.getText(console, 'Install Package', 'Bitte geben Sie den Namen des zu installierenden Pakets ein:')
    if ok and package_name:
        console.console_output.appendPlainText(f"Installing package '{package_name}'...")
        subprocess.run([console.embedded_python_path, "-m", "pip", "install", package_name])
        console.console_output.appendPlainText(f"Package '{package_name}' installed successfully.")
    else:
        console.console_output.appendPlainText("Package installation cancelled.")

def update_package(console):
    package_name, ok = QInputDialog.getText(console, 'Update Package', 'Bitte geben Sie den Namen des zu aktualisierenden Pakets ein:')
    if ok and package_name:
        console.console_output.appendPlainText(f"Updating package '{package_name}'...")
        subprocess.run([console.embedded_python_path, "-m", "pip", "install", "--upgrade", package_name])
        console.console_output.appendPlainText(f"Package '{package_name}' updated successfully.")
    else:
        console.console_output.appendPlainText("Package update cancelled.")

def uninstall_package(console):
    package_name, ok = QInputDialog.getText(console, 'Uninstall Package', 'Bitte geben Sie den Namen des zu deinstallierenden Pakets ein:')
    if ok and package_name:
        console.console_output.appendPlainText(f"Uninstalling package '{package_name}'...")
        subprocess.run([console.embedded_python_path, "-m", "pip", "uninstall", "-y", package_name])
        console.console_output.appendPlainText(f"Package '{package_name}' uninstalled successfully.")
    else:
        console.console_output.appendPlainText("Package uninstallation cancelled.")
