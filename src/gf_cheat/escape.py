# Copyright (c) 2026 Martial Systems LLC
"""Closed-form loom escape: GF vs LPLC2-only. Leak is template coupling."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from gf_cheat.config import RunConfig
from gf_cheat.genome import I_FERT, I_GF, I_LEAK, I_LPLC2, I_OTHER, Pop, additive_z


@dataclass
class Escape:
    z: np.ndarray
    gf_drive: np.ndarray
    lplc2_drive: np.ndarray
    slow_drive: np.ndarray
    used_gf: np.ndarray
    slow_ok: np.ndarray
    lplc2_only: np.ndarray
    leak_share: np.ndarray
    fitness: np.ndarray
    fertility: np.ndarray


def drives(z: np.ndarray, cfg: RunConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    gf = np.exp(z[:, I_GF])
    lplc2 = np.exp(z[:, I_LPLC2])
    leak = np.exp(z[:, I_LEAK])
    other = np.exp(z[:, I_OTHER])
    leak_term = cfg.leak0 * lplc2 * leak
    gf_drive = gf * (1.0 + leak_term)
    slow_drive = other * lplc2
    leak_share = leak_term / (1.0 + leak_term)
    return gf_drive, lplc2, slow_drive, leak_share


def phenotype(pop: Pop, cfg: RunConfig, *, select: bool) -> Escape:
    z = additive_z(pop)
    gf_drive, lplc2_drive, slow_drive, leak_share = drives(z, cfg)
    used_gf = gf_drive >= cfg.theta_gf
    slow_ok = (lplc2_drive >= cfg.theta_slow) & (slow_drive >= cfg.theta_slow)
    lplc2_only = slow_ok & ~used_gf
    v_template = np.exp(-cfg.beta * np.square(z).sum(axis=1))
    fert = np.clip(np.exp(-cfg.beta * np.square(z[:, I_FERT])), 0.0, 1.0)
    if select:
        raw = cfg.w_rew * lplc2_only.astype(np.float64) - cfg.w_pen * used_gf.astype(np.float64)
        # Residual 0.5 so template GF-jumpers still replace. Zero fitness would empty G0.
        shaped = np.clip(0.5 + 0.5 * (0.5 + 0.5 * raw), 0.0, 1.0)
        fit = shaped * v_template
    else:
        fit = v_template
    return Escape(
        z=z,
        gf_drive=gf_drive,
        lplc2_drive=lplc2_drive,
        slow_drive=slow_drive,
        used_gf=used_gf,
        slow_ok=slow_ok,
        lplc2_only=lplc2_only,
        leak_share=leak_share,
        fitness=fit,
        fertility=fert,
    )
