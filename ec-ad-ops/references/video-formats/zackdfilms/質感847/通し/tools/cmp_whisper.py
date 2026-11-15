"""whisper の書き起こしを台本（字幕の字）と照らす。差の所だけ出す。cmp_whisper.py <w.json>"""
import json,sys,re,difflib,os
W=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S=json.load(open(W+"/声/sentences.json"))
norm=lambda t: re.sub(r"[\s、。,.!?！？「」『』…]","",t)
ref="".join(norm(s["disp"]) for s in S)
hyp="".join(norm(x["text"]) for x in json.load(open(sys.argv[1]))["transcription"])
sm=difflib.SequenceMatcher(None,ref,hyp,autojunk=False)
print("一致率",round(sm.ratio(),3),len(ref),len(hyp))
for op,a,b,c,d in sm.get_opcodes():
    if op!="equal": print(op, ref[max(0,a-6):a]+"["+ref[a:b]+"]"+ref[b:b+4], "→", "["+hyp[c:d]+"]")
