# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from pathlib import Path

import pytest

from gf_cheat import BANNER
from gf_cheat.claims import ClaimBanError, require_clean, scan_text

REPO = Path(__file__).resolve().parents[1]


def test_banner_clean() -> None:
    assert scan_text(BANNER) == []
    require_clean(BANNER, source="banner")


def test_readme_clean() -> None:
    require_clean((REPO / "README.md").read_text(encoding="utf-8"), source="README.md")
    require_clean((REPO / "description.txt").read_text(encoding="utf-8"), source="description.txt")
    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "—" not in agents
    assert "—" not in (REPO / "README.md").read_text(encoding="utf-8")
    assert "What it is not" not in (REPO / "README.md").read_text(encoding="utf-8")


def test_banned_tokens() -> None:
    with pytest.raises(ClaimBanError):
        require_clean("the giant fiber learned to hide", source="x")
    with pytest.raises(ClaimBanError):
        require_clean("em dash — no", source="x")
