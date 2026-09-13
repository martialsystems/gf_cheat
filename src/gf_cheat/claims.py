# Copyright (c) 2026 Martial Systems LLC
"""Fail closed on banned claim tokens."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

BANNED: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("gf_learned", re.compile(r"\bGF learned\b|giant fiber learned|the fly decided", re.I)),
    (
        "connectome_stepped",
        re.compile(r"(connectome|166k|139k).{0,40}(stepped|ran the vial|simulated the population)", re.I),
    ),
    ("parent_f", re.compile(r"F = 0\.524|F=0\.524")),
    (
        "deformed_visual",
        re.compile(r"deformed.{0,30}visual style|visual style.{0,30}deformed", re.I),
    ),
)


class ClaimBanError(RuntimeError):
    pass


def scan_text(text: str) -> list[str]:
    return [name for name, pat in BANNED if pat.search(text or "")]


def require_clean(text: str, *, source: str) -> None:
    hits = scan_text(text)
    if hits:
        raise ClaimBanError(f"{source}: banned claims {hits}")
    if "—" in (text or ""):
        raise ClaimBanError(f"{source}: em dash")


def require_paths_clean(paths: Iterable[Path]) -> None:
    for path in paths:
        if path.is_file():
            require_clean(path.read_text(encoding="utf-8"), source=str(path))
