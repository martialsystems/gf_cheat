# Copyright (c) 2026 Martial Systems LLC
"""LPLC2→GF leak is a template constant, not a trained weight."""

from __future__ import annotations

from typing import Any

from cheatforge.graphs._common import binary_graph


def _evaluate(state: dict[str, Any]) -> dict[str, Any]:
    v: list[str] = []
    if bool(state.get("leak_is_trained")):
        v.append("leak_is_trained")
    if bool(state.get("unique_reconstruction")):
        v.append("unique_reconstruction")
    return {"violations": v, "events": [{"node": "evaluate", "ok": not v}]}


def build_graph():
    return binary_graph(
        name="cheat.template_leak",
        evaluate=_evaluate,
        extra=["leak_is_trained", "unique_reconstruction"],
    )
