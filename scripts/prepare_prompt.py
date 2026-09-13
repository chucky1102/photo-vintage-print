#!/usr/bin/env python3
"""Copy the default creative recipe without rewriting it or overwriting a run."""
import argparse
import hashlib
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / "references/original-prompt.md"
    data = source.read_bytes()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("xb") as target:
        target.write(data)
    assert args.output.read_bytes() == data
    print(f"Saved unchanged prompt: {args.output}")
    print(f"SHA256: {hashlib.sha256(data).hexdigest()}")

if __name__ == "__main__":
    main()
