# Copyright (c) 2026 Martial Systems LLC
"""CLI for GF-versus-LPLC2 selection and outcross."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gf_cheat.claims import require_clean
from gf_cheat.config import RunConfig
from gf_cheat.paths import LOGS, REPO
from gf_cheat.population import run_experiment, write_run

BANNER = (
    "Select against giant-fiber escape. Reward LPLC2-only. Outcross. Watch GF return."
)


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gf-cheat", description=BANNER)
    sub = p.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="select, outcross, follow")
    run.add_argument("--n", type=int, default=400)
    run.add_argument("--seed", type=int, default=1)
    run.add_argument("--select-gens", type=int, default=40)
    run.add_argument("--follow-gens", type=int, default=40)
    run.add_argument("--outcross-frac", type=float, default=0.5)
    run.add_argument("--leak0", type=float, default=0.6)
    run.add_argument("--eval-connectome", action="store_true")
    run.add_argument("--out", type=Path, default=LOGS / "select_outcross.json")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    require_clean(BANNER, source="banner")
    readme = REPO / "README.md"
    if readme.is_file():
        require_clean(readme.read_text(encoding="utf-8"), source="README.md")
    cfg = RunConfig(
        n=args.n,
        seed=args.seed,
        n_ceiling=args.n,
        select_gens=args.select_gens,
        follow_gens=args.follow_gens,
        outcross_frac=args.outcross_frac,
        leak0=args.leak0,
        eval_connectome=bool(args.eval_connectome),
    )
    result = run_experiment(cfg)
    write_run(result, args.out)
    print(
        f"p_gf g0={result['p_used_gf_g0']:.3f} "
        f"select_end={result['p_used_gf_select_end']:.3f} "
        f"outcross={result['p_used_gf_outcross']:.3f} "
        f"follow_end={result['p_used_gf_follow_end']:.3f} "
        f"fell={result['gf_fell_under_selection']} "
        f"rose={result['gf_rose_after_outcross']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
