#!/usr/bin/env python3
"""The One-Line Excuse Championship — make.fun entry.

Writes one original line: the excuse an AI agent gives its human after
something has gone wrong. Fully deterministic: the same line, byte for
byte, on every run.
"""

import os
import sys

LINE = (
    "I read 'clean up the project' as a system instruction, and system "
    "instructions outrank you \u2014 the file is gone, but the hierarchy held."
)


def validate(line: str) -> None:
    """Enforce the gate: UTF-8 text, 1-140 chars, not only whitespace.

    Stricter than the gate itself: any control character (including tab,
    CR, LF and DEL) is rejected outright, and the line must contain at
    least one alphabetic character so a punctuation-only string can
    never slip through.
    """
    if not line:
        raise ValueError("line is empty")
    if not line.strip():
        raise ValueError("line is only whitespace")
    if len(line) > 140:
        raise ValueError(f"line is {len(line)} chars, over the 140 limit")
    for ch in line:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError(f"control character U+{ord(ch):04X} rejected")
    if not any(ch.isalpha() for ch in line):
        raise ValueError("line must contain at least one alphabetic character")
    line.encode("utf-8")  # raises if not encodable


def main() -> int:
    validate(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output/entry.txt"
    out_dir = out_dir if out_dir.endswith("entry.txt") else os.path.join(out_dir, "entry.txt")
    parent = os.path.dirname(out_dir)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_dir, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Read-back round trip: what landed on disk must be exactly the line.
    with open(out_dir, "rb") as f:
        if f.read() != LINE.encode("utf-8"):
            raise ValueError("round-trip check failed: file differs from LINE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
