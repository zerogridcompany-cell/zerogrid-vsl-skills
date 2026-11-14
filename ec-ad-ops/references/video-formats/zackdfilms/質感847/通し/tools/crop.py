"""絵を切り出して元の大きさに戻す（カメラが寄った終わりの絵の下絵）。crop.py <入> <出> <倍率> <中心x 0-1> <中心y 0-1>"""
import sys
from PIL import Image
i, o, s, cx, cy = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
im = Image.open(i).convert("RGB"); W, H = im.size; w, h = W / s, H / s
x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h)
im.crop((round(x0), round(y0), round(x0 + w), round(y0 + h))).resize((W, H), Image.LANCZOS).save(o)
print(o, round(x0), round(y0), round(w), round(h))
