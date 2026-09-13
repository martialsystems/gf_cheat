# Copyright (c) 2026 Martial Systems LLC
"""Diploid QTLs for GF, LPLC2, leak, and non-GF descending escape."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from gf_cheat.config import RunConfig

FEMALE = 0
MALE = 1

QTL_AUTO = (
    "gf_gain",
    "lplc2_gain",
    "leak_mod",
    "other_dn",
    "fertility",
    "stability",
)

I_GF = 0
I_LPLC2 = 1
I_LEAK = 2
I_OTHER = 3
I_FERT = 4
I_STAB = 5


@dataclass
class Pop:
    t: int
    n: int
    ids: np.ndarray
    sex: np.ndarray
    qtl: np.ndarray
    mother_id: np.ndarray
    father_id: np.ndarray
    is_normal: np.ndarray
    next_id: int


def clip_qtl(arr: np.ndarray, z_max: float) -> np.ndarray:
    return np.clip(arr, -z_max, z_max)


def additive_z(pop: Pop) -> np.ndarray:
    return pop.qtl.mean(axis=2)


def draw_sex(n: int, cfg: RunConfig, rng: np.random.Generator) -> np.ndarray:
    sex = np.zeros(n, dtype=np.uint8)
    for _ in range(200):
        sex = (rng.random(n) >= cfg.p_female).astype(np.uint8)
        nf = int(np.sum(sex == FEMALE))
        if abs(nf - (n - nf)) <= cfg.sex_imbalance_max:
            return sex
    return sex


def init_population(cfg: RunConfig, rng: np.random.Generator, *, normals: bool = True) -> Pop:
    n = cfg.n
    sex = draw_sex(n, cfg, rng)
    qtl = clip_qtl(rng.normal(0.0, cfg.sigma_init, size=(n, cfg.k_a, 2)), cfg.z_max)
    ids = np.arange(n, dtype=np.uint64)
    return Pop(
        t=0,
        n=n,
        ids=ids,
        sex=sex,
        qtl=qtl,
        mother_id=np.full(n, -1, dtype=np.int64),
        father_id=np.full(n, -1, dtype=np.int64),
        is_normal=np.ones(n, dtype=bool) if normals else np.zeros(n, dtype=bool),
        next_id=n,
    )
