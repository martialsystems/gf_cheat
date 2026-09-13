# Copyright (c) 2026 Martial Systems LLC
"""Refuse laws. Verify-before-done is the finish gate."""

from __future__ import annotations

from typing import Any

from cheatforge.graphs.template_identity import FLYWIRE_N, MALECNS_N


def laws() -> list[dict[str, Any]]:
    from cheatforge.graphs.claim_bans import build_graph as claim_bans
    from cheatforge.graphs.engine_order import build_graph as engine_order
    from cheatforge.graphs.template_identity import build_graph as template_identity
    from cheatforge.graphs.template_leak import build_graph as template_leak

    return [
        {
            "id": "cheat.claim_bans",
            "build": claim_bans,
            "state": {
                "gf_learned": False,
                "connectome_stepped": False,
                "parent_f_restamp": False,
                "animation_as_science": False,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "cheat.engine_order",
            "build": engine_order,
            "state": {
                "eval_whole_population": False,
                "eval_as_default_engine": False,
                "eval_n": 0,
                "eval_n_max": 8,
            },
            "allow_decisions": ["allow"],
        },
        {
            "id": "cheat.template_leak",
            "build": template_leak,
            "state": {"leak_is_trained": False, "unique_reconstruction": False},
            "allow_decisions": ["allow"],
        },
        {
            "id": "cheat.template_identity",
            "build": template_identity,
            "state": {"female_n": FLYWIRE_N, "male_n": MALECNS_N},
            "allow_decisions": ["allow"],
        },
    ]
