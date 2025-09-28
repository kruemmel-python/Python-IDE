import json
from pathlib import Path

import pytest

from codex_client import CodexAPIError, CodexClient, apply_generated_files


class DummyResponse:
    def __init__(self, body: str) -> None:
        self._body = body.encode("utf-8")

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class DummyOpener:
    def __init__(self, body: str) -> None:
        self.body = body
        self.last_request = None
        self.last_timeout = None

    def open(self, request, timeout=30):
        self.last_request = request
        self.last_timeout = timeout
        return DummyResponse(self.body)


def test_codex_client_success(tmp_path):
    opener = DummyOpener(json.dumps({"message": "ok"}))
    client = CodexClient(base_url="https://example.invalid/api", opener=opener, api_key="token")

    result = client.execute("modify_project", "Bitte ändern", project_path=str(tmp_path))

    assert result["message"] == "ok"
    assert opener.last_timeout == 30.0
    sent_payload = json.loads(opener.last_request.data.decode("utf-8"))
    assert sent_payload["project_path"] == str(tmp_path)
    assert sent_payload["action"] == "modify_project"
    assert opener.last_request.get_header("Authorization") == "Bearer token"


def test_codex_client_invalid_json(tmp_path):
    opener = DummyOpener("not-json")
    client = CodexClient(base_url="https://example.invalid/api", opener=opener)

    with pytest.raises(CodexAPIError):
        client.execute("modify_project", "test", project_path=str(tmp_path))


def test_apply_generated_files(tmp_path):
    files = [
        {"path": "src/main.py", "content": "print('hi')"},
        {"path": "README.md", "content": "# Hallo"},
    ]
    written = apply_generated_files(tmp_path, files)

    expected_paths = [
        Path(tmp_path / "src" / "main.py").resolve(),
        Path(tmp_path / "README.md").resolve(),
    ]

    assert written == expected_paths
    assert (tmp_path / "src" / "main.py").read_text(encoding="utf-8") == "print('hi')"
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == "# Hallo"


def test_apply_generated_files_blocks_escape(tmp_path):
    with pytest.raises(ValueError):
        apply_generated_files(tmp_path, [{"path": "../hack.py", "content": ""}])
