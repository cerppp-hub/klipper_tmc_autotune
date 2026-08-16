# Source and redistribution

The preferred form for modifying this package is the public
[`snapmaker-u1`](https://github.com/cerppp-hub/klipper_tmc_autotune/tree/snapmaker-u1)
branch. The root `motor_constants.py` and `motor_database.cfg` files are
canonical upstream source. The root `autotune_tmc.py` is derived from upstream
with a small U1 adaptation that exposes the existing `small_hysteresis` driver
choice as a config option and runtime `AUTOTUNE_TMC` parameter. The
`scripts/stage_bespok3d.py` script assembles these sources with the Bespok3d
manifest, configuration template, documentation, and GPL text.

The adaptation is based on upstream commit
`b6c7cfa98c2ef880812d5279a9117cbe67d6d4d5` from:

https://github.com/andrewmcgr/klipper_tmc_autotune

That snapshot includes upstream commit
`a4f4daa0b3512b751bb95cd20759e36a4963c25f`, which preserves tuned TOFF across
Klipper virtual-enable re-enable events.

Klipper TMC Autotune and this adaptation are distributed under GPL-3.0.
Redistributors must preserve the copyright and modification notices, provide
corresponding source, and state any further changes they make.
