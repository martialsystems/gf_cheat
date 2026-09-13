# gf_cheat

Can you penalize giant-fiber (DNp01) use, reward slow LPLC2-only visual escape, outcross to normals who still jump on GF, and watch whether the famous cell cheats back in?

Seed 1, N=400: P(use GF) 1.000 → 0.160 under a GF penalty, then 0.590 after a 50% outcross to GF jumpers. Follow ended 0.520. The cell returned with the normals. LEAK0=0.6 is template coupling, not a trained weight.

Locked log: `logs/select_outcross.json`. Parent [fly_vial](https://github.com/martialsystems/fly_vial) locked F sentence is a different question.

The 0.590 outcross value is the mix. Half the vial is still the selected pool (0.160); half is template-noise normals (1.000): 0.5 × 0.160 + 0.5 × 1.0 = 0.580. Logged 0.590. Follow then fell to 0.520. GF did not reconquer in the next 40 generations. Selection works. Half a vial of jumpers undoes it.

Under selection, P(LPLC2-only) rose to 0.723 on seed 1. Engine is closed-form. FlyWire/MaleCNS are templates, not the stepper.

Seeds 2 and 3, same protocol: P(use GF) 1.000 → 0.585 / 0.583 under selection, then 0.767 / 0.767 at outcross (mix predicts ~0.79), follow 0.708 / 0.672. Same sign, not the same punch. Title stays seed 1. A leak=0 arm is not in the locked log. Template leak as the cheat path is untested.

## Locked metrics

Copied from `logs/select_outcross.json`.

| phase | P(use GF) | P(LPLC2-only) | mean z_GF |
|-------|----------:|--------------:|----------:|
| G0 | 1.000 | 0.000 | -0.001 |
| select end | 0.160 | 0.723 | -0.341 |
| outcross | 0.590 | 0.368 |  |
| follow end | 0.520 | 0.408 | -0.245 |

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
