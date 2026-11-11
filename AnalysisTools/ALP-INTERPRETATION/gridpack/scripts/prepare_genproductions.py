#!/usr/bin/env python3
"""Install the curated cards and UFO into a fresh, pinned genproductions checkout."""
import argparse
from pathlib import Path
import shutil
import subprocess

REVISION = "082de8dc377f80fb3d867e0192feafe3a563e848"
SCRIPT = Path("bin/MadGraph5_aMCatNLO/gridpack_generation.sh")
ANCHOR = "      ./bin/mg5_aMC mgconfigscript\n"
HOOK = '\n      # Local ALP model snapshot\n      cp -R "$PRODHOME/extra_models/axion_UFO" models/\n'


def prepare(checkout):
    root = Path(__file__).resolve().parents[2]
    checkout = checkout.resolve()
    revision = subprocess.check_output(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True
    ).strip()
    if revision != REVISION:
        raise ValueError(f"Expected genproductions revision {REVISION}, found {revision}")
    original = subprocess.check_output(
        ["git", "-C", str(checkout), "show", f"HEAD:{SCRIPT.as_posix()}"], text=True
    )
    if original.count(ANCHOR) != 1:
        raise ValueError("Expected exactly one model setup location in the pinned script")
    patched = original.replace(ANCHOR, ANCHOR + HOOK)
    target_script = checkout / SCRIPT
    if target_script.read_text() not in (original, patched):
        raise ValueError("gridpack_generation.sh has other edits; use a fresh checkout")
    production = target_script.parent
    copies = []
    for src in sorted((root / "gridpack/cards").glob("*/*.dat")):
        copies.append((src, production / "cards/production/13TeV" / src.parent.name / src.name))
    for src in sorted((root / "models/axion_UFO").glob("*.py")):
        copies.append((src, production / "extra_models/axion_UFO" / src.name))
    # Check conflicts before making any changes.
    for src, dst in copies:
        if dst.exists() and dst.read_bytes() != src.read_bytes():
            raise ValueError(f"Refusing to replace a different existing file: {dst}")
    for src, dst in copies:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    target_script.write_text(patched)
    print(f"Prepared {len(copies)} card/model files in {production}")
    print("No gridpack production was launched.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkout", type=Path, help="Fresh genproductions checkout at the documented revision")
    args = parser.parse_args()
    try:
        prepare(args.checkout)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Preparation failed: {exc}\n")
