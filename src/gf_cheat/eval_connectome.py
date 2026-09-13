# Copyright (c) 2026 Martial Systems LLC
"""Cap-8 rate-model audit on LPLC2 and DNp01. Not the engine."""

from __future__ import annotations

import json

import numpy as np

from gf_cheat.config import RunConfig
from gf_cheat.escape import Escape
from gf_cheat.paths import TEMPLATES
from cheatforge.gate import require_engine


def eval_sample(esc: Escape, cfg: RunConfig, rng: np.random.Generator) -> list[dict]:
    n = min(int(cfg.eval_n), int(esc.z.shape[0]), cfg.eval_n_max)
    require_engine(
        eval_n=n,
        eval_n_max=cfg.eval_n_max,
        eval_whole_population=False,
        eval_as_default_engine=False,
    )
    if n <= 0:
        return []
    spec = json.loads((TEMPLATES / "escape_subgraph.json").read_text(encoding="utf-8"))
    w = np.asarray(spec["W"], dtype=np.float64)
    cells = spec["cells"]
    i_lplc2 = cells.index("LPLC2")
    i_gf = cells.index("DNp01")
    pick = rng.choice(esc.z.shape[0], size=n, replace=False)
    rows = []
    for i in pick:
        ww = w.copy()
        ww[i_gf, i_lplc2] = cfg.leak0 * float(np.exp(esc.z[i, 2]))
        r = np.zeros(w.shape[0])
        i_ext = np.zeros(w.shape[0])
        i_ext[i_lplc2] = float(np.exp(esc.z[i, 1]))
        i_ext[i_gf] += float(np.exp(esc.z[i, 0]))
        for _ in range(20):
            r = np.tanh(ww @ r + i_ext)
        rows.append(
            {
                "lplc2_rate": float(np.abs(r[i_lplc2])),
                "gf_rate": float(np.abs(r[i_gf])),
                "used_gf_closed_form": bool(esc.used_gf[i]),
            }
        )
    return rows
