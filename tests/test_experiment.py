# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import hashlib
from pathlib import Path

from gf_cheat.config import RunConfig
from gf_cheat.population import run_experiment

PARENT = Path(__file__).resolve().parents[2]
LOCKED_ASSORT = "92a328278e62c4c607749c9358cdc733e1f06424a4b7f13c97c352ce4f4f759b"


def test_parent_locked_log_untouched() -> None:
    path = PARENT / "logs" / "assort_80.json"
    assert path.is_file()
    assert hashlib.sha256(path.read_bytes()).hexdigest() == LOCKED_ASSORT


def test_short_select_then_outcross() -> None:
    cfg = RunConfig(n=60, seed=1, select_gens=8, follow_gens=8, n_ceiling=60, outcross_frac=0.5)
    result = run_experiment(cfg)
    assert result["p_used_gf_g0"] > 0.8
    assert "p_used_gf_select_end" in result
    assert "p_used_gf_outcross" in result
    phases = [g["phase"] for g in result["generations"]]
    assert "select" in phases
    assert "outcross" in phases
    assert "follow" in phases
    assert result["n_eval_hook"] == 0


def test_eval_hook_does_not_empty_run() -> None:
    off = RunConfig(n=40, seed=3, select_gens=3, follow_gens=2, n_ceiling=40)
    on = RunConfig(n=40, seed=3, select_gens=3, follow_gens=2, n_ceiling=40, eval_connectome=True, eval_n=2)
    a = run_experiment(off)
    b = run_experiment(on)
    assert b["n_eval_hook"] > 0
    assert abs(a["p_used_gf_follow_end"] - b["p_used_gf_follow_end"]) < 1e-9
