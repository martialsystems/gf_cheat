# Copyright (c) 2026 Martial Systems LLC
"""Refuse GF-learned and connectome-stepped claims."""

from __future__ import annotations

from typing import Any

from cheatforge.graphs._common import binary_graph

_FLAGS = (
    "gf_learned",
    "connectome_stepped",
    "parent_f_restamp",
    "animation_as_science",
)


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v = [k for k in _FLAGS if state.get(k)]
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(name="cheat.claim_bans", evaluate=_evaluate, extra=list(_FLAGS))
