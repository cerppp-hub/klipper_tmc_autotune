# Changelog

## 0.2.0-u1.2 - 2026-08-12

- Target the confirmed U1 motion-motor mapping: BJ42D29-100V78 on the TMC2240 X/Y axes and BJ42D22-130 on the TMC2209 Z axis.
- Fix both motor profiles at the Keli BJ42D family's documented 1.8-degree step angle (200 full steps per revolution).
- Remove the two unnecessary step-angle installer fields and label the remaining electrical fields with the exact motor model.
- Remove illustrative electrical placeholders so they cannot be mistaken for verified constants for these custom windings.

## 0.2.0-u1.1 - 2026-08-12

- Package upstream commit `b6c7cfa98c2ef880812d5279a9117cbe67d6d4d5` for the Snapmaker U1 vendor Klipper layout.
- Collect the fitted X/Y and Z motor constants as printer-scoped Bespok3d installation variables.
- Render a U1 configuration that tunes only the fixed X, Y, and Z motion motors.
- Preserve the stock sensorless-homing paths: TMC2240 SGT threshold 1 on X/Y and TMC2209 SG4 threshold 110 on Z.
- Keep every tuned axis in SpreadCycle performance mode so homing is not silently moved to an incompatible StealthChop path.
- Add source staging, compatibility verification, licensing, attribution, and U1 operating documentation.
