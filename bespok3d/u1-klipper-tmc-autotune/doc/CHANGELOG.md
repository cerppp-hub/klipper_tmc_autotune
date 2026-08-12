# Changelog

## 0.2.0-u1.4 - 2026-08-12

- Identify the X/Y motors as Keli BJ42D29-Y2V01.
- Fix the X/Y profile to Keli's published 2.2-ohm, 4.5-mH, 0.60-Nm, 1.5-A, 1.8-degree specifications.
- Remove the four X/Y installer fields; only the less-certain BJ42D22-130 Z profile remains editable.

## 0.2.0-u1.3 - 2026-08-12

- Add editable electrical defaults from Keli's BJ42D29-Y2 and BJ42D22-Y2 profiles.
- Document the supporting stock-current correlation: 1.2 A is 80% of the XY profile's 1.5 A rating, while 0.85 A is 85% of the Z profile's 1.0 A rating.
- Keep the values overridable because the exact OEM `-100V78` and `-130` winding sheets remain unpublished.

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
