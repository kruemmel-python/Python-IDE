"""Plugin that integrates chatgpt.com Codex into the IDE."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, Signal, Slot
from PySide6.QtWidgets import (
    QDockWidget,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)

from plugin_interface import PluginInterface
from codex_client import CodexAPIError, CodexClient, apply_generated_files

LOGGER = logging.getLogger(__name__)


class _WorkerSignals(QObject):
    completed = Signal(object, dict, str, str)
    failed = Signal(object, str)


class _CodexWorker(QRunnable):
    def __init__(
        self,
        client: CodexClient,
        action: str,
        prompt: str,
        target_path: str,
        project_name: Optional[str],
    ) -> None:
        super().__init__()
        self.client = client
        self.action = action
        self.prompt = prompt
        self.target_path = target_path
        self.project_name = project_name
        self.signals = _WorkerSignals()

    def run(self) -> None:  # pragma: no cover - executed in worker thread
        try:
            payload = self.client.execute(
                self.action,
                self.prompt,
                project_path=self.target_path,
                project_name=self.project_name,
            )
        except CodexAPIError as exc:
            LOGGER.warning("Codex request failed: %s", exc)
            self.signals.failed.emit(self, str(exc))
        except Exception as exc:  # pragma: no cover - defensive logging
            LOGGER.exception("Unexpected error while talking to Codex", exc_info=exc)
            self.signals.failed.emit(self, str(exc))
        else:
            if not isinstance(payload, dict):
                payload = {"response": payload}
            self.signals.completed.emit(self, payload, self.target_path, self.action)


class CodexDockWidget(QDockWidget):
    request_submitted = Signal(str, str, str, str)

    def __init__(self, ide) -> None:
        super().__init__("Codex Assistent", ide)
        self.ide = ide
        self.setObjectName("codex_dock")
        container = QWidget(self)
        layout = QVBoxLayout(container)

        description = QLabel(
            "Nutze chatgpt.com Codex, um Projekte automatisch zu erstellen oder zu aktualisieren."
        )
        description.setWordWrap(True)
        layout.addWidget(description)

        project_name_layout = QHBoxLayout()
        project_name_label = QLabel("Neues Projekt:")
        self.project_name_input = QLineEdit()
        self.project_name_input.setPlaceholderText("Name für neue Projekte")
        project_name_layout.addWidget(project_name_label)
        project_name_layout.addWidget(self.project_name_input)
        layout.addLayout(project_name_layout)

        prompt_label = QLabel("Anweisung")
        layout.addWidget(prompt_label)

        self.prompt_edit = QPlainTextEdit()
        self.prompt_edit.setPlaceholderText("Beschreibe, was Codex erstellen oder ändern soll...")
        layout.addWidget(self.prompt_edit)

        button_layout = QHBoxLayout()
        self.modify_button = QPushButton("Projekt aktualisieren")
        self.create_button = QPushButton("Neues Projekt generieren")
        button_layout.addWidget(self.modify_button)
        button_layout.addWidget(self.create_button)
        layout.addLayout(button_layout)

        response_label = QLabel("Codex Antwort")
        layout.addWidget(response_label)

        self.response_view = QPlainTextEdit()
        self.response_view.setReadOnly(True)
        layout.addWidget(self.response_view)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        container.setLayout(layout)
        self.setWidget(container)

        self.modify_button.clicked.connect(self._emit_modify)
        self.create_button.clicked.connect(self._emit_create)

    def _validate_prompt(self) -> Optional[str]:
        prompt = self.prompt_edit.toPlainText().strip()
        if not prompt:
            QMessageBox.warning(self, "Codex", "Bitte gib eine Anweisung für Codex ein.")
            return None
        return prompt

    @Slot()
    def _emit_modify(self) -> None:
        prompt = self._validate_prompt()
        if prompt is None:
            return

        project_dir = getattr(self.ide, "project_dir", None)
        if not project_dir:
            QMessageBox.warning(
                self,
                "Codex",
                "Es ist kein Projekt geöffnet. Öffne zuerst ein Projekt, damit Codex Änderungen anwenden kann.",
            )
            return

        self.set_busy(True)
        self.status_label.setText("Projekt wird an Codex übermittelt...")
        self.request_submitted.emit("modify_project", prompt, project_dir, "")

    @Slot()
    def _emit_create(self) -> None:
        prompt = self._validate_prompt()
        if prompt is None:
            return

        project_name = self.project_name_input.text().strip()
        if not project_name:
            QMessageBox.warning(self, "Codex", "Bitte gib einen Namen für das neue Projekt an.")
            return

        base_dir = QFileDialog.getExistingDirectory(
            self,
            "Zielverzeichnis wählen",
            getattr(self.ide, "project_dir", "") or str(Path.home()),
        )
        if not base_dir:
            self.status_label.setText("Codex Anfrage abgebrochen")
            return

        target_path = str(Path(base_dir) / project_name)
        self.set_busy(True)
        self.status_label.setText("Neues Projekt wird von Codex erstellt...")
        self.request_submitted.emit("create_project", prompt, target_path, project_name)

    def show_response(self, message: str) -> None:
        self.response_view.setPlainText(message)

    def show_error(self, message: str) -> None:
        self.status_label.setText(message)
        QMessageBox.critical(self, "Codex", message)

    def show_success(self, message: str) -> None:
        self.status_label.setText(message)

    def set_busy(self, busy: bool) -> None:
        self.modify_button.setDisabled(busy)
        self.create_button.setDisabled(busy)


class CodexIntegrationPlugin(PluginInterface):
    def __init__(self, ide) -> None:
        super().__init__(ide)
        self._dock: Optional[CodexDockWidget] = None
        self._client = CodexClient()
        self._thread_pool = QThreadPool.globalInstance()
        self._active_workers: set[_CodexWorker] = set()

    def register(self) -> None:
        LOGGER.info("CodexIntegrationPlugin registered")

    def initialize(self) -> None:
        LOGGER.debug("Initialising CodexIntegrationPlugin")
        dock = CodexDockWidget(self.ide)
        dock.request_submitted.connect(self._handle_request)
        self.ide.addDockWidget(Qt.RightDockWidgetArea, dock)
        self.ide.dock_widgets[dock.objectName()] = dock
        self._dock = dock
        LOGGER.info("CodexIntegrationPlugin initialised")

    def deinitialize(self) -> None:
        LOGGER.debug("Deinitialising CodexIntegrationPlugin")
        if self._dock:
            try:
                self.ide.removeDockWidget(self._dock)
            except Exception:  # pragma: no cover - Qt cleanup differs per platform
                LOGGER.exception("Failed to remove Codex dock widget during shutdown")
            self._dock.deleteLater()
            self.ide.dock_widgets.pop(self._dock.objectName(), None)
            self._dock = None
        self._active_workers.clear()
        LOGGER.info("CodexIntegrationPlugin deinitialised")

    @Slot(str, str, str, str)
    def _handle_request(self, action: str, prompt: str, target_path: str, project_name: str) -> None:
        worker = _CodexWorker(self._client, action, prompt, target_path, project_name or None)
        worker.signals.completed.connect(self._handle_completed)
        worker.signals.failed.connect(self._handle_failed)
        self._active_workers.add(worker)
        self._thread_pool.start(worker)

    @Slot(object, dict, str, str)
    def _handle_completed(self, worker: _CodexWorker, payload: dict, target_path: str, action: str) -> None:
        if not self._dock:
            return

        message_parts: list[str] = []
        files = payload.get("files") if isinstance(payload, dict) else None
        if files:
            try:
                written = apply_generated_files(target_path, files)
            except ValueError as exc:
                LOGGER.error("Codex lieferte ungültige Dateien: %s", exc)
                self._dock.show_error(str(exc))
                self._dock.set_busy(False)
                self._active_workers.discard(worker)
                return

            message_parts.append(f"{len(written)} Datei(en) aktualisiert.")
            if action == "create_project":
                self._refresh_project_view(target_path)
        response_message = payload.get("message") if isinstance(payload, dict) else None
        if response_message:
            message_parts.append(response_message)
        elif not message_parts:
            message_parts.append("Codex Anfrage abgeschlossen.")

        combined_message = "\n".join(message_parts)
        self._dock.show_response(json.dumps(payload, indent=2, ensure_ascii=False))
        self._dock.show_success(combined_message)
        self._dock.set_busy(False)
        self._active_workers.discard(worker)

    @Slot(object, str)
    def _handle_failed(self, worker: _CodexWorker, message: str) -> None:
        if not self._dock:
            return
        self._dock.set_busy(False)
        self._dock.show_error(message)
        self._active_workers.discard(worker)

    def _refresh_project_view(self, project_dir: str) -> None:
        try:
            path = str(Path(project_dir).resolve())
            self.ide.project_dir = path
            if hasattr(self.ide, "file_system_model"):
                self.ide.file_system_model.setRootPath(path)
                self.ide.project_files.setRootIndex(self.ide.file_system_model.index(path))
            if hasattr(self.ide, "interactive_console"):
                self.ide.interactive_console.project_dir = path
            if hasattr(self.ide, "console_output"):
                self.ide.console_output.appendPlainText(f"Codex Projekt bereit: {path}")
        except Exception as exc:  # pragma: no cover - defensive logging
            LOGGER.exception("Konnte Projektansicht nicht aktualisieren", exc_info=exc)
