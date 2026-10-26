#!/usr/bin/env python3
"""Build 3 tiny synthetic 60-Hz SID-like test tunes, not copyrighted SID rips.

Each has INIT=$1000, PLAY=$1003; different base-frequency per slot.
These provide only an observable audio baseline for loader integration.
They are NOT substitutes for real PSID compatibility tests.
"""
from pathlib import Path
import argparse

def tune(low: int) -> bytes:
    # $1000 JMP init($1006); $1003 JMP play($102A)
    blob=bytearray([0x4c,0x06,0x10,0x4c,0x2a,0x10])
    for value,reg in [(0,0xd404),(low,0xd400),(8,0xd401),
                      (0xf0,0xd405),(0xe5,0xd406),
                      (0x21,0xd404),(0x0f,0xd418)]:
        blob+=bytes([0xa9,value,0x8d,reg&255,reg>>8])
    blob+=bytes([0x60])
    assert len(blob)==0x2a
    blob+=bytes([0xee,0x00,0xd4,0x60])
    return bytes([0,0x10])+blob

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("out",type=Path)
    x=parser.parse_args()
    x.out.mkdir(parents=True,exist_ok=True)
    for slot,low in zip("ABC",(0x18,0x78,0xd8)):
        p=x.out/("MIX_"+slot+".PRG")
        addr=0x1000 if slot=="A" else 0x5000
        data=tune(low)
        p.write_bytes(bytes([addr&255,addr>>8])+data[2:])
        print(p, "load",hex(addr), "bytes",p.stat().st_size)

if __name__=="__main__":
    main()
