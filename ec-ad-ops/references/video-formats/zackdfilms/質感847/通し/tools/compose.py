"""組む：無音の映像（render2.py の出力）に、指す輪（fx.json）・札（badges.json）・字幕を重ね、声・効果音・BGM を混ぜて 24コマで書き出す。
usage: compose.py silent.mp4 out.mp4
- 輪：fx.json の行 [t0,t1,x0,y0,r0,x1,y1,r1,"色","指す物"]（16章。pointer_check.py の --gate を通してから）
- 札：badges.json の行 {"t0","t1","text","x","y","size"}（時計の札・数字の札。絵には文字を描かせず、編集で重ねる）
- 字幕：声/timing.json の句。白の太字・黒のふち・高さ78%
- 音：声 −14 LUFS／効果音（work/timeline.json の sfx_join ＋ work/sfx_extra.json）／BGM W-MOOD-27 を声の20dB下
"""
import json, os, re, subprocess, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import _zg_video as _zg
W0 = _zg.W; os.chdir(W0)   # アプリ：作業フォルダ（ZG_WORK）
SIL, OUT = sys.argv[1], sys.argv[2]
Wd, Ht, FPS = 1080, 1920, 24
TL = json.load(open("work/timeline.json")); END = TL["end"]
FX = json.load(open("fx.json")) if os.path.exists("fx.json") else []
BD = json.load(open("badges.json")) if os.path.exists("badges.json") else []
CH = json.load(open("声/timing.json"))["chunks"]
FONT = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc", 66)
BF = lambda s: ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W8.ttc", s)
COL = dict(red=(235, 40, 40), yellow=(255, 214, 40), gray=(200, 205, 210), green=(60, 220, 110), white=(255, 255, 255))
# 字幕の時刻：句の始め〜次の句の始め（最後は +0.35）。文の間は消さずにつなぐ（ちらつき防止）
subs = []
for i, c in enumerate(CH):
    b = CH[i + 1]["t0"] if i + 1 < len(CH) else min(END, c["t1"] + 0.35)
    if b - c["t1"] > 0.6: b = c["t1"] + 0.3
    subs.append((c["text"], c["t0"], b))
SUBIMG = {}


def sub_img(text):
    if text in SUBIMG: return SUBIMG[text]
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    w = d.textlength(text, font=FONT); im = Image.new("RGBA", (int(w) + 40, 110), (0, 0, 0, 0)); g = ImageDraw.Draw(im)
    g.text((23, 12), text, font=FONT, fill=(0, 0, 0, 120), stroke_width=9, stroke_fill=(0, 0, 0, 120))
    g.text((20, 8), text, font=FONT, fill=(255, 255, 255, 255), stroke_width=7, stroke_fill=(0, 0, 0, 255))
    SUBIMG[text] = im; return im


def badge_img(text, size, plain=False, gray=False):
    f = BF(size)
    if plain:
        d = ImageDraw.Draw(Image.new("RGBA", (10, 10))); w = d.textlength(text, font=f); im = Image.new("RGBA", (int(w) + 80, int(size * 1.6)), (0, 0, 0, 0)); g = ImageDraw.Draw(im)
        from PIL import ImageFilter
        g.text((40, 10), text, font=f, fill=(255, 255, 255, 200)); im = im.filter(ImageFilter.GaussianBlur(12)); g = ImageDraw.Draw(im)
        g.text((40, 10), text, font=f, fill=(255, 255, 255, 255)); return im
    d = ImageDraw.Draw(Image.new("RGBA", (10, 10))); w = d.textlength(text, font=f)
    pw, ph = int(w + size * 0.9), int(size * 1.45)
    im = Image.new("RGBA", (pw + 12, ph + 12), (0, 0, 0, 0)); g = ImageDraw.Draw(im)
    g.rounded_rectangle((8, 10, pw + 8, ph + 10), radius=ph // 3, fill=(0, 0, 0, 90))
    g.rounded_rectangle((4, 4, pw + 4, ph + 4), radius=ph // 3, fill=(225, 228, 232, 235) if gray else (255, 255, 255, 245), outline=(120, 128, 138, 255) if gray else (20, 40, 70, 255), width=max(3, size // 14))
    g.text((4 + (pw - w) / 2, 4 + size * 0.18), text, font=f, fill=(120, 128, 138, 255) if gray else (20, 40, 70, 255))
    return im


def ease_out(u): return 1 - (1 - u) ** 3


def draw_frame(arr, t):
    im = Image.fromarray(arr).convert("RGBA"); ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(ov)
    for r in FX:
        t0, t1, x0, y0, r0, x1, y1, r1 = r[:8]; col = COL.get(r[9] if len(r) > 9 else "red", (235, 40, 40))
        if not (t0 <= t < t1): continue
        u = (t - t0) / max(t1 - t0, 1e-3); x = x0 + (x1 - x0) * u; y = y0 + (y1 - y0) * u; rr = r0 + (r1 - r0) * u
        grow = ease_out(min(1, (t - t0) / 0.25)); fade = min(1, (t1 - t) / 0.2)
        R = rr * Wd * (0.55 + 0.45 * grow); cx, cy = x * Wd, y * Ht; a = int(255 * fade)
        for k, (wd, al) in enumerate([(int(R * 0.22), 60), (int(R * 0.12), 140), (max(6, int(R * 0.07)), 255)]):
            g.ellipse((cx - R, cy - R, cx + R, cy + R), outline=col + (int(al * fade),), width=wd)
        # 外へ広がる薄い輪（ZackD の広がる輪）
        pr = R * (1 + 0.6 * ((t - t0) % 0.8) / 0.8); g.ellipse((cx - pr, cy - pr, cx + pr, cy + pr), outline=col + (int(90 * fade * (1 - ((t - t0) % 0.8) / 0.8)),), width=5)
    for b in BD:
        if not (b["t0"] <= t < b["t1"]): continue
        bi = badge_img(b["text"], b.get("size", 64), b.get("plain"), b.get("gray")); u = (t - b["t0"]) / 0.18
        sc = 0.6 + 0.5 * ease_out(min(1, u)) - 0.1 * max(0, min(1, u - 1)); fade = min(1, (b["t1"] - t) / 0.15)
        if b.get("pop_out") and b["t1"] - t < 0.2: sc *= 1 + (0.2 - (b["t1"] - t)) * 3
        bi = bi.resize((max(1, int(bi.width * sc)), max(1, int(bi.height * sc))))
        if fade < 1: bi.putalpha(bi.getchannel("A").point(lambda v: int(v * fade)))
        ov.alpha_composite(bi, (int(b["x"] * Wd - bi.width / 2), int(b["y"] * Ht - bi.height / 2)))
    for s, a, b in subs:
        if a <= t < b:
            si = sub_img(s); ov.alpha_composite(si, (int((Wd - si.width) / 2), int(Ht * 0.78 - si.height / 2)))
    im.alpha_composite(ov); return np.asarray(im.convert("RGB"))


def video():
    rd = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SIL, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Wd}x{Ht}", "-r", str(FPS), "-i", "-",
                            "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "work/video_sub.mp4"], stdin=subprocess.PIPE)
    j = 0
    while True:
        raw = rd.stdout.read(Wd * Ht * 3)
        if len(raw) < Wd * Ht * 3: break
        t = (j + 0.5) / FPS; enc.stdin.write(draw_frame(np.frombuffer(raw, np.uint8).reshape(Ht, Wd, 3), t).tobytes()); j += 1
    enc.stdin.close(); enc.wait(); print("frames", j)


def lufs(p):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", o)[-1])


def htp(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-ac', '1', '-ar', '48000', '-f', 'f32le', '-'], capture_output=True).stdout
    x = np.abs(np.frombuffer(r, np.float32)); return float(np.argmax(x)) / 48000


def audio():
    _zg.compose_audio(TL, END, CH, lufs, htp)   # アプリ：曲・効果音は 音/ に置いた時だけ（_zg_video.py）


if __name__ == "__main__":
    if "--audio-only" not in sys.argv: video()
    audio()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", "work/video_sub.mp4", "-i", "work/mix.wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], check=True)
    print("ok", OUT)
