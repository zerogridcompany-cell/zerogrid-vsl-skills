"""ElevenLabs forced alignment（声に渡した文で当てる）→ 声/fa.json。鍵の値は出さない"""
import os,sys,json,urllib.request,uuid
O=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
key=os.environ.get("ELEVENLABS_API_KEY")
if not key:
    _f=os.path.expanduser("~/.config/secrets/elevenlabs.env")
    if os.path.exists(_f):
        for l in open(_f):
            if "ELEVENLABS_API_KEY" in l: key=l.split("=",1)[1].strip().strip("\"'").replace("export ","")
if not key: sys.exit("ELEVENLABS_API_KEY がありません（はじめに_つなぐ物.md の 1）")
text=open(O+"/声/vo_text.txt").read().strip()
b="----"+uuid.uuid4().hex
body=(f'--{b}\r\nContent-Disposition: form-data; name="text"\r\n\r\n{text}\r\n--{b}\r\nContent-Disposition: form-data; name="file"; filename="vo.wav"\r\nContent-Type: audio/wav\r\n\r\n').encode()+open(O+"/声/vo_raw.wav","rb").read()+f"\r\n--{b}--\r\n".encode()
req=urllib.request.Request("https://api.elevenlabs.io/v1/forced-alignment",data=body,headers={"xi-api-key":key,"Content-Type":f"multipart/form-data; boundary={b}"})
d=json.loads(urllib.request.urlopen(req,timeout=300).read())
json.dump(d,open(O+"/声/fa.json","w"),ensure_ascii=False)
print(len(d["characters"]),d["characters"][-1])
