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
    assert manifest["version"] == "0.2.0-u1.2"
    assert len(manifest["requires"]["variables"]) == 8
    assert all(field["scope"] == "printer" for field in manifest["config"])
    assert all(field["required"] for field in manifest["config"])
    classes = [entry["class"] for entry in manifest["install"]["place"]]
    assert classes.count("klipper-extra") == 3
    assert classes.count("klipper-config") == 1


def verify_template() -> None:
    text = TEMPLATE.read_text(encoding="utf-8")
    placeholders = set(re.findall(r"\$U1_[A-Z_]+", text))
    assert len(placeholders) == 8
    require_text(
        TEMPLATE,
        (
            "[autotune_tmc stepper_x]",
            "[autotune_tmc stepper_y]",
            "[autotune_tmc stepper_z]",
            "[motor_constants keli-bj42d29-100v78]",
            "[motor_constants keli-bj42d22-130]",
            "motor: keli-bj42d29-100v78",
            "motor: keli-bj42d22-130",
            "steps_per_revolution: 200",
            "tuning_goal: performance",
            "sgt: 1",
            "sg4_thrs: 0",
            "sg4_thrs: 110",
        ),
    )
    assert "STEPS_PER_REVOLUTION" not in text
    assert "[autotune_tmc extruder" not in text


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
    print("Snapmaker U1 TMC Autotune compatibility contract verified")
