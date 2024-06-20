import sys
import io
from PyQt5.QtWidgets import QApplication
from console import Console
import check_python

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
