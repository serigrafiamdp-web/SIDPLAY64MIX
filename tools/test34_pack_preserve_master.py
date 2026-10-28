#!/usr/bin/env python3
"""TEST34: 1 PRG + original TEST19 19 SID, preserving their EXACT D64 sectors.
Unlike TEST27..31, don't rebuild SID data layout. Controlled Krill disk test.
Does not prove VICE playback.
"""
from pathlib import Path
import argparse
import hashlib
import json

SPT={t:21 if t<=17 else 19 if t<=24 else 18 if t<=30 else 17 for t in range(1,36)}
SIZE=174848
MASTER_SHA="b247f58ce9d3df87025d0f09ca145998bffe31e8f9e520c5c29dcfc238d66cc5"

def off(t,s):
    assert 1<=t<=35 and 0<=s<SPT[t],(t,s)
    return (sum(SPT[i] for i in range(1,t))+s)*256

def entries(b):
    t,s=18,1;names=set();out=[];directory=[]
    while t:
        assert (t,s) not in directory, "loop in directory"
        directory.append((t,s))
        p=off(t,s)
        nt,ns=b[p:p+2]
        for i in range(8):
            q=p+i*32
            if not b[q+2]&0x80:continue
            name=b[q+5:q+21].rstrip(b'\xa0').decode('latin1')
            assert name not in names,name
            names.add(name)
            chain=[];bytes_out=bytearray();ft,fs=b[q+3:q+5]
            while ft:
                assert (ft,fs) not in chain,(name,ft,fs)
                chain.append((ft,fs))
                p2=off(ft,fs)
                ntt,nss=b[p2:p2+2]
                bytes_out+=b[p2+2:p2+256] if ntt else b[p2+2:p2+nss+1]
                ft,fs=ntt,nss
            out.append({'name':name,'data':bytes(bytes_out),'chain':chain,
                        'dirent':bytes(b[q:q+32])})
        t,s=nt,ns
    return out,directory

def create(master,prg):
    assert len(master)==SIZE
    orig,old_dirs=entries(master)
    assert orig[0]['name']=='BOOT' and orig[0]['chain']==[(1,0)]
    songs=[x for x in orig if x['name'].upper().endswith('.SID')]
    assert len(songs)==19 and [x['name'] for x in orig[1:20]]==[x['name'] for x in songs]
    assert prg[:2]==bytes((1,8)) and len(prg)>2000
    old_sid_sectors=set(x for sid in songs for x in sid['chain'])
    # Re-use only the now-unlisted auxiliary sectors and original BOOT sector.
    available=list(orig[0]['chain'])
    for item in orig[20:]:
        assert not item['name'].upper().endswith('.SID')
        available.extend(item['chain'])
    assert len(available)==len(set(available))
    assert not (set(available) & old_sid_sectors)
    chunks=[prg[i:i+254] for i in range(0,len(prg),254)]
    new_chain=available[:len(chunks)]
    assert len(new_chain)==len(chunks), "not enough spare auxiliary sectors"
    assert new_chain[0]==(1,0)
    out=bytearray(master)
    for i,((t,s),fragment) in enumerate(zip(new_chain,chunks)):
        p=off(t,s)
        out[p:p+256]=bytes(256)
        out[p:p+2]=bytes(new_chain[i+1]) if i+1<len(new_chain) else bytes((0,len(fragment)+1))
        out[p+2:p+2+len(fragment)]=fragment
    # Keep same exact directory chain and sector locations as TEST19.
    for dt,ds in old_dirs:
        p=off(dt,ds)
        for i in range(8):
            a=p+2 if i==0 else p+32*i
            out[a:p+(i+1)*32]=bytes(p+(i+1)*32-a)
    kept=[]
    d0=bytearray(orig[0]['dirent'])
    d0[2]=0x82
    d0[3:5]=bytes(new_chain[0])
    d0[5:21]=b'SIDPLAY64MIX'.ljust(16,b'\xa0')
    d0[30:32]=len(new_chain).to_bytes(2,'little')
    kept.append(bytes(d0))
    kept.extend(song['dirent'] for song in songs)
    for i,ent in enumerate(kept):
        dt,ds=old_dirs[i//8]
        p=off(dt,ds)
        q=p+i%8*32
        out[q+2:q+32]=ent[2:32]
    # Update BAM to represent allocated directory/SID/PRG sectors.
    occupied={(18,0),*old_dirs,*old_sid_sectors,*new_chain}
    p=off(18,0)
    for t in range(1,36):
        vacant=[s for s in range(SPT[t]) if (t,s) not in occupied]
        bitmask=[0,0,0]
        for s in vacant:bitmask[s//8]|=1<<(s%8)
        q=p+4+(t-1)*4
        out[q:q+4]=bytes([len(vacant),*bitmask])
    # Preserve the original disk title, disk ID and DOS type, intentionally.
    checked,directories=entries(out)
    assert len(checked)==20
    assert checked[0]['name']=='SIDPLAY64MIX'
    assert checked[0]['data']==prg
    assert [x['name'] for x in checked[1:]]==[x['name'] for x in songs]
    for a,b in zip(checked[1:],songs):
        assert a['data']==b['data'],a['name']
        assert a['chain']==b['chain'],a['name']
        for t,s in a['chain']:
            p=off(t,s)
            assert master[p:p+256]==out[p:p+256],(a['name'],t,s)
    assert bytes(out[off(18,0)+0x90:off(18,0)+0xA8])==master[off(18,0)+0x90:off(18,0)+0xA8]
    assert directories==old_dirs
    return bytes(out),{
        "test":"TEST34",
        "status":"STATIC PASS ONLY; VICE UNTESTED",
        "experiment":"Original TEST19 SID physical sectors unchanged; changed only program and directory/BAM",
        "prg_bytes":len(prg),"new_prg_blocks":len(new_chain),
        "sid_count":len(songs),"files_total":len(checked),
        "all_19_sid_chains_byte_identical_to_TEST19":True,
        "unchanged_disk_id":True,
        "master_sha256":MASTER_SHA,
        "d64_sha256":hashlib.sha256(out).hexdigest(),
    }

def main():
    ap=argparse.ArgumentParser()
    for arg in ('master','prg','output','report'):
        ap.add_argument('--'+arg,type=Path,required=True)
    a=ap.parse_args()
    master=a.master.read_bytes()
    assert hashlib.sha256(master).hexdigest()==MASTER_SHA
    output,report=create(master,a.prg.read_bytes())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_bytes(output)
    a.report.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
if __name__=="__main__":main()
