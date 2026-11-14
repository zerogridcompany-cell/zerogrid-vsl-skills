"""クリップを並べて、速さの山・編集のカメラ・ブレを作る（作り方の直し 1-1・1-2。針マット_01 の render.py を元に直した）
usage: python render2.py plan.json out_silent.mp4   （針マット_14：クリップの場所は plan の src。中間コマ(minterpolate)は interp の時だけ。それ以外は同じコマの複製）
plan.json:
  "clips": [{"name","t0","t1","keys":[[出す時刻, クリップの時刻],...]}]   クリップは クリップ/<版>/<name>.mp4
  "cam":   [[時刻, 倍率, 中心x, 中心y, "lin"|"io"|"out"], ...]   編集のカメラ（全体で1本の線。切り替えの所は同じ時刻を2つ置く）
- クリップは先に 72コマ/秒へ中間コマを作る（minterpolate mci）。
- 出す1コマごとに、シャッターの間（shutter/24 秒）を細かく区切り、その時刻ごとの「クリップのコマ × 編集のカメラ」を全部混ぜる。
  → クリップを速く進めた所も、編集のカメラが速く動いた所も、動きの向きにそってブレる。止まっている所はくっきり。
"""
import json, os, subprocess, sys
import numpy as np, cv2

plan = json.load(open(sys.argv[1])); OUT = sys.argv[2]
ROOT = __import__("_zg_video").W   # アプリ：作業フォルダ（ZG_WORK）
FPS = plan.get("fps", 24); W, H = plan.get("W", 1080), plan.get("H", 1920); UP = 72
SHUT = plan.get("shutter", 0.5)


def pchip(xs, ys):
    xs = np.asarray(xs, float); ys = np.asarray(ys, float); h = np.diff(xs); d = np.diff(ys) / h
    m = np.zeros(len(xs))
    for k in range(1, len(xs) - 1):
        if d[k - 1] * d[k] > 0:
            w1, w2 = 2 * h[k] + h[k - 1], h[k] + 2 * h[k - 1]
            m[k] = (w1 + w2) / (w1 / d[k - 1] + w2 / d[k])
    m[0], m[-1] = d[0], d[-1]

    def f(x):
        x = np.clip(x, xs[0], xs[-1]); k = int(np.clip(np.searchsorted(xs, x) - 1, 0, len(h) - 1))
        t = (x - xs[k]) / h[k]; t2, t3 = t * t, t * t * t
        return float((2 * t3 - 3 * t2 + 1) * ys[k] + (t3 - 2 * t2 + t) * h[k] * m[k] + (-2 * t3 + 3 * t2) * ys[k + 1] + (t3 - t2) * h[k] * m[k + 1])
    return f


def upsampled(c):
    src = c["src"]; name = c["name"]; os.makedirs(f"{ROOT}/work/up", exist_ok=True); dst = f"{ROOT}/work/up/{name}_up{UP}.mp4"
    mi = f"minterpolate=fps={UP}:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" if c.get("interp") else f"fps={UP}"
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-vf",
                        f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},{mi}",
                        "-c:v", "libx264", "-crf", "10", "-preset", "fast", "-pix_fmt", "yuv420p", dst], check=True)
    return dst


class Reader:
    def __init__(self, path):
        self.p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
        self.buf = {}; self.next = 0; self.last = None

    def get(self, i):
        i = max(0, i)
        while self.next <= i:
            raw = self.p.stdout.read(W * H * 3)
            if len(raw) < W * H * 3:
                break
            self.last = np.frombuffer(raw, np.uint8).reshape(H, W, 3); self.buf[self.next] = self.last; self.next += 1
        for k in [k for k in self.buf if k < i - 40]:
            del self.buf[k]
        return self.buf.get(i, self.buf[min(self.buf, key=lambda k: abs(k - i))] if self.buf else self.last)


CAM = plan["cam"]


def ease(u, kind):
    if kind == "io":
        return u * u * (3 - 2 * u)
    if kind == "in":
        return u ** 3
    if kind == "out":
        return 1 - (1 - u) ** 3
    return u


def cam_at(t):
    if t <= CAM[0][0]:
        return CAM[0][1:4]
    for a, b in zip(CAM, CAM[1:]):
        if a[0] <= t < b[0]:
            u = ease((t - a[0]) / max(b[0] - a[0], 1e-6), b[4] if len(b) > 4 else "lin")
            return [a[k] + (b[k] - a[k]) * u for k in (1, 2, 3)]
    return CAM[-1][1:4]


def apply_cam(img, sc, cx, cy):
    w, h = W / sc, H / sc; x0 = min(max(cx * W - w / 2, 0), W - w); y0 = min(max(cy * H - h / 2, 0), H - h)
    M = np.float32([[sc, 0, -x0 * sc], [0, sc, -y0 * sc]])
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


import _zg_render; _zg_render.split(plan, OUT, FPS, upsampled)   # 子の回（ZG_SEG）では何もしない
enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                        "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p", OUT], stdin=subprocess.PIPE)
log = []
END = plan["clips"][-1]["t1"]; nfr = int(round(END * FPS))
readers = {}; taus = {}
for c in plan["clips"]:
    taus[c["name"]] = pchip([k[0] for k in c["keys"]], [k[1] for k in c["keys"]])
for j in range(*_zg_render.frames(nfr)):
    t = (j + 0.5) / FPS
    c = next(c for c in plan["clips"] if c["t0"] <= t < c["t1"] or c is plan["clips"][-1])
    if c["name"] not in readers:
        for n in list(readers):
            readers[n].p.kill(); del readers[n]
        readers[c["name"]] = Reader(upsampled(c))
    rd = readers[c["name"]]; tau = taus[c["name"]]
    a, b = max(c["t0"], t - SHUT / FPS / 2), min(c["t1"] - 1e-4, t + SHUT / FPS / 2)
    span_in = abs(tau(b) - tau(a)) * UP
    ca, cb = cam_at(a), cam_at(b)
    span_cam = (abs(cb[0] - ca[0]) * W * 0.6 + abs(cb[1] - ca[1]) * W * cb[0] + abs(cb[2] - ca[2]) * H * cb[0]) / 5.0
    n = int(min(28, max(1, round(span_in) + 1, int(np.ceil(span_cam)))))
    acc = np.zeros((H, W, 3), np.float32)
    for ts in (np.linspace(a, b, n) if n > 1 else [t]):
        fr = rd.get(int(round(tau(ts) * UP)))
        sc, cx, cy = cam_at(ts)
        acc += apply_cam(fr, sc, cx, cy)
    img = acc / n
    for dc in plan["clips"]:
        if dc.get("dip") and abs(t - dc["t0"]) < 0.3:
            img = img * (0.25 + 0.75 * abs(t - dc["t0"]) / 0.3)
    enc.stdin.write(np.clip(img, 0, 255).astype(np.uint8).tobytes())
    sc, cx, cy = cam_at(t)
    log.append({"t": round(t, 3), "clip": c["name"], "in": round(tau(t), 3), "mix": n, "cam": [round(sc, 3), round(cx, 3), round(cy, 3)]})
for r in readers.values():
    r.p.kill()
enc.stdin.close(); enc.wait()
json.dump(log, open(OUT.replace(".mp4", "_map.json"), "w"))
print("frames", len(log), OUT)
