# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_readme_question_first() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    assert text.startswith("# gf_cheat\n")
    body = text.split("\n", 1)[1].lstrip()
    assert body.startswith("Can you penalize giant-fiber")
    assert "LEAK0" in text
    assert "closed-form" in text.lower()
    assert "What it is not" not in text
    assert "—" not in text
    log = REPO / "logs" / "select_outcross.json"
    assert log.is_file()
    data = json.loads(log.read_text(encoding="utf-8"))
    assert f"select_end = {data['p_used_gf_select_end']:.3f}" in text or f"{data['p_used_gf_select_end']:.3f}" in text
