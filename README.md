# gf_cheat

Can you penalize giant-fiber (DNp01) use, reward slow LPLC2-only visual escape, outcross to normals who still jump on GF, and watch whether the famous cell cheats back in?

Seed 1, N=400: P(use GF) 1.000 → 0.160 under GF-penalty selection, then 0.590 after outcross to normals. Follow end 0.520. Closed-form. LPLC2→GF leak is template coupling LEAK0 = 0.6, not a trained weight. FlyWire/MaleCNS are templates, not the stepper.

Locked log: `logs/select_outcross.json`. Parent [fly_vial](https://github.com/martialsystems/fly_vial) locked F sentence is a different question. Do not restamp it.

Under selection, P(LPLC2-only) rose to 0.723. After injecting 200 template-noise normals (outcross_frac = 0.5), P(use GF) jumped to 0.590. Relaxed follow stayed at 0.520. The famous cell came back with the normals. Engine did not run a 166k spike loop.

Seeds 2 and 3, same protocol: P(use GF) 1.000 → 0.585 / 0.583 under selection, then 0.767 / 0.767 at outcross, follow 0.708 / 0.672. Direction matches seed 1. Title stays seed 1.

## Locked metrics

Copied from `logs/select_outcross.json`.

| phase | P(use GF) | P(LPLC2-only) | mean z_GF |
|-------|----------:|--------------:|----------:|
| G0 | 1.000 | 0.000 | ~0 |
| select end | 0.160 | 0.723 | -0.341 |
| outcross | 0.590 | 0.368 |  |
| follow end | 0.520 | 0.408 | -0.245 |

LEAK0 is the template LPLC2→DNp01 coupling scale. Raising LPLC2 still feeds GF. That leak is not fitted to this run.

## How to run

```
.venv/bin/python -m pytest
.venv/bin/python -m gf_cheat run --n 400 --seed 1 --select-gens 40 --follow-gens 40 --eval-connectome --out logs/select_outcross.json
```

## Files

| Path | Role |
|------|------|
| `src/gf_cheat/` | Genome, escape scores, selection, outcross |
| `logs/select_outcross.json` | Locked seed-1 select/outcross/follow |
| `cheatforge/` | GraphForge pin |
| `AGENTS.md` | Project rules and VBD |

[Fly research index](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178)
