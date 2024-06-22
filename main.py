import sys
import io
from PyQt5.QtWidgets import QApplication
from console import Console
import check_python

def get_python_executable():
    embedded_python_path = os.path.join(
        os.path.dirname(__file__), "python_embedded", "python.exe"
    )

    if os.path.exists(embedded_python_path):
        return embedded_python_path
    else:
        print("Embedded Python not found. Using system Python.")
        return sys.executable

def main():
    python_exec = get_python_executable()
    print(f"Using Python executable: {python_exec}")

import logging
logging.basicConfig(filename='ide.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

if sys.stdout and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

def main():
    logging.debug("Anwendung wird gestartet")
    app = QApplication(sys.argv)
    embedded_python_path = check_python.get_python_executable()
    logging.debug(f"Embedded Python Path: {embedded_python_path}")
    console = Console(embedded_python_path)
    console.show()
    logging.debug("Hauptfenster wird angezeigt")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
