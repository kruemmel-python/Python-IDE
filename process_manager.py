import subprocess
import tempfile
import logging
import os
import sys
from PyQt5.QtWidgets import QInputDialog

def run_script(console, script):
    if console.code_editor.current_file:
        project_dir = os.path.dirname(console.code_editor.current_file)
    else:
        project_dir = os.getcwd()

    os.chdir(project_dir)
    sys.path.insert(0, project_dir)

    # Temporäre Datei im Projektverzeichnis erstellen
    temp_script_path = os.path.join(project_dir, "temp_script.py")
    with open(temp_script_path, 'w', encoding='utf-8') as temp_script:
        temp_script.write(script)
        
    try:
        # Starten Sie einen neuen Subprozess, um das Skript auszuführen
        execute_script(console, temp_script_path, project_dir)
    except subprocess.CalledProcessError as e:
        logging.error(f"Script execution failed: {e}")
        console.terminal.appendPlainText(f"ERROR: Script execution failed: {e}")

def execute_script(console, script_path, project_dir):
    # Setzen des Arbeitsverzeichnisses auf das Projektverzeichnis
    process = subprocess.Popen([console.embedded_python_path, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=project_dir)

    # Ausgabe in die Konsole weiterleiten
    stdout, stderr = process.communicate()
    console.terminal.appendPlainText(stdout)
    if stderr:
        console.terminal.appendPlainText(f"ERROR: {stderr}")

def create_exe(console):
    script = console.code_editor.toPlainText()
    if console.code_editor.current_file:
        project_dir = os.path.dirname(console.code_editor.current_file)
    else:
        project_dir = os.getcwd()

    os.chdir(project_dir)

    temp_script_path = os.path.join(project_dir, "temp_script.py")
    with open(temp_script_path, 'w', encoding='utf-8') as file:
        file.write(script)
    
    exe_name, ok = QInputDialog.getText(console, 'Name der ausführbaren Datei', 'Bitte geben Sie den Namen der ausführbaren Datei ein:')
    
    if ok and exe_name:
        try:
            subprocess.run([console.embedded_python_path, "-m", "PyInstaller", "--onefile", "--noconfirm", "--name", exe_name, temp_script_path], cwd=project_dir)
            logging.info(f"Executable created with name '{exe_name}' using pyinstaller.")
            console.terminal.appendPlainText(f"Executable created with name '{exe_name}' using pyinstaller.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Executable creation failed: {e}")
            console.terminal.appendPlainText(f"ERROR: Executable creation failed: {e}")

def install_package(console):
    package_name, ok = QInputDialog.getText(console, 'Install Package', 'Bitte geben Sie den Namen des zu installierenden Pakets ein:')
    
    if ok and package_name:
        console.terminal.appendPlainText(f"Installing package '{package_name}'...")
        subprocess.run([console.embedded_python_path, "-m", "pip", "install", package_name])
        console.terminal.appendPlainText(f"Package '{package_name}' installed successfully.")
    else:
        console.terminal.appendPlainText("Package installation cancelled.")

def update_package(console):
    package_name, ok = QInputDialog.getText(console, 'Update Package', 'Bitte geben Sie den Namen des zu aktualisierenden Pakets ein:')
    
    if ok and package_name:
        console.terminal.appendPlainText(f"Updating package '{package_name}'...")
        subprocess.run([console.embedded_python_path, "-m", "pip", "install", "--upgrade", package_name])
        console.terminal.appendPlainText(f"Package '{package_name}' updated successfully.")
    else:
        console.terminal.appendPlainText("Package update cancelled.")

def uninstall_package(console):
    package_name, ok = QInputDialog.getText(console, 'Uninstall Package', 'Bitte geben Sie den Namen des zu deinstallierenden Pakets ein:')
    
    if ok and package_name:
        console.terminal.appendPlainText(f"Uninstalling package '{package_name}'...")
        subprocess.run([console.embedded_python_path, "-m", "pip", "uninstall", "-y", package_name])
        console.terminal.appendPlainText(f"Package '{package_name}' uninstalled successfully.")
    else:
        console.terminal.appendPlainText("Package uninstallation cancelled.")
