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

## Why some motor constants are still required

TMC Autotune also needs each motor's phase resistance, phase inductance, holding
torque, and rated current. Those values cannot be recovered from Klipper's
`run_current`. Keli's public BJ42D table documents standard windings but does
not list the custom `-100V78` or `-130` performance/mechanical variants. A
generic BJ42D29 or BJ42D22 row is therefore not a verified substitute.

Before installation, obtain the four exact electrical values for each named
motor from its OEM sheet or measurements. Enter inductance in **henries**,
torque in **newton-metres**, and current in **amperes**. The form intentionally
does not suggest values from a different winding.

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
   `u1-klipper-tmc-autotune-0.2.0-u1.2.b3` package.
3. Confirm the motor labels match the supported mapping and enter the eight
   electrical values. Do not use values from a generic BJ42D table row.
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
