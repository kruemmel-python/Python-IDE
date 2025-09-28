"""Entry point for the Python IDE using PySide6."""
from __future__ import annotations

import io
import logging
import os
import sys
from typing import Iterable, Optional, Tuple, Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from check_python import get_python_executable
from console import Console

LOGGER = logging.getLogger(__name__)


def configure_logging() -> None:
    """Initialise a default logging configuration once per process."""
    if logging.getLogger().handlers:
        return

    log_path = os.path.join(os.path.dirname(__file__), "ide.log")
    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    LOGGER.debug("Logging configured")


def ensure_utf8_stdout() -> None:
    """Ensure stdout uses UTF-8 encoding for consistency across platforms."""
    stream = sys.stdout
    if not stream:
        return

    encoding = getattr(stream, "encoding", "").lower() if getattr(stream, "encoding", None) else ""
    if encoding == "utf-8":
        return

    buffer = getattr(stream, "buffer", None)
    if buffer is None:
        return

    sys.stdout = io.TextIOWrapper(buffer, encoding="utf-8")
    LOGGER.debug("stdout wrapped with UTF-8 encoding")


def create_application(argv: Optional[Iterable[str]] = None) -> QApplication:
    """Create the QApplication instance required for the GUI."""
    configure_logging()
    ensure_utf8_stdout()
    existing_app = QApplication.instance()
    if existing_app is not None:
        return existing_app
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    return QApplication(list(argv) if argv is not None else sys.argv)


def main(
    argv: Optional[Iterable[str]] = None,
    *,
    run_app: bool = True,
) -> Union[int, Tuple[QApplication, Console]]:
    """Start the IDE and optionally enter the Qt event loop.

    Parameters
    ----------
    argv:
        Optional iterable of arguments to pass to :class:`QApplication`.
    run_app:
        If ``True`` (default) the Qt event loop is started and the return value is
        the exit status of :meth:`QApplication.exec`. When ``False`` the
        function returns the created :class:`QApplication` and :class:`Console`
        instances without starting the event loop.  This is primarily intended
        for testing.
    """

    app = create_application(argv)

    python_exec = get_python_executable()
    LOGGER.info("Using Python executable: %s", python_exec)

    console = Console(python_exec)
    console.show()
    LOGGER.info("Console window displayed")

    if not run_app:
        return app, console

    result = app.exec()
    LOGGER.info("Application exited with status %s", result)
    return result


if __name__ == "__main__":
    sys.exit(main())
