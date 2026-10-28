#!/usr/bin/env python3
"""TEST36: non-invasive PSID/RSID compatibility audit. No master changes."""
import argparse
from pathlib import Path
import hashlib
import json
import zipfile

SPT = {t:(21 if t<=17 else 19 if t<=24 else 18 if t<=30 else 17) for t in range(1,36)}

def u16(b,i):
    return int.from_bytes(b[i:i+2], "big")

def audit(b,name):
    info={"file":name,"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
    if len(b)<118 or b[:4] not in (b"PSID",b"RSID"):
        return {**info,"status":"INVALID","reasons":["Invalid/missing SID header"]}
    kind=b[:4].decode("ascii")
    v,off,hl,ini,play,n,first=[u16(b,i) for i in (4,6,8,10,12,14,16)]
    speed=int.from_bytes(b[18:22],"big")
    flags=u16(b,118) if v>=2 and len(b)>=124 else 0
    sid2=b[122] if v>=3 and len(b)>=124 else 0
    sid3=b[123] if v>=4 and len(b)>=124 else 0
    info.update(format=kind,version=v,offset=off,header_load=hex(hl),
                init=hex(ini),play=hex(play),songs=n,start_song=first,
                speed=hex(speed),flags=hex(flags),sid2=sid2,sid3=sid3)
    errors=[]
    if v not in (1,2,3,4):errors.append("Version not supported in TEST36")
    if kind=="RSID" and v==1:errors.append("RSID v1 invalid")
    if off < (118 if v==1 else 124) or off>len(b):errors.append("Bad data offset")
    if n<1 or n>256 or first<1 or first>n:errors.append("Bad subtune numbers")
    if kind=="RSID" and (hl or play or speed):errors.append("RSID reserved fields not zero")
    if errors:return {**info,"status":"INVALID","reasons":errors}
    if hl==0 and len(b)-off<2:
        return {**info,"status":"INVALID","reasons":["Missing load-address word"]}
    load=hl or int.from_bytes(b[off:off+2],"little")
    body=len(b)-off-(2 if hl==0 else 0)
    end=load+body
    ini=ini or load
    info.update(load=hex(load),effective_init=hex(ini),end_exclusive=hex(end),
                body_bytes=body,embedded_load_address=(hl==0))
    if body<=0 or end>65536:
        return {**info,"status":"INVALID","reasons":["Empty music or out of address space"]}
    reasons=[]
    if kind=="RSID":reasons.append("RSID needs its own C64 hardware/IRQ execution environment")
    if flags&1:reasons.append("MUS needs external player")
    if flags&2 and kind=="PSID":reasons.append("PlaySID-specific behavior")
    if sid2 or sid3:reasons.append("Multiple SID chips")
    if play==0:reasons.append("PLAY=0 self-managed interrupt")
    if load<0x1000 or end>0x3000:reasons.append("Overlaps TEST35 protected player RAM")
    if body>0x1a00:reasons.append("Exceeds 26-page prefetch bank")
    if not load<=ini<end:reasons.append("INIT not in tune payload")
    if play and not load<=play<end:reasons.append("PLAY not in tune payload")
    if reasons:
        info["status"]="NEEDS_NEW_ENGINE"
    elif (v==2 and off==0x7c and hl==0 and load==0x1000 and
          ini==0x1000 and play==0x1003 and n==first==1):
        info["status"]="TEST35_LAYOUT_CANDIDATE"
        reasons=["Matches the tested layout; playback still needs VICE validation"]
    else:
        info["status"]="TEST37_DYNAMIC_ADDRESS_CANDIDATE"
        reasons=["Requires dynamic LOAD/INIT/PLAY or header-aware bank loading"]
    info["reasons"]=reasons
    return info

def offset(t,s):
    if t not in SPT or not 0<=s<SPT[t]:raise ValueError("Invalid track/sector")
    return (sum(SPT[x] for x in range(1,t))+s)*256

def d64files(d,name):
    if len(d)<174848:raise ValueError("D64 image truncated")
    t,s=18,1;seen=set()
    while t:
        if (t,s) in seen:raise ValueError("Cyclic directory")
        seen.add((t,s))
        p=offset(t,s);nt,ns=d[p:p+2]
        for j in range(8):
            q=p+j*32
            if not d[q+2]&0x80:continue
            filename=d[q+5:q+21].rstrip(b"\xa0").decode("latin1")
            if not filename.upper().endswith(".SID"):continue
            ft,fs=d[q+3:q+5];file=bytearray();chain=set()
            while ft:
                if (ft,fs) in chain:raise ValueError("Cyclic SID sector chain")
                chain.add((ft,fs));a=offset(ft,fs);nn,ss=d[a:a+2]
                file+=d[a+2:a+256] if nn else d[a+2:a+ss+1]
                ft,fs=nn,ss
            yield name+":"+filename,bytes(file)
        t,s=nt,ns

def files(paths):
    for p in paths:
        if p.is_dir():
            yield from files(sorted(x for x in p.rglob("*") if x.suffix.lower()==".sid"))
        elif p.suffix.lower()==".sid":
            yield str(p),p.read_bytes()
        elif p.suffix.lower()==".d64":
            yield from d64files(p.read_bytes(),str(p))
        elif p.suffix.lower()==".zip":
            with zipfile.ZipFile(p) as z:
                for f in z.infolist():
                    if f.filename.lower().endswith(".sid") and not f.is_dir() and f.file_size<=262144:
                        yield str(p)+":"+f.filename,z.read(f)
        else:
            raise ValueError("Unsupported input: "+str(p))

def main():
    a=argparse.ArgumentParser(description="TEST36 PSID/RSID compatibility audit")
    a.add_argument("inputs",type=Path,nargs="+")
    a.add_argument("--json",type=Path)
    args=a.parse_args()
    rows=[audit(data,name) for name,data in files(args.inputs)]
    statuses=["TEST35_LAYOUT_CANDIDATE","TEST37_DYNAMIC_ADDRESS_CANDIDATE","NEEDS_NEW_ENGINE","INVALID"]
    summary={x:sum(r["status"]==x for r in rows) for x in statuses}
    report={"test":"TEST36","static_only":True,"count":len(rows),
            "categories":summary,"files":rows}
    out=json.dumps(report,indent=2,ensure_ascii=False)
    if args.json:args.json.write_text(out+"\n",encoding="utf-8")
    print(out)

if __name__=="__main__":
    main()
