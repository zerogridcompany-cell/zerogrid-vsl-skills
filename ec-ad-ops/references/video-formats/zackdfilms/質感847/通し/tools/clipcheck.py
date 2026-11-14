"""複数のクリップの 1秒6コマを、1枚にまとめる（1行＝1クリップ。小さめ）。clipcheck.py out.jpg 場面..."""
import sys,subprocess,os
from PIL import Image
import _zg_video as _zg; W=_zg.W   # アプリ：作業フォルダ（ZG_WORK）
rows=[]
for s in sys.argv[2:]:
    p=_zg.clip_path(s)
    if not os.path.exists(p): continue
    out=os.path.join(__import__("tempfile").gettempdir(),f"cc_{s}.jpg")   # アプリ：/tmp には書けない（囲いの中）
    subprocess.run(["ffmpeg","-v","error","-y","-i",p,"-vf","fps=6,scale=110:165,tile=30x1:padding=1","-frames:v","1",out])
    rows.append(Image.open(out))
w=max(r.width for r in rows); S=Image.new("RGB",(w,sum(r.height+4 for r in rows)),"white"); y=0
for r in rows: S.paste(r,(0,y)); y+=r.height+4
S.save(sys.argv[1],quality=78); print(len(rows))
