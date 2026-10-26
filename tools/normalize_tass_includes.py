#!/usr/bin/env python3
"""Normalize Glenn-era unquoted 64tass include/binary paths for current 64tass.

BUILD-TIME TRANSFORM ONLY. Run in a checked-out build workspace, not on
user's master sources. Only rewrites .include/.binary operands beginning with
a bare path, never modifies existing quoted strings or assembly behavior.
"""
from pathlib import Path
import re

PATTERN = re.compile(
    r'(?im)^(\s*\.(?:include|binary)\s+)(?!["\'])([A-Za-z_][A-Za-z0-9_./\\-]*)'
)

def normalize(root: Path) -> tuple[int, int]:
    modified = 0
    total = 0
    for file in [root / "sidplay64.tas", *root.rglob("*.tas")]:
        if not file.exists():
            continue
        data = file.read_bytes()
        raw = data.decode("latin1")
        def fix(match: re.Match[str]) -> str:
            nonlocal total
            total += 1
            return match.group(1) + '"' + match.group(2).replace("\\", "/") + '"'
        changed = PATTERN.sub(fix, raw)
        if changed != raw:
            file.write_bytes(changed.encode("latin1"))
            modified += 1
    return modified, total

if __name__ == "__main__":
    changed, directives = normalize(Path("."))
    print(f"64tass build normalization: {changed} files, {directives} operands")
