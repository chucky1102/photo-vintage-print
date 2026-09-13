#!/usr/bin/env python3
"""Validate the distributable photo-vintage-print skill without network access."""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "SKILL.md",
    "README.md",
    "VERSION",
    "LICENSE",
    "agents/openai.yaml",
    ".github/workflows/validate.yml",
    "references/original-prompt.md",
    "references/original-prompt.sha256",
    "references/print-controls.md",
    "references/quality-check.md",
    "scripts/prepare_prompt.py",
    "THIRD_PARTY_NOTICES.md",
    "LICENSE.baoyu-cover-image",
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    missing = [relative for relative in REQUIRED if not (ROOT / relative).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail("VERSION must use MAJOR.MINOR.PATCH format")

    skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    if "name: photo-vintage-print" not in skill_text:
        fail("SKILL.md name does not match the folder")

    interface_text = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
    if "$photo-vintage-print" not in interface_text:
        fail("agents/openai.yaml default_prompt must mention $photo-vintage-print")

    lock_line = (ROOT / "references/original-prompt.sha256").read_text(
        encoding="utf-8"
    ).strip()
    expected_hash = lock_line.split()[0] if lock_line else ""
    actual_hash = sha256(ROOT / "references/original-prompt.md")
    if expected_hash != actual_hash:
        fail(
            "original-prompt.md changed; review it deliberately and update the lock "
            f"only after approval (expected {expected_hash}, got {actual_hash})"
        )

    with tempfile.TemporaryDirectory(prefix="photo-vintage-print-") as temp_dir:
        copied_prompt = Path(temp_dir) / "prompts/01-final.md"
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/prepare_prompt.py"),
                "--output",
                str(copied_prompt),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            fail("prepare_prompt.py failed: " + result.stderr.strip())
        if copied_prompt.read_bytes() != (ROOT / "references/original-prompt.md").read_bytes():
            fail("prepare_prompt.py output is not byte-identical to original-prompt.md")

    print(f"PASS: photo-vintage-print {version}")
    print(f"PASS: {len(REQUIRED)} required files")
    print(f"PASS: original Prompt SHA256 {actual_hash}")
    print("PASS: prepare_prompt.py produced a byte-identical copy")


if __name__ == "__main__":
    main()
