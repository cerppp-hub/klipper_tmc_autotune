# Snapmaker U1 installation and configuration

This branch packages Klipper TMC Autotune for a Snapmaker U1 whose X and Y
motors have been upgraded to LDO-42STH48-2504MACF units. It uses Bespok3d for
the U1's appliance-style Klipper layout. Do not run upstream `install.sh` on
the printer.

## Scope

- X and Y: LDO-42STH48-2504MACF, driven by the stock TMC2240 drivers.
- Z: not tuned; the stock TMC2209 configuration remains active.
- Toolhead extruders: not tuned.
- Goal: `auto`, which resolves to performance/SpreadCycle for X and Y.
- Sensorless homing: stock TMC2240 SGT path, `sgt: 1`, `sg4_thrs: 0`.
- Small hysteresis: enabled for X and Y.

The motor is already present in upstream `motor_database.cfg` with these
published constants:

| Resistance | Inductance | Holding torque | Rated current | Full steps/revolution |
| ---: | ---: | ---: | ---: | ---: |
| 1.2 ohms | 1.5 mH | 0.45 Nm | 2.5 A | 400 (0.9 degree) |

The package does not change the U1's configured X/Y `run_current`. Confirm that
the current is appropriate for the installed motors and mechanical load before
high-speed testing.

## TOFF persistence update

The packaged upstream snapshot is commit
`b6c7cfa98c2ef880812d5279a9117cbe67d6d4d5`. It includes commit
`a4f4daa0b3512b751bb95cd20759e36a4963c25f`, which fixes tuned TOFF values being
replaced by Klipper's earlier virtual-enable snapshot when a stepper is
re-enabled.

## Runtime tuning and raw TMC fields

Autotune-managed parameters should be changed through `AUTOTUNE_TMC`, which
updates Autotune's in-memory state and immediately retunes the driver:

```gcode
AUTOTUNE_TMC STEPPER=stepper_x SMALL_HYSTERESIS=0
AUTOTUNE_TMC STEPPER=stepper_y SMALL_HYSTERESIS=0
```

Use `SMALL_HYSTERESIS=1` to enable it again. `TOFF`, `TBL`, `TPFD`,
`EXTRA_HYSTERESIS`, `SGT`, and other supported Autotune parameters can be
supplied on the same command.

The U1 Klipper build also exposes every writable field registered by its
TMC2240 driver through the standard command:

```gcode
SET_TMC_FIELD STEPPER=stepper_x FIELD=en_pwm_mode VALUE=0
SET_TMC_FIELD STEPPER=stepper_y FIELD=en_pwm_mode VALUE=0
SET_TMC_FIELD STEPPER=stepper_x FIELD=small_hysteresis VALUE=1
```

`SET_TMC_FIELD` is a direct runtime register write. It is not saved to the
configuration, and an Autotune rerun, homing transition, driver reset, Klipper
restart, or stepper re-enable may restore an Autotune- or Klipper-managed value.
In particular, change TOFF with `AUTOTUNE_TMC ... TOFF=<value>` rather than a raw
field write so the TOFF persistence handler retains the intended value.

Arbitrary TMC field writes can disable protection or motion-control behavior.
Change one field at a time, record the prior `DUMP_TMC` output, and keep access
to the power switch.

## Install

1. Confirm both X/Y motor labels and wiring match LDO-42STH48-2504MACF.
2. Make sure the printer is idle and cool.
3. In Bespok3d Desktop, choose **Add plugin from file** and select
   `u1-klipper-tmc-autotune-0.2.0-u1.5.b3`.
4. Let Bespok3d install the three Klipper extras and X/Y configuration, then
   restart Klipper.
5. Confirm Klipper reports **Ready** before attempting to home or move.

## Validate

Confirm the Klipper log contains Autotune entries for `stepper_x` and
`stepper_y`, but not `stepper_z`. Save the initial register state:

```gcode
DUMP_TMC STEPPER=stepper_x
DUMP_TMC STEPPER=stepper_y
```

Perform the first home with the motion area clear and a hand near the power
switch. Test low-speed moves first, then increase speed and acceleration while
monitoring motor and TMC2240 temperatures. Do not print until repeated X/Y
homing is reliable and no steps are lost.

## Sources

- [Klipper TMC Autotune upstream](https://github.com/andrewmcgr/klipper_tmc_autotune)
- [Upstream motor database entry](https://github.com/andrewmcgr/klipper_tmc_autotune/blob/main/motor_database.cfg)
- [Klipper configuration reference](https://www.klipper3d.org/Config_Reference.html#tmc2240)
