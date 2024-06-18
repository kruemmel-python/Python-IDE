# Start your new project here
import sys
import io
from PyQt5.QtWidgets import QApplication
import check_python
from console import Console

# Konfigurieren des Logging-Moduls
import logging
logging.basicConfig(filename='ide.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

if sys.stdout and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

def main():
    app = QApplication(sys.argv)
    embedded_python_path = check_python.get_python_executable()
    console = Console(embedded_python_path)
    console.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
