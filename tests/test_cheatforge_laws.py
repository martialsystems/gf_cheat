# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import pytest

from cheatforge.gate import LawBlockedError, require_claims, require_engine, require_leak
from cheatforge.product_laws import laws


def test_four_laws() -> None:
    ids = [row["id"] for row in laws()]
    assert "cheat.claim_bans" in ids
    assert "cheat.template_leak" in ids


def test_blocks_gf_learned() -> None:
    with pytest.raises(LawBlockedError):
        require_claims(gf_learned=True)


def test_blocks_eval_cap() -> None:
    with pytest.raises(LawBlockedError):
        require_engine(eval_n=9)


def test_blocks_trained_leak() -> None:
    with pytest.raises(LawBlockedError):
        require_leak(leak_is_trained=True)
