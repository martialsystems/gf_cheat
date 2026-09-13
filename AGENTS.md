# Agent notes: gf_cheat

Nested tree under `fly_vial`. MIT for original code. FlyWire and MaleCNS remain under their published licenses.

Question: can you select against giant-fiber (DNp01) escape, reward slow LPLC2-only escape, then outcross to GF-jumping normals and watch whether GF cheats back in?

Connectomes are templates. LPLC2→GF leak is a fixed template coupling (`LEAK0`), not a trained weight and not a live 166k LIF. The default engine is closed-form circuit scalars. `--eval-connectome` is a cap-8 audit hook with a separate RNG.

Do not restamp the parent fly_vial locked F sentence. That is a different question.

Do not claim the giant fiber acquired a skill, that the fly chose, or that the map ran the population.

Do not add FANC, animation, or a free-choice mating model. Mating is random. Selection is the fitness rule.

Do not retune `LEAK0` after a run to force cheat-back or force GF off.

Pin is `cheatforge/`. Laws: claim bans, engine order, template leak is not trained, parent F not restamped. Engine checkout `~/graphforge`. No catalog/`surfaces.json` unless asked. Verify-before-done is the finish gate.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`

`vbd.runtime.json` runs pytest and `cheatforge/scripts/sanity_cheatforge.py`.
