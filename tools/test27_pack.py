#!/usr/bin/env python3
"""TEST27 single C64 PRG plus 19 original SID. STATIC verification only."""
from pathlib import Path
import argparse,math,hashlib,json
S={t:(21 if t<=17 else 19 if t<=24 else 18 if t<=30 else 17) for t in range(1,36)}
def off(t,s):
 assert t in S and 0<=s<S[t]
 return 256*(sum(S[x] for x in range(1,t))+s)
def files(b):
 assert len(b)==174848
 t,s=18,1;result=[];d=set()
 while t:
  assert (t,s) not in d;d.add((t,s));p=off(t,s)
  for i in range(8):
   q=p+i*32
   if not b[q+2]&0x80:continue
   name=b[q+5:q+21].rstrip(b'\xa0').decode('latin1')
   a,c=b[q+3:q+5];body=bytearray();seen=set()
   while a:
    assert (a,c) not in seen;seen.add((a,c));v=off(a,c)
    nxt,sec=b[v:v+2]
    body+=b[v+2:v+256] if nxt else b[v+2:v+sec+1]
    a,c=nxt,sec
   result.append((name,bytes(body)))
  t,s=b[p:p+2]
 return result
def make(data):
 b=bytearray(174848);used={(18,0)};dn=math.ceil(len(data)/8)
 used|={(18,s) for s in range(1,dn+1)}
 for s in range(1,dn+1):b[off(18,s):off(18,s)+2]=bytes((18,s+1)) if s<dn else b'\x00\xff'
 pool=[(t,s) for t in list(range(17,0,-1))+list(range(19,36)) for s in range(S[t])]
 cursor=0
 for k,(name,blob) in enumerate(data):
  assert len(name.encode('latin1'))<=16 and blob
  part=[blob[j:j+254] for j in range(0,len(blob),254)]
  chain=pool[cursor:cursor+len(part)];assert len(chain)==len(part)
  cursor+=len(part)
  for n,((t,s),frag) in enumerate(zip(chain,part)):
   assert (t,s) not in used;used.add((t,s));p=off(t,s)
   b[p:p+2]=bytes(chain[n+1]) if n+1<len(chain) else bytes((0,len(frag)+1))
   b[p+2:p+2+len(frag)]=frag
  q=off(18,k//8+1)+(k%8)*32
  b[q+2]=0x82;b[q+3:q+5]=bytes(chain[0]);b[q+5:q+21]=name.encode('latin1').ljust(16,b'\xa0')
  b[q+30:q+32]=len(chain).to_bytes(2,'little')
 p=off(18,0);b[p:p+4]=bytes((18,1,0x41,0))
 for t in range(1,36):
  z=[s for s in range(S[t]) if (t,s) not in used];q=p+4+(t-1)*4;b[q]=len(z)
  for s in z:b[q+1+s//8]|=1<<(s%8)
 b[p+0x90:p+0xa0]=b'SIDPLAY MIX27'.ljust(16,b'\xa0')
 b[p+0xa2:p+0xa4]=b'27';b[p+0xa5:p+0xa7]=b'2A'
 return bytes(b)
def main():
 ap=argparse.ArgumentParser()
 for k in ['master','prg','output','report']:ap.add_argument('--'+k,required=True,type=Path)
 a=ap.parse_args();master=a.master.read_bytes()
 assert hashlib.sha256(master).hexdigest()=='b247f58ce9d3df87025d0f09ca145998bffe31e8f9e520c5c29dcfc238d66cc5'
 songs=[x for x in files(master) if x[0].upper().endswith('.SID')];assert len(songs)==19
 prg=a.prg.read_bytes();assert prg[:2]==b'\x01\x08' and len(prg)>2000
 entries=[('SIDPLAY64MIX',prg)]+songs
 d=make(entries);assert files(d)==entries
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(d)
 info={'version':'TEST27','status':'STATIC PASS ONLY; needs VICE','files':len(entries),'sids':19,
       'program_bytes':len(prg),'d64_sha256':hashlib.sha256(d).hexdigest(),
       'music_unchanged':True,'supported_now':'current curated PSID v2 $1000 titles'}
 a.report.write_text(json.dumps(info,indent=2),encoding='utf-8')
 print(json.dumps(info,indent=2))
if __name__=='__main__':main()
