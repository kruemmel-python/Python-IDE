"""Utilities for interacting with the chatgpt.com Codex service."""
from __future__ import annotations

import json
import logging
import os
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Optional
import urllib.error
import urllib.request

LOGGER = logging.getLogger(__name__)


class CodexAPIError(RuntimeError):
    """Raised when the Codex API cannot be reached or returns an error."""


class CodexClient:
    """Thin client for the chatgpt.com Codex automation endpoint."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        opener: Optional[urllib.request.OpenerDirector] = None,
    ) -> None:
        self.base_url = base_url or os.environ.get("CODEX_API_URL", "https://chatgpt.com/codex/api")
        self.api_key = api_key or os.environ.get("CODEX_API_KEY")
        self._opener = opener or urllib.request.build_opener()

    def _build_headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def execute(
        self,
        action: str,
        prompt: str,
        *,
        project_path: Optional[str] = None,
        project_name: Optional[str] = None,
        timeout: float = 30.0,
    ) -> dict:
        """Send a request to Codex and return the JSON payload.

        Parameters
        ----------
        action:
            Operation requested from Codex, e.g. ``"modify_project"`` or
            ``"create_project"``.
        prompt:
            The natural language instructions for the desired action.
        project_path:
            Optional absolute project directory path to provide additional
            context for Codex.
        project_name:
            Optional project name, mainly used when creating a new project.
        timeout:
            Maximum number of seconds to wait for the remote service to respond.
        """

        payload: dict[str, Optional[str]] = {
            "action": action,
            "prompt": prompt,
        }
        if project_path:
            payload["project_path"] = project_path
        if project_name:
            payload["project_name"] = project_name

        request = urllib.request.Request(
            self.base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers=self._build_headers(),
        )

        LOGGER.info("Sending Codex request to %s for action %s", self.base_url, action)

        try:
            with self._opener.open(request, timeout=timeout) as response:
                raw_body = response.read().decode("utf-8")
        except urllib.error.URLError as exc:
            LOGGER.error("Failed to reach Codex API at %s: %s", self.base_url, exc)
            raise CodexAPIError("Unable to reach Codex API") from exc

        if not raw_body:
            LOGGER.debug("Codex response body was empty; assuming empty object")
            return {}

        try:
            decoded = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            LOGGER.error("Invalid JSON returned by Codex: %s", raw_body)
            raise CodexAPIError("Codex API returned invalid JSON") from exc

        if isinstance(decoded, dict) and decoded.get("error"):
            LOGGER.error("Codex API error: %s", decoded["error"])
            raise CodexAPIError(str(decoded["error"]))

        if not isinstance(decoded, dict):
            LOGGER.debug("Codex response was not a dict; wrapping into dict")
            return {"response": decoded}

        return decoded


def apply_generated_files(base_path: Path | str, files: Iterable[Mapping[str, str]]) -> list[Path]:
    """Persist generated file content inside ``base_path``.

    Parameters
    ----------
    base_path:
        Directory that should contain the generated files.
    files:
        Iterable of mappings containing at least ``path`` and ``content`` keys.

    Returns
    -------
    list[Path]
        Sequence of absolute file paths that were created or overwritten.
    """

    base_directory = Path(base_path).expanduser().resolve()
    base_directory.mkdir(parents=True, exist_ok=True)

    written_files: list[Path] = []
    for file_entry in files:
        relative_path = file_entry.get("path") if isinstance(file_entry, Mapping) else None
        if not relative_path:
            LOGGER.warning("Skipping file entry without path: %s", file_entry)
            continue

        target_path = (base_directory / relative_path).resolve()
        if base_directory not in target_path.parents and target_path != base_directory:
            raise ValueError(f"Refusing to write outside the base directory: {target_path}")

        target_path.parent.mkdir(parents=True, exist_ok=True)
        content = file_entry.get("content", "") if isinstance(file_entry, Mapping) else ""
        target_path.write_text(content, encoding="utf-8")
        written_files.append(target_path)
        LOGGER.info("Wrote Codex generated file: %s", target_path)

    return written_files
