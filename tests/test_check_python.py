import sys

import check_python


def test_get_python_executable_fallback(monkeypatch):
    monkeypatch.setattr(check_python, "_embedded_candidates", lambda _: [])
    assert check_python.get_python_executable() == sys.executable


def test_get_python_executable_embedded(tmp_path, monkeypatch):
    embedded = tmp_path / "python"
    embedded.write_text("#!/usr/bin/env python3", encoding="utf-8")
    monkeypatch.setattr(check_python, "_embedded_candidates", lambda _: [embedded])
    assert check_python.get_python_executable() == str(embedded)
