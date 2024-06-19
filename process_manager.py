import subprocess
import logging
import os
import sys
from PyQt5.QtWidgets import QInputDialog

def run_script(console, script):
    logging.debug("run_script gestartet")
    if console.project_dir:
        project_dir = console.project_dir
    else:
        project_dir = os.getcwd()

    os.chdir(project_dir)
    sys.path.insert(0, project_dir)

    temp_script_path = os.path.join(project_dir, "temp_script.py")
    with open(temp_script_path, 'w', encoding='utf-8') as temp_script:
        temp_script.write(script)
    logging.debug(f"Script gespeichert: {temp_script_path}")

    try:
        if hasattr(console, 'current_process') and console.current_process:
            console.current_process.terminate()
            logging.debug("Vorheriger Prozess beendet")

        console.current_process = subprocess.Popen(
            [console.embedded_python_path, temp_script_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=project_dir
        )
        logging.debug("Neuer Prozess gestartet")

        output, error = console.current_process.communicate()

        if output:
            console.console_output.appendPlainText(output)
        if error:
            console.console_output.appendPlainText(f"ERROR: {error}")
        logging.debug("Skriptausführung abgeschlossen")

    except subprocess.CalledProcessError as e:
        logging.error(f"Script execution failed: {e}")
        console.console_output.appendPlainText(f"ERROR: Script execution failed: {e}")

def create_exe(console):
    script = console.code_editor.toPlainText()
    logging.debug("create_exe gestartet")
    if console.project_dir:
        project_dir = console.project_dir
    else:
        project_dir = os.getcwd()

    os.chdir(project_dir)

    temp_script_path = os.path.join(project_dir, "temp_script.py")
    with open(temp_script_path, 'w', encoding='utf-8') as file:
        file.write(script)
    logging.debug(f"Script für EXE gespeichert: {temp_script_path}")

    exe_name, ok = QInputDialog.getText(console, 'Name der ausführbaren Datei', 'Bitte geben Sie den Namen der ausführbaren Datei ein:')

    if ok and exe_name:
        try:
            subprocess.run(
                [console.embedded_python_path, "-m", "PyInstaller", "--onefile", "--noconfirm", "--name", exe_name, temp_script_path],
                cwd=project_dir
            )
            logging.info(f"Executable created with name '{exe_name}' using pyinstaller.")
            console.console_output.appendPlainText(f"Executable created with name '{exe_name}' using pyinstaller.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Executable creation failed: {e}")
            console.console_output.appendPlainText(f"ERROR: Executable creation failed: {e}")

def install_package(console):
    package_name, ok = QInputDialog.getText(console, 'Install Package', 'Bitte geben Sie den Namen des zu installierenden Pakets ein:')

    if ok and package_name:
        logging.debug(f"Installing package '{package_name}'...")
        console.console_output.appendPlainText(f"Installing package '{package_name}'...")
        subprocess.run([console.embedded_python_path, "-m", "pip", "install", package_name])
        console.console_output.appendPlainText(f"Package '{package_name}' installed successfully.")
    else:
        logging.debug("Package installation cancelled")
        console.console_output.appendPlainText("Package installation cancelled.")

def update_package(console):
    package_name, ok = QInputDialog.getText(console, 'Update Package', 'Bitte geben Sie den Namen des zu aktualisierenden Pakets ein:')

    if ok and package_name:
        logging.debug(f"Updating package '{package_name}'...")
        console.console_output.appendPlainText(f"Updating package '{package_name}'...")
        subprocess.run([console.embedded_python_path, "-m", "pip", "install", "--upgrade", package_name])
        console.console_output.appendPlainText(f"Package '{package_name}' updated successfully.")
    else:
        logging.debug("Package update cancelled")
        console.console_output.appendPlainText("Package update cancelled.")

def uninstall_package(console):
    package_name, ok = QInputDialog.getText(console, 'Uninstall Package', 'Bitte geben Sie den Namen des zu deinstallierenden Pakets ein:')

    if ok and package_name:
        logging.debug(f"Uninstalling package '{package_name}'...")
        console.console_output.appendPlainText(f"Uninstalling package '{package_name}'...")
        subprocess.run([console.embedded_python_path, "-m", "pip", "uninstall", "-y", package_name])
        console.console_output.appendPlainText(f"Package '{package_name}' uninstalled successfully.")
    else:
        logging.debug("Package uninstallation cancelled")
        console.console_output.appendPlainText("Package uninstallation cancelled.")
