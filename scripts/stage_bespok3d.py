#!/usr/bin/env python3
"""Assemble canonical TMC Autotune source into a b3-builder input directory."""

from __future__ import annotations

import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SOURCE = REPO_ROOT / "bespok3d" / "u1-klipper-tmc-autotune"
STAGE_ROOT = REPO_ROOT / "dist" / "u1-klipper-tmc-autotune"
UPSTREAM_FILES = ("autotune_tmc.py", "motor_constants.py", "motor_database.cfg")


def stage() -> Path:
    if STAGE_ROOT.exists():
        shutil.rmtree(STAGE_ROOT)

    shutil.copytree(PACKAGE_SOURCE, STAGE_ROOT)
    extras = STAGE_ROOT / "files" / "klipper" / "klippy" / "extras"
    extras.mkdir(parents=True, exist_ok=True)
    for filename in UPSTREAM_FILES:
        shutil.copy2(REPO_ROOT / filename, extras / filename)

    shutil.copy2(REPO_ROOT / "LICENSE", STAGE_ROOT / "LICENSE")
    shutil.copy2(REPO_ROOT / "LICENSE", STAGE_ROOT / "doc" / "LICENSE")
    shutil.copy2(
        REPO_ROOT / "docs" / "SNAPMAKER_U1.md", STAGE_ROOT / "doc" / "README.md"
    )
    return STAGE_ROOT


if __name__ == "__main__":
    print(stage())
