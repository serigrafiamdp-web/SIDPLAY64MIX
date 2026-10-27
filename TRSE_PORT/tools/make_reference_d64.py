#!/usr/bin/env python3
"""Build a canonical, simple 35-track CBM DOS 2.6 D64.

This disk is a REFERENCE smoke test for the unmodified Glenn binary.
No SIDPLAY64 code, data, or callbacks are patched.
"""
from pathlib import Path
from math import ceil
import argparse
import hashlib

SPT = {t: 21 if t <= 17 else 19 if t <= 24 else 18 if t <= 30 else 17
       for t in range(1, 36)}
SIZE = 256 * sum(SPT.values())
assert SIZE == 174848

def position(track, sector):
    assert track in SPT and 0 <= sector < SPT[track]
    return 256 * (sum(SPT[t] for t in range(1, track)) + sector)

def petscii(name, size=16):
    name = name.upper().encode("ascii")
    if len(name) > size:
        raise ValueError("C64 filename too long: " + repr(name))
    return name.ljust(size, b"\xa0")

def build(output_path, title, files):
    disk = bytearray(SIZE)
    used = {(18, 0)}
    pool = [(t, s) for t in list(range(17, 0, -1)) +
            list(range(19, 36)) for s in range(SPT[t])]
    index = 0

    def allocate():
        nonlocal index
        if index >= len(pool):
            raise ValueError("D64 full")
        item = pool[index]
        index += 1
        assert item not in used
        used.add(item)
        return item

    directories = [(18, s) for s in range(1, 19)]
    directory_count = ceil(len(files) / 8)
    if directory_count > len(directories):
        raise ValueError("Too many directory entries")
    for i in range(directory_count):
        t, s = directories[i]
        used.add((t, s))
        offset = position(t, s)
        if i + 1 < directory_count:
            disk[offset:offset+2] = bytes((18, s+1))
        else:
            disk[offset:offset+2] = b"\x00\xff"

    report = []
    for i, (name, payload) in enumerate(files):
        if not payload:
            raise ValueError("Empty file " + name)
        segments = [payload[j:j+254] for j in range(0, len(payload), 254)]
        chain = [allocate() for _ in segments]
        for n, ((t, s), fragment) in enumerate(zip(chain, segments)):
            offset = position(t, s)
            if n+1 < len(chain):
                disk[offset:offset+2] = bytes(chain[n+1])
            else:
                disk[offset:offset+2] = bytes((0, len(fragment)+1))
            disk[offset+2:offset+2+len(fragment)] = fragment

        dt, ds = directories[i // 8]
        entry = position(dt, ds) + (i % 8) * 32
        disk[entry+2] = 0x82   # CLOSED PRG
        disk[entry+3:entry+5] = bytes(chain[0])
        disk[entry+5:entry+21] = petscii(name)
        disk[entry+30:entry+32] = len(chain).to_bytes(2, "little")
        report.append((name, len(payload), len(chain), chain[0]))

    # Disk BAM, track 18 sector 0
    bam = position(18, 0)
    disk[bam:bam+4] = bytes((18, 1, 0x41, 0x00))
    for t in range(1, 36):
        available = [(t, s) for s in range(SPT[t]) if (t, s) not in used]
        bits = bytearray(3)
        for _, s in available:
            bits[s // 8] |= 1 << (s % 8)
        q = bam + 4 + (t-1)*4
        disk[q:q+4] = bytes([len(available), *bits])
    disk[bam+0x90:bam+0xa0] = petscii(title)
    disk[bam+0xa2:bam+0xa4] = b"GR"
    disk[bam+0xa5:bam+0xa7] = b"2A"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_bytes(disk)
    assert len(disk) == SIZE
    # Re-read every file from the actual linked sectors to validate output.
    for (name, payload), (_, _, count, start) in zip(files, report):
        t, s = start
        found = bytearray()
        hops = 0
        while t:
            p = position(t, s)
            nt, ns = disk[p], disk[p+1]
            found += disk[p+2:p+256] if nt else disk[p+2:p+ns+1]
            t, s = nt, ns
            hops += 1
            assert hops <= count
        assert found == payload, (name, len(found), len(payload))
    print("BUILT", output_path, "files", len(report),
          "sha256", hashlib.sha256(disk).hexdigest())
    for rec in report:
        print(" ", *rec)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--prg", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()
    folder = Path(args.source)
    songs = [
        ("SHAPE.SID", "shape.sid"),
        ("DEFLEKTOR.SID", "deflektor.sid"),
        ("DEATHWISH3.SID", "deathwish3.sid"),
        ("HARDBALL.SID", "hardball.sid"),
        ("HOCUSFOCUS.SID", "hocus_focus.sid"),
        ("LAW_OF_WEST.SID", "law_of_the_west.sid"),
        ("MAGICSS.SID", "magicss.sid"),
        ("NINJA_SPRT.SID", "ninja_spirit.sid"),
    ]
    files = [("SIDPLAY64", Path(args.prg).read_bytes())]
    for name, file in songs:
        path = folder / "sids" / file
        if not path.is_file():
            raise FileNotFoundError(str(path))
        files.append((name, path.read_bytes()))
    build(args.output, args.title, files)

if __name__ == "__main__":
    main()
