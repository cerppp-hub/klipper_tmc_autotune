# Snapmaker U1 installation and configuration

This branch adapts Klipper TMC Autotune to the U1's appliance-style Klipper
installation using a Bespok3d package. Do not run upstream `install.sh` on the
U1: its Linux paths, service assumptions, and Moonraker update-manager workflow
do not match Snapmaker's firmware layout.

## Supported motor and driver mapping

This package profile is deliberately limited to:

- X and Y: Keli `BJ42D29-100V78`, each driven by a TMC2240.
- Z only: Keli `BJ42D22-130`, driven by a TMC2209.

Both belong to Keli's two-phase BJ42D family. Keli documents that the `D` in
the model identifies a 1.8-degree step angle, so the generated profiles safely
fix `steps_per_revolution: 200`. Do not install this package on a U1 whose motor
labels differ.

## Electrical profile and evidence

The package uses Keli's published Y2-winding profiles as editable defaults:

| Axis | Profile basis | Resistance | Inductance | Holding torque | Rated current | U1 run current |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| X/Y | BJ42D29-Y2 | 2.2 ohms | 4.5 mH | 0.60 Nm | 1.5 A | 1.2 A (80%) |
| Z | BJ42D22-Y2 | 4.0 ohms | 7.9 mH | 0.40 Nm | 1.0 A | 0.85 A (85%) |

The exact agreement between the U1's stock X/Y current and 80% of the BJ42D29-Y2
rating is strong corroborating evidence. The Z current similarly lands at 85%
of the BJ42D22-Y2 rating. These values also match the motors' BJ42D29 and BJ42D22
frame/stator families and documented 1.8-degree construction.

Keli's public table does not list the custom `-100V78` or `-130` performance and
mechanical variants, however, so this remains an evidence-based identification
rather than a published cross-reference from Keli or Snapmaker.

Sources:

- [Keli BJ42D technical parameters](https://en.kelimotor.com/applist_detail/97.html)
- [Klipper configuration reference](https://www.klipper3d.org/Config_Reference.html#tmc2240), which defines `run_current` in amps RMS

The installer pre-fills the table values and keeps all eight fields editable.
If an exact OEM sheet or measurement becomes available, override the relevant
value. Inductance is entered in **henries**, torque in **newton-metres**, and
current in **amperes**.

## U1-specific safety choices

- Only `stepper_x`, `stepper_y`, and `stepper_z` are tuned. The four removable
  toolheads are intentionally excluded.
- X and Y retain the stock TMC2240 `sgt: 1` sensorless-homing threshold.
- Z retains the stock TMC2209 `sg4_thrs: 110` threshold.
- All three axes use `tuning_goal: performance` (SpreadCycle). The upstream
  `auto` goal would choose silent mode for Z, which is inappropriate for the
  U1's sensorless Z homing path.
- The package leaves the stock run currents unchanged: 1.2 A on X/Y and 0.85 A
  on Z in the audited U1 firmware snapshot.

## Install with Bespok3d

1. Make sure the printer is idle and cool.
2. In Bespok3d Desktop, choose **Add plugin from file** and select the built
   `u1-klipper-tmc-autotune-0.2.0-u1.3.b3` package.
3. Confirm the motor labels match the supported mapping and review the eight
   pre-filled Y2-profile values. Override them only with better model-specific
   evidence.
4. Bespok3d installs the three Klipper extras, renders the configuration,
   restarts Klipper, and rolls back automatically if Klipper fails to return.
5. Confirm Klipper reports **Ready** before attempting to home or move.

## Validate after installation

With the printer clear of obstructions, inspect the Klipper log for
`autotune_tmc set stepper_x`, `stepper_y`, and `stepper_z` entries. Then query:

```gcode
DUMP_TMC STEPPER=stepper_x
DUMP_TMC STEPPER=stepper_y
DUMP_TMC STEPPER=stepper_z
```

Perform the first home with a hand near the power switch and stop immediately if
an axis fails to trigger normally. Do not begin a print until X, Y, and Z homing
have each been verified.

## Reconfigure or remove

Change the printer-scoped motor values through Bespok3d's plugin configuration;
it will rerender the file and restart Klipper. Uninstalling the plugin removes
the managed extras and configuration include, then restarts Klipper with the
stock driver settings.
