# Changelog

## 0.2.0-u1.1 - 2026-08-12

- Package upstream commit `b6c7cfa98c2ef880812d5279a9117cbe67d6d4d5` for the Snapmaker U1 vendor Klipper layout.
- Collect the fitted X/Y and Z motor constants as printer-scoped Bespok3d installation variables.
- Render a U1 configuration that tunes only the fixed X, Y, and Z motion motors.
- Preserve the stock sensorless-homing paths: TMC2240 SGT threshold 1 on X/Y and TMC2209 SG4 threshold 110 on Z.
- Keep every tuned axis in SpreadCycle performance mode so homing is not silently moved to an incompatible StealthChop path.
- Add source staging, compatibility verification, licensing, attribution, and U1 operating documentation.
