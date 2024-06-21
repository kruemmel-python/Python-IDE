import os
import sys


def get_python_executable():
    embedded_python_path = os.path.join(
        os.path.dirname(__file__), "python_embedded", "python.exe"
    )

    if os.path.exists(embedded_python_path):
        return embedded_python_path
    else:
        print("Embedded Python not found. Using system Python.")
        return sys.executable
