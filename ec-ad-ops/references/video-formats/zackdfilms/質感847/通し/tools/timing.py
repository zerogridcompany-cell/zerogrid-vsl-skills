"""fa.json → 声/timing.json（文ごとの時刻・字幕の句ごとの時刻）"""
import json,os,re,sys
import _zg_video as _zg; O=_zg.W   # アプリ：作業フォルダ（ZG_WORK）
S=json.load(open(O+"/声/sentences.json")); fa=json.load(open(O+"/声/fa.json"))["characters"]
REP=_zg.readings("REP")   # アプリ：字幕の字と声の読みの差は 声/読み.json（無ければ無し）
SUB=_zg.readings("SUB")
def vo(s):
    for a,b in REP: s=s.replace(a,b)
    return s
P=lambda t: re.sub(r"[\s、。]","",t)
chars=[c for c in fa if P(c["text"])]; stream="".join(c["text"] for c in chars)
pos=0
def find(v):
    global pos
    v=P(v); i=stream.index(v,pos); pos=i+len(v); return chars[i]["start"],chars[i+len(v)-1]["end"]
MAX=14
def split_phrase(p):
    if len(P(p))<=MAX: return [p]
    # 真ん中に近い助詞の後で割る
    best=None
    for m in re.finditer(r"(は|が|を|に|で|て|と|の|へ|も|ら|ば)",p):
        k=m.end()
        if k<len(p) and p[k] in "っゃゅょぁぃぅぇぉたてだでるれらりんいうえおけげくぐ": continue
        if 4<=k<=len(p)-3:
            sc=abs(k-len(p)/2)
            if best is None or sc<best[0]: best=(sc,k)
    if not best: return [p]
    return split_phrase(p[:best[1]])+split_phrase(p[best[1]:])
out={"sentences":[],"chunks":[]}
for s in S:
    parts=[x for x in re.split(r"(?<=、)",s["disp"]) if P(x)]
    # 短すぎる句は次とくっつける
    merged=[]
    for x in parts:
        if merged and len(P(merged[-1]))+len(P(x))<=MAX and len(P(merged[-1]))<=6: merged[-1]+=x
        else: merged.append(x)
    t0=None
    for x in merged:
        for y in split_phrase(x):
            a,b=find(vo(y)); t0=a if t0 is None else t0
            d=y.rstrip("、。")
            for u,w in SUB: d=d.replace(u,w)
            out["chunks"].append({"n":s["n"],"text":d,"t0":round(a,3),"t1":round(b,3)})
    out["sentences"].append({"n":s["n"],"disp":s["disp"],"t0":round(t0,3),"t1":round(b,3)})
json.dump(out,open(O+"/声/timing.json","w"),ensure_ascii=False,indent=1)
for s in out["sentences"]: print(s["n"],s["t0"],s["t1"],round(s["t1"]-s["t0"],2),s["disp"][:20])
print(len(out["chunks"]),"句 最長",max(len(c["text"]) for c in out["chunks"]))
