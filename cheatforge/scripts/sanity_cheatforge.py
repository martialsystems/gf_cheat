#!/usr/bin/env python3
# Copyright (c) 2026 Martial Systems LLC
"""Refuse paths for cheatforge laws."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from cheatforge.gate import (
    FLYWIRE_N,
    MALECNS_N,
    LawBlockedError,
    require_claims,
    require_engine,
    require_leak,
    require_templates,
)


def main() -> None:
    require_claims()
    try:
        require_claims(gf_learned=True)
        raise SystemExit("expected gf_learned block")
    except LawBlockedError:
        pass
    require_engine(eval_n=0)
    try:
        require_engine(eval_n=9)
        raise SystemExit("expected eval cap block")
    except LawBlockedError:
        pass
    require_leak()
    try:
        require_leak(leak_is_trained=True)
        raise SystemExit("expected trained leak block")
    except LawBlockedError:
        pass
    require_templates(female_n=FLYWIRE_N, male_n=MALECNS_N)
    print("cheatforge sanity pass")


if __name__ == "__main__":
    main()
