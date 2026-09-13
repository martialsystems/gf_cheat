# Copyright (c) 2026 Martial Systems LLC
"""Run hyperparameters."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RunConfig:
    n: int = 400
    seed: int = 1
    p_female: float = 0.5
    sex_imbalance_max: int = 40
    k_a: int = 6
    sigma_init: float = 0.05
    z_max: float = 2.0
    sigma_mu: float = 0.03
    c0: float = 4.0
    n_ceiling: int = 400
    beta: float = 0.05
    leak0: float = 0.6
    theta_gf: float = 1.25
    theta_slow: float = 0.8
    w_pen: float = 1.0
    w_rew: float = 1.0
    select_gens: int = 40
    follow_gens: int = 40
    outcross_frac: float = 0.5
    eval_connectome: bool = False
    eval_n_max: int = 8
    eval_n: int = 4

    @property
    def generations(self) -> int:
        return int(self.select_gens + 1 + self.follow_gens)

    def payload(self) -> dict:
        d = asdict(self)
        d["generations"] = self.generations
        d["leak0_note"] = "template LPLC2-to-GF coupling; not fitted to this run"
        return d
