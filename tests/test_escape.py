# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import numpy as np

from gf_cheat.config import RunConfig
from gf_cheat.escape import drives
from gf_cheat.genome import I_GF, I_LEAK, I_LPLC2, I_OTHER


def test_template_uses_gf() -> None:
    cfg = RunConfig()
    z = np.zeros((1, cfg.k_a))
    gf, lplc2, slow, _ = drives(z, cfg)
    assert gf[0] >= cfg.theta_gf
    assert lplc2[0] >= cfg.theta_slow


def test_leak_zero_lplc2_does_not_drive_gf() -> None:
    cfg = RunConfig(leak0=0.0)
    z = np.zeros((2, cfg.k_a))
    z[1, I_LPLC2] = 1.5
    gf, _, _, _ = drives(z, cfg)
    assert abs(gf[1] - gf[0]) < 1e-9


def test_leak_positive_lplc2_raises_gf() -> None:
    cfg = RunConfig(leak0=0.6)
    z = np.zeros((2, cfg.k_a))
    z[1, I_LPLC2] = 1.0
    gf, _, _, _ = drives(z, cfg)
    assert gf[1] > gf[0]


def test_suppressing_gf_cell_can_drop_below_theta() -> None:
    cfg = RunConfig()
    z = np.zeros((1, cfg.k_a))
    z[0, I_GF] = -1.5
    gf, _, _, _ = drives(z, cfg)
    assert gf[0] < cfg.theta_gf
