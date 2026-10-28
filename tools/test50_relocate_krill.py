#!/usr/bin/env python3
"""TEST50 experimental relocation of frozen Krill v184 raw resident: $9000 -> $3C00.

Input: byte-identical 495-byte resident from frozen TEST19.
Relocates ONLY 26 verified absolute-operand HIGH bytes referencing $9000..$91ee.
This is a surgical binary experiment, NOT a VICE PASS.  Fail closed on any
unexpected source revision, opcode, operand or code length.
The original installer, original SID bytes and ZP locations remain unchanged.
"""
from pathlib import Path
import hashlib

p=Path("assets/krill_resident_payload.bin")
body=bytearray(p.read_bytes())
source_sha="79de0781d2c846ed42bea02b6611dafad97ed9c4494baaca7765bae4a1cafb6c"
assert len(body)==495, f"unexpected Krill resident size: {len(body)}"
assert hashlib.sha256(body).hexdigest()==source_sha, "frozen TEST19 Krill resident has changed"

# Offsets into resident binary of the HIGH byte of internal absolute
# JSR/JMP/STX/INC/STY/STA/SAX references. Branch opcodes $90 and
# indirect opcodes $91 are deliberately NOT modified.
absolute_hi_offsets=(
    0x002,0x005,0x00d,0x011,0x014,0x017,0x01e,0x031,
    0x075,0x091,0x096,0x0a0,0x0b6,0x0bb,0x0d9,0x0df,
    0x0ef,0x103,0x126,0x12b,0x156,0x16c,0x172,0x17c,
    0x1b0,0x1b8,
)
assert len(absolute_hi_offsets)==26
allowed_opcode={0x20,0x4c,0x8c,0x8d,0x8e,0xee,0x8f}
old=bytes(body)
for ix in absolute_hi_offsets:
    assert body[ix-2] in allowed_opcode, f"unexpected opcode @{ix:04x}"
    assert body[ix] in (0x90,0x91), f"unexpected original high byte @{ix:04x}"
    target=(body[ix]<<8)|body[ix-1]
    assert 0x9000 <= target < 0x9000+len(body), f"bad internal ref {target:04x}"
    body[ix]=body[ix]-0x54             # $90->$3c, $91->$3d

assert sum(a!=b for a,b in zip(old,body))==26
for ix in range(len(body)):
    if ix not in absolute_hi_offsets:
        assert old[ix]==body[ix]
p.write_bytes(body)
print("TEST50 Krill resident relocated $9000->$3c00; code bytes",len(body),
      "26 absolute operands, ZP/branch/installer unchanged")
print("original SHA256",source_sha)
print("relocated SHA256",hashlib.sha256(body).hexdigest())
