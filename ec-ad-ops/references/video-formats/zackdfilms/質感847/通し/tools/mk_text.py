"""台本の本文から、字幕の文（disp）と声に渡す文（vo）を作る → 声/sentences.json・声/vo_text.txt"""
import json,re,os
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L=open(W+"/ref/台本.md").read().split("\n")
i=L.index("## 本文")+1; body=[]
for l in L[i:]:
    if l.strip()=="---": break
    body.append(l)
paras=[[s for s in re.split(r"(?<=。)",p) if s.strip()] for p in "\n".join(body).strip().split("\n\n")]
REP=[("朝7時","朝しちじ"),("夕方6時","夕方ろくじ"),("10時","じゅうじ"),("3時","さんじ"),("11時間","じゅういちじかん"),
     ("30秒","さんじゅうびょう"),("5分","ごふん"),("10分","じゅっぷん"),("1本1本","いっぽんいっぽん"),("1本","いっぽん"),
     ("1つ","ひとつ"),("床","ゆか"),("敷いて","しいて")]
def vo(s):
    for a,b in REP: s=s.replace(a,b)
    return s
out=[];n=0
for pi,p in enumerate(paras):
    for s in p:
        n+=1; s=s.strip(); out.append({"n":n,"para":pi,"disp":s,"vo":vo(s)})
json.dump(out,open(W+"/声/sentences.json","w"),ensure_ascii=False,indent=1)
txt="\n\n".join("".join(o["vo"] for o in out if o["para"]==pi) for pi in range(len(paras)))
open(W+"/声/vo_text.txt","w").write(txt)
print(n,"文",len(paras),"段", sum(len(re.sub(r"[、。\s]","",o["disp"])) for o in out),"字")
