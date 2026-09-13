# Copyright (c) 2026 Martial Systems LLC
"""Select against GF, outcross to normals, follow under relaxed fitness."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from gf_cheat.config import RunConfig
from gf_cheat.escape import Escape, phenotype
from gf_cheat.genome import FEMALE, MALE, Pop, clip_qtl, init_population
from cheatforge.gate import FLYWIRE_N, MALECNS_N, require_claims, require_engine, require_templates


def _subset(pop: Pop, idx: np.ndarray) -> Pop:
    if idx.size == 0:
        return Pop(
            t=pop.t,
            n=0,
            ids=np.empty(0, dtype=np.uint64),
            sex=np.empty(0, dtype=np.uint8),
            qtl=np.empty((0, pop.qtl.shape[1], 2)),
            mother_id=np.empty(0, dtype=np.int64),
            father_id=np.empty(0, dtype=np.int64),
            is_normal=np.empty(0, dtype=bool),
            next_id=pop.next_id,
        )
    return Pop(
        t=pop.t,
        n=int(idx.size),
        ids=pop.ids[idx],
        sex=pop.sex[idx],
        qtl=pop.qtl[idx],
        mother_id=pop.mother_id[idx],
        father_id=pop.father_id[idx],
        is_normal=pop.is_normal[idx],
        next_id=pop.next_id,
    )


def cap_ceiling(pop: Pop, ceiling: int, rng: np.random.Generator) -> Pop:
    if pop.n <= ceiling:
        return pop
    idx = rng.choice(pop.n, size=ceiling, replace=False)
    idx.sort()
    return _subset(pop, idx)


def random_pairs(pop: Pop, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    f_idx = np.flatnonzero(pop.sex == FEMALE)
    m_idx = np.flatnonzero(pop.sex == MALE)
    rng.shuffle(f_idx)
    rng.shuffle(m_idx)
    n = int(min(f_idx.size, m_idx.size))
    return f_idx[:n], m_idx[:n]


def reproduce(
    pop: Pop,
    esc: Escape,
    fi: np.ndarray,
    mi: np.ndarray,
    cfg: RunConfig,
    rng: np.random.Generator,
) -> Pop:
    clutch = np.maximum(0, np.rint(cfg.c0 * esc.fitness[fi] * esc.fertility[fi] * esc.fertility[mi])).astype(np.int32)
    n_eggs = int(clutch.sum())
    if n_eggs == 0:
        empty = _subset(pop, np.empty(0, dtype=np.int64))
        empty.t = pop.t + 1
        return empty
    mom = np.repeat(fi, clutch)
    dad = np.repeat(mi, clutch)
    pick_m = rng.integers(0, 2, size=(n_eggs, cfg.k_a))
    pick_d = rng.integers(0, 2, size=(n_eggs, cfg.k_a))
    a_m = np.take_along_axis(pop.qtl[mom], pick_m[:, :, None], axis=2)[:, :, 0]
    a_d = np.take_along_axis(pop.qtl[dad], pick_d[:, :, None], axis=2)[:, :, 0]
    a_m = clip_qtl(a_m + rng.normal(0.0, cfg.sigma_mu, size=a_m.shape), cfg.z_max)
    a_d = clip_qtl(a_d + rng.normal(0.0, cfg.sigma_mu, size=a_d.shape), cfg.z_max)
    qtl = np.stack([a_m, a_d], axis=2)
    sex = rng.integers(0, 2, size=n_eggs, dtype=np.uint8)
    ids = np.arange(pop.next_id, pop.next_id + n_eggs, dtype=np.uint64)
    return Pop(
        t=pop.t + 1,
        n=n_eggs,
        ids=ids,
        sex=sex,
        qtl=qtl,
        mother_id=pop.ids[mom].astype(np.int64),
        father_id=pop.ids[dad].astype(np.int64),
        is_normal=np.zeros(n_eggs, dtype=bool),
        next_id=pop.next_id + n_eggs,
    )


def inject_normals(pop: Pop, cfg: RunConfig, rng: np.random.Generator) -> Pop:
    n_inj = int(round(pop.n * cfg.outcross_frac))
    n_inj = min(max(n_inj, 0), pop.n)
    if n_inj == 0:
        return pop
    inj_cfg = replace(cfg, n=n_inj)
    normals = init_population(inj_cfg, rng, normals=True)
    idx = rng.choice(pop.n, size=n_inj, replace=False)
    pop.qtl[idx] = normals.qtl
    pop.sex[idx] = normals.sex
    pop.is_normal[idx] = True
    pop.ids[idx] = np.arange(pop.next_id, pop.next_id + n_inj, dtype=np.uint64)
    pop.mother_id[idx] = -1
    pop.father_id[idx] = -1
    pop.next_id += n_inj
    return pop


def record(pop: Pop, esc: Escape, phase: str) -> dict:
    n = pop.n
    return {
        "t": pop.t,
        "phase": phase,
        "n": n,
        "n_normal": int(pop.is_normal.sum()) if n else 0,
        "p_used_gf": float(esc.used_gf.mean()) if n else 0.0,
        "p_lplc2_only": float(esc.lplc2_only.mean()) if n else 0.0,
        "p_slow_ok": float(esc.slow_ok.mean()) if n else 0.0,
        "mean_gf_drive": float(esc.gf_drive.mean()) if n else 0.0,
        "mean_lplc2_drive": float(esc.lplc2_drive.mean()) if n else 0.0,
        "mean_z_gf": float(esc.z[:, 0].mean()) if n else 0.0,
        "mean_z_lplc2": float(esc.z[:, 1].mean()) if n else 0.0,
        "mean_leak_share": float(esc.leak_share.mean()) if n else 0.0,
        "mean_fitness": float(esc.fitness.mean()) if n else 0.0,
    }


def run_experiment(cfg: RunConfig, rng: np.random.Generator | None = None) -> dict:
    require_claims()
    require_engine(
        eval_n=cfg.eval_n if cfg.eval_connectome else 0,
        eval_n_max=cfg.eval_n_max,
        eval_whole_population=False,
        eval_as_default_engine=False,
    )
    require_templates(female_n=FLYWIRE_N, male_n=MALECNS_N)
    from cheatforge.gate import require_leak

    require_leak()
    rng = rng or np.random.default_rng(cfg.seed)
    eval_rng = np.random.default_rng(int(cfg.seed) + 1_000_003)
    pop = init_population(cfg, rng, normals=True)
    records: list[dict] = []
    hook_rows: list[dict] = []

    def step(pop: Pop, *, select: bool, phase: str) -> Pop:
        esc = phenotype(pop, cfg, select=select)
        rec = record(pop, esc, phase)
        if cfg.eval_connectome and pop.n:
            from gf_cheat.eval_connectome import eval_sample

            rec["eval_hook"] = eval_sample(esc, cfg, eval_rng)
            hook_rows.extend(rec["eval_hook"])
        else:
            rec["eval_hook"] = []
        records.append(rec)
        if pop.n == 0:
            return pop
        fi, mi = random_pairs(pop, rng)
        if fi.size == 0:
            pop.n = 0
            return pop
        kids = reproduce(pop, esc, fi, mi, cfg, rng)
        return cap_ceiling(kids, cfg.n_ceiling, rng)

    # G0 census then select
    pop = step(pop, select=True, phase="select")
    for _ in range(cfg.select_gens):
        if pop.n == 0:
            break
        pop = step(pop, select=True, phase="select")

    pop = inject_normals(pop, cfg, rng)
    pop = step(pop, select=False, phase="outcross")

    for _ in range(cfg.follow_gens):
        if pop.n == 0:
            break
        pop = step(pop, select=False, phase="follow")

    select_recs = [r for r in records if r["phase"] == "select"]
    follow_recs = [r for r in records if r["phase"] == "follow"]
    p_gf_g0 = select_recs[0]["p_used_gf"] if select_recs else 0.0
    p_gf_sel = select_recs[-1]["p_used_gf"] if select_recs else 0.0
    p_gf_f1 = next((r["p_used_gf"] for r in records if r["phase"] == "outcross"), 0.0)
    p_gf_end = follow_recs[-1]["p_used_gf"] if follow_recs else p_gf_f1
    return {
        "config": cfg.payload(),
        "generations": records,
        "n_eval_hook": len(hook_rows),
        "p_used_gf_g0": p_gf_g0,
        "p_used_gf_select_end": p_gf_sel,
        "p_used_gf_outcross": p_gf_f1,
        "p_used_gf_follow_end": p_gf_end,
        "gf_fell_under_selection": p_gf_sel < p_gf_g0,
        "gf_rose_after_outcross": p_gf_end > p_gf_sel,
        "leak0": cfg.leak0,
    }


def write_run(result: dict, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    gens = result["generations"]
    keys = [
        "t",
        "phase",
        "n",
        "n_normal",
        "p_used_gf",
        "p_lplc2_only",
        "mean_z_gf",
        "mean_z_lplc2",
        "mean_leak_share",
        "mean_fitness",
    ]
    lines = [",".join(keys)]
    for g in gens:
        lines.append(",".join(str(g[k]) for k in keys))
    out.with_suffix(".csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
