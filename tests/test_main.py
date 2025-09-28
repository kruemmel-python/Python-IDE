from console import Console
from check_python import get_python_executable
import main


def test_main_initialises_without_exec(qapp):
    app, console = main.main(run_app=False)
    try:
        assert console.isVisible()
    finally:
        console.close()
        app.processEvents()


def test_console_creation(qapp):
    console = Console(get_python_executable())
    try:
        assert console.windowTitle() == "Python IDE"
    finally:
        console.close()
        qapp.processEvents()
