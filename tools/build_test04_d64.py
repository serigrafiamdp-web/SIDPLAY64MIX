#!/usr/bin/env python3
"""Build TEST04 D64 from original user-supplied SIPLAY.d64, without Krill.
No SID code is relocated: only its file load address is changed for DATA
staging; playback copies code to original $1000 before INIT=$1000/PLAY=$1003.
"""
from argparse import ArgumentParser
from pathlib import Path
from build_test02_d64 import build,offset
from test02_synthetic_tunes import tune

SLOTS = [
    ("RAM_A", 0x7000, "MINIMERCADO.SID"),
    ("RAM_B", 0x3000, "CHACABEZA.SID"),
    ("RAM_C", 0x5000, "COMEME (1).SID"),
]
CACHE_BYTES = 0x1300

def read_d64(d):
    assert len(d)==174848
    t,s=18,1
    result={}
    seen_dirs=set()
    while t:
        assert (t,s) not in seen_dirs
        seen_dirs.add((t,s))
        p=offset(t,s)
        for i in range(8):
            a=p+i*32
            if not d[a+2]&0x80: continue
            name=d[a+5:a+21].rstrip(b"\xa0").decode("latin1")
            f,g=d[a+3:a+5]
            blob=bytearray()
            seen=set()
            while f:
                assert (f,g) not in seen
                seen.add((f,g))
                q=offset(f,g)
                nf,ng=d[q:q+2]
                blob+=d[q+2:q+2+(254 if nf else ng-1)]
                f,g=nf,ng
            result.setdefault(name,bytes(blob))
        t,s=d[p:p+2]
    return result

def data_only_psid(song,bank):
    assert song[:4]==b"PSID"
    assert song[4:6]==b"\x00\x02" and song[6:8]==b"\x00\x7c"
    assert song[8:10]==b"\x00\x00"
    assert song[10:14]==b"\x10\x00\x10\x03"
    assert song[18:22]==b"\xff\xff\xff\xff"
    assert song[0x7c:0x7e]==b"\x00\x10"
    raw=song[0x7e:]
    assert 0<len(raw)<=CACHE_BYTES
    print("Cache $%04X: %d SID bytes" % (bank,len(raw)))
    return bank.to_bytes(2,"little")+raw.ljust(CACHE_BYTES,b"\x00")

def main():
    ap=ArgumentParser()
    ap.add_argument("--main",required=True,type=Path)
    ap.add_argument("--source-d64",type=Path)
    ap.add_argument("--out",required=True,type=Path)
    x=ap.parse_args()
    program=x.main.read_bytes()
    assert program[:2]==b"\x01\x08"
    assert len(program)<0x1000-0x0801+2
    songs=read_d64(x.source_d64.read_bytes()) if x.source_d64 else {}
    entries=[("RAM_PLAYER",program)]
    for i,(name,bank,sidname) in enumerate(SLOTS):
        if x.source_d64:
            entries.append((name,data_only_psid(songs[sidname],bank)))
        else:
            synthetic=tune([0x18,0x78,0xd8][i])
            entries.append((name,bank.to_bytes(2,"little")+
                       synthetic[2:].ljust(CACHE_BYTES,b"\x00")))
    data=build(entries,title="SID MIX RAM TEST4")
    assert len(data)==174848
    assert read_d64(data)==dict(entries)
    x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_bytes(data)
    print("D64 PASS, player and 3 RAM-cached tunes:",x.out)

if __name__=="__main__":
    main()
