#!/usr/bin/env python3
"""TEST03D: binary-only N default patch of exact VICE-PASS TEST03A build.

The test03A original assembler output must match the SHA-256 of the build
previously tested on VICE. Exactly TWO bytes are changed; no shift,
no reassembly, no relocation and no Krill code change.

start at $C81E, source:
  ldx #$02
  stx plt_flag          ; $0159
  lda #$4D             ; M
  sta plt_letter        ; $015A
becomes:
  ldx #$00
  stx plt_flag
  lda #$4E             ; N
  sta plt_letter
"""
from pathlib import Path
import hashlib
import sys

EXPECTED_SHA256 = "a1f4f8be45d4677f00cf3f4b386eb0b11b8282af5fdf31032e7012f9e9cbc389"
BEFORE = bytes.fromhex("a2 02 8e 59 01 a9 4d 8d 5a 01")
AFTER  = bytes.fromhex("a2 00 8e 59 01 a9 4e 8d 5a 01")
START = 0xC81E

def patch(original: bytes) -> bytes:
    checksum = hashlib.sha256(original).hexdigest()
    if checksum != EXPECTED_SHA256:
        raise SystemExit(f"STOP: build != confirmed TEST03A baseline: {checksum}")
    load_address = int.from_bytes(original[:2], "little")
    offset = START - load_address + 2
    if original[offset:offset + len(BEFORE)] != BEFORE:
        raise SystemExit("STOP: entry does not contain TEST03A original M-init bytes")
    if original.count(BEFORE) != 1:
        raise SystemExit("STOP: signature not unique")
    updated = original[:offset] + AFTER + original[offset + len(BEFORE):]
    differences = [n for n,(a,b) in enumerate(zip(original,updated)) if a != b]
    assert len(original) == len(updated)
    assert differences == [offset+1,offset+6], differences
    print(f"TEST03D patch PASS: exact 2 bytes at file offsets "
          f"${offset+1:04X}, ${offset+6:04X}; "
          f"runtime address ${START:04X}; {len(updated)} B")
    return updated

if __name__ == "__main__":
    if len(sys.argv)!=3:
        raise SystemExit("Usage: python tools/test03d_bytepatch.py ORIGINAL.o64 NEXT.o64")
    src,dst=map(Path,sys.argv[1:])
    dst.write_bytes(patch(src.read_bytes()))
