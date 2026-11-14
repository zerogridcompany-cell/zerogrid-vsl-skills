"""絵を並べて1枚にする。sheet.py out.jpg 幅 絵...  (名前を下に書く)"""
import sys,os
from PIL import Image,ImageDraw,ImageFont
out=sys.argv[1]; w=int(sys.argv[2]); fs=sys.argv[3:]
F=ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",max(12,w//18))
ims=[]
for f in fs:
    im=Image.open(f).convert("RGB"); h=int(im.height*w/im.width); im=im.resize((w,h)); c=Image.new("RGB",(w,h+w//10),"white"); c.paste(im,(0,0))
    ImageDraw.Draw(c).text((4,h+2),os.path.basename(f)[:30],fill="black",font=F); ims.append(c)
cols=min(len(ims),int(sys.argv[0] and os.environ.get("COLS","4")))
rows=(len(ims)+cols-1)//cols; H=max(i.height for i in ims)
S=Image.new("RGB",(w*cols,H*rows),"white")
for i,im in enumerate(ims): S.paste(im,((i%cols)*w,(i//cols)*H))
S.save(out,quality=85)
