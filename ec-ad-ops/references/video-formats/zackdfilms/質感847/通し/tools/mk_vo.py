"""全文を1回で録る（テイク番号を引数で）。鍵は ELEVENLABS_API_KEY（無ければ ~/.config/secrets/elevenlabs.env）。値は出さない→ 声/take{i}.mp3"""
import os,sys,json,urllib.request
from concurrent.futures import ThreadPoolExecutor
O=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
key=os.environ.get("ELEVENLABS_API_KEY")
if not key:
    _f=os.path.expanduser("~/.config/secrets/elevenlabs.env")
    if os.path.exists(_f):
        for l in open(_f):
            if "ELEVENLABS_API_KEY" in l: key=l.split("=",1)[1].strip().strip("\"'").replace("export ","")
if not key: sys.exit("ELEVENLABS_API_KEY がありません（はじめに_つなぐ物.md の 1）")
text=open(O+"/声/vo_text.txt").read().strip()
VOICE=os.environ.get("ELEVENLABS_VOICE_ID","W8wofKLOWnsM57L8hIx2")  # Koji（男性ナレーター・音声.md の10番）
def go(i):
    out=f"{O}/声/take{i}.mp3"
    if os.path.exists(out) and os.path.getsize(out)>1000: return out+" あり"
    req=urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_192",
        data=json.dumps({"text":text,"model_id":"eleven_v4","language_code":"ja"}).encode(),headers={"xi-api-key":key,"Content-Type":"application/json"})
    try:
        b=urllib.request.urlopen(req,timeout=420).read(); open(out,"wb").write(b); return f"{out} ok {len(b)}"
    except urllib.error.HTTPError as e: return f"{out} ERR {e.code} {e.read()[:300]}"
    except Exception as e: return f"{out} ERR {e}"
with ThreadPoolExecutor(3) as ex:
    for o in ex.map(go,[int(x) for x in sys.argv[1:]] or [1]): print(o,flush=True)
