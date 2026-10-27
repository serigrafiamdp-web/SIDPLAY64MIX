#!/usr/bin/env python3
"""TEST28: embed exact TEST19 FIX bootstrap and TEST25 generic ENGINE into one PRG."""
from pathlib import Path
import hashlib,base64
from test27_pack import files

ENGINE_B64 = """ADapE40YNKkTjXw0qcyNQzSpNo1ENKm5jUc0qTaNSDSppo3pNKk2jeo0qUmNSzSpNo1MNKnwjTM0qT+NNDSp8Y08NKk/jT00TACQrjk1vcw2qL25NqogAJCwS61QU8lJ0EStUVPJRNA9rVZT0DitV1PQM61VUxhpUI2RNq1UU2lTjZI2rjk1vaY2qqlQjZU2oAC5AACZAFDI0PfukjbulTbK0OwYYDhgDxITEg8NExIUEBESExMaDBMSEt/v/QwaKjdATVxqdIWRoa+7zNc2NjY3Nzc3Nzc3Nzc3Nzc3TUlOSU1FUkNBRE8uU0lEAENIQUNBQkVaQS5TSUQAQ09NRU1FICgxKS5TSUQAREFUQVNFVFRFLlNJRABEUk9HQUNVTUJJQS5TSUQARVNQQUNJQUwuU0lEAENBUkEuU0lEAE1BVFJBQ0EzLlNJRABNT05HT0xPTkdPLlNJRABQRVJST0NVTE8uU0lEAFBPUlJPLlNJRABJTkRJRUNJVE8gREUuU0lEAEpVQU5FTE8uU0lEAFBPV0VSIFBPV0VSLlNJRABQU0NJSURTSzIuU0lEAFJBUENJVE8uU0lEAFNJRU1QUkUgRU4gTS5TSUQAVFVSUk8xLlNJRABUVVJST1JFR0dBRSAuU0lEAA=="""
MASTER_SHA = "b247f58ce9d3df87025d0f09ca145998bffe31e8f9e520c5c29dcfc238d66cc5"
ENGINE_SHA = "61fd232ea9365c4e8d8f03348a0a6fa258b1a7cf0a65d1f527a328f4fc832159"

def main():
    image=Path("frozen-master/MASTERS/2026-10-27_PASS/TEST19_MULTIPLES_ARCHIVOS_KRILL_5_SEGUNDOS.d64").read_bytes()
    assert hashlib.sha256(image).hexdigest()==MASTER_SHA
    original=dict(files(image))
    installer=original["INSTA"]
    resident=original["RESIDENT"]
    fix=bytearray(original["FIX"])
    engine=base64.b64decode(ENGINE_B64)
    assert engine[:2]==bytes((0,0x36)) and len(engine)==490
    assert hashlib.sha256(engine).hexdigest()==ENGINE_SHA
    assert installer[:2]==bytes((0,0x60)) and len(installer)==6888
    assert resident[:2]==bytes((0,0x90)) and len(resident)==497
    assert fix[:2]==bytes((0,5)) and len(fix)==549
    # TEST19 FIX installs original callbacks, then jumps to Glenn at $9000.
    # Replace only that final JMP with JMP $3600, where TEST25 engine
    # is now EMBEDDED and patches a generic 19-SID directory loader.
    offset=2+(0x0563-0x0500)
    assert fix[offset:offset+3]==bytes((0x4c,0x00,0x90))
    fix[offset:offset+3]=bytes((0x4c,0x00,0x36))
    assert fix[2+(0x058a-0x0500):2+(0x0590-0x0500)]==bytes((0xad,0x09,0xdc,0xc9,0x05,0x90)), "TEST19 5s hook altered"
    Path("assets").mkdir(exist_ok=True)
    Path("assets/test28_fix_embedded.bin").write_bytes(fix[2:])
    Path("assets/test28_engine_embedded.bin").write_bytes(engine[2:])
    Path("assets/krill_insta_payload.bin").write_bytes(installer[2:])
    Path("assets/krill_resident_payload.bin").write_bytes(resident[2:])
    for f in ["test28_fix_embedded.bin","test28_engine_embedded.bin","krill_insta_payload.bin","krill_resident_payload.bin"]:
        p=Path("assets")/f
        print(f,len(p.read_bytes()),hashlib.sha256(p.read_bytes()).hexdigest())
    print("TEST28 PASS assets: TEST19 FIX hook at $0580, engine $3600, init $6000, resident backup $8800; 1 PRG")

if __name__=="__main__":
    main()
