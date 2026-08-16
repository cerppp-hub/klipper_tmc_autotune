from __future__ import annotations

import ast
import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
U1_ROOT = Path(
    os.environ.get("U1_KLIPPER_ROOT", REPO_ROOT.parent / "u1-klipper")
).resolve()
PACKAGE_ROOT = REPO_ROOT / "bespok3d" / "u1-klipper-tmc-autotune"
TEMPLATE = (
    PACKAGE_ROOT / "files" / "cfg" / "klipper" / "u1-klipper-tmc-autotune.cfg.tmpl"
)


def require_text(path: Path, fragments: tuple[str, ...]) -> None:
    text = path.read_text(encoding="utf-8")
    missing = [fragment for fragment in fragments if fragment not in text]
    if missing:
        raise AssertionError(f"{path} is missing required U1 APIs/settings: {missing}")


def compile_upstream_python() -> None:
    for filename in ("autotune_tmc.py", "motor_constants.py"):
        path = REPO_ROOT / filename
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def verify_manifest() -> None:
    manifest = json.loads((PACKAGE_ROOT / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["channel"] == "experiment"
    assert manifest["install"]["restart"] == ["klipper"]
    assert manifest["version"] == "0.2.0-u1.5"
    assert manifest["sw_version"] == "0.2.0+git.b6c7cfa.u1.1"
    assert manifest["requires"]["variables"] == []
    assert manifest["config"] == []
    classes = [entry["class"] for entry in manifest["install"]["place"]]
    assert classes.count("klipper-extra") == 3
    assert classes.count("klipper-config") == 1


def verify_template() -> None:
    text = TEMPLATE.read_text(encoding="utf-8")
    placeholders = set(re.findall(r"\$U1_[A-Z_]+", text))
    assert placeholders == set()
    require_text(
        TEMPLATE,
        (
            "[autotune_tmc stepper_x]",
            "[autotune_tmc stepper_y]",
            "motor: ldo-42sth48-2504macf",
            "tuning_goal: auto",
            "small_hysteresis: True",
            "sgt: 1",
            "sg4_thrs: 0",
        ),
    )
    assert "[autotune_tmc stepper_z]" not in text
    assert "[autotune_tmc extruder" not in text


def verify_u1_runtime_field_access() -> None:
    require_text(
        REPO_ROOT / "autotune_tmc.py",
        (
            'config.getboolean(\n            "small_hysteresis"',
            'gcmd.get_int("SMALL_HYSTERESIS", None)',
            'self._set_driver_field("small_hysteresis", self.small_hysteresis)',
            "see GH-354",
        ),
    )
    require_text(
        REPO_ROOT / "motor_database.cfg",
        (
            "[motor_constants ldo-42sth48-2504macf]",
            "holding_torque: 0.45",
            "steps_per_revolution: 400",
        ),
    )
    require_text(
        U1_ROOT / "klippy" / "extras" / "tmc.py",
        (
            'gcode.register_mux_command("SET_TMC_FIELD"',
            "reg_name = self.fields.lookup_register(field_name, None)",
            "reg_val = self.fields.set_field(field_name, value)",
        ),
    )
    require_text(
        U1_ROOT / "klippy" / "extras" / "tmc2240.py",
        ('"en_pwm_mode":', '"small_hysteresis":'),
    )


def verify_u1_contract() -> None:
    require_text(
        U1_ROOT / "lava" / "printer.cfg",
        (
            "kinematics: corexy",
            "[tmc2240 stepper_x]",
            "[tmc2240 stepper_y]",
            "[tmc2209 stepper_z]",
            "driver_SGT: 1",
            "driver_SGTHRS: 110",
            "run_current: 1.2",
            "run_current: 0.85",
        ),
    )
    require_text(
        U1_ROOT / "klippy" / "extras" / "tmc.py",
        (
            "class TMCCommandHelper:",
            "self.current_helper = current_helper",
            "def get_status(self, eventtime=None):",
            "def TMCtstepHelper",
        ),
    )
    require_text(
        U1_ROOT / "klippy" / "extras" / "tmc2240.py",
        (
            "class TMC2240CurrentHelper:",
            "def get_current(self):",
            "TMC_FREQUENCY=12500000.",
            "def load_config_prefix(config):",
        ),
    )


if __name__ == "__main__":
    compile_upstream_python()
    verify_manifest()
    verify_template()
    verify_u1_contract()
    verify_u1_runtime_field_access()
    print("Snapmaker U1 TMC Autotune compatibility contract verified")
