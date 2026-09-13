# Copyright (c) 2026 Martial Systems LLC
"""Call sites for refuse laws."""

from __future__ import annotations

from typing import Any

from cheatforge._bootstrap import ensure_paths

ensure_paths()

from graphforge.product_law import LawBlockedError, require_law

from cheatforge.graphs.claim_bans import build_graph as build_claims
from cheatforge.graphs.engine_order import EVAL_N_MAX, build_graph as build_engine
from cheatforge.graphs.template_identity import (
    FLYWIRE_N,
    MALECNS_N,
    build_graph as build_templates,
)
from cheatforge.graphs.template_leak import build_graph as build_leak


def require_claims(**flags: Any) -> None:
    state = {
        "gf_learned": False,
        "connectome_stepped": False,
        "parent_f_restamp": False,
        "animation_as_science": False,
    }
    state.update(flags)
    require_law(
        build_claims(),
        state,
        allow_decisions=["allow"],
        law_id="cheat.claim_bans",
        thread_id=str(flags.get("thread_id", "cheat_claims")),
        raise_error=True,
    )


def require_engine(
    *,
    eval_n: int = 0,
    eval_n_max: int = EVAL_N_MAX,
    eval_whole_population: bool = False,
    eval_as_default_engine: bool = False,
) -> None:
    require_law(
        build_engine(),
        {
            "eval_n": int(eval_n),
            "eval_n_max": int(eval_n_max),
            "eval_whole_population": bool(eval_whole_population),
            "eval_as_default_engine": bool(eval_as_default_engine),
        },
        allow_decisions=["allow"],
        law_id="cheat.engine_order",
        thread_id="engine_order",
        raise_error=True,
    )


def require_templates(*, female_n: int = FLYWIRE_N, male_n: int = MALECNS_N) -> None:
    require_law(
        build_templates(),
        {"female_n": int(female_n), "male_n": int(male_n)},
        allow_decisions=["allow"],
        law_id="cheat.template_identity",
        thread_id="template_identity",
        raise_error=True,
    )


def require_leak(*, leak_is_trained: bool = False, unique_reconstruction: bool = False) -> None:
    require_law(
        build_leak(),
        {
            "leak_is_trained": bool(leak_is_trained),
            "unique_reconstruction": bool(unique_reconstruction),
        },
        allow_decisions=["allow"],
        law_id="cheat.template_leak",
        thread_id="template_leak",
        raise_error=True,
    )


__all__ = [
    "EVAL_N_MAX",
    "FLYWIRE_N",
    "MALECNS_N",
    "LawBlockedError",
    "require_claims",
    "require_engine",
    "require_templates",
    "require_leak",
]
