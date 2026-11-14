"""編集の表を作る：場面の時刻（声の文の時刻から）・クリップの時刻の当て方（速さの山）・編集のカメラ（振り・中へ入る）・効果音の時刻。
→ work/plan.json（render2.py が読む）・work/timeline.json（絵コンテ・字幕・効果音・重ねる物が読む）
"""
import json, os, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _zg_video as _zg   # アプリ：作業フォルダ（ZG_WORK）の 指示/shots.json が場面の表
W = _zg.W; SHOTS = _zg.shots(); BYID = {s["id"]: s for s in SHOTS}
TM = json.load(open(W + "/声/timing.json"))
SEN = {s["n"]: s for s in TM["sentences"]}; CH = TM["chunks"]
VOICE_END = TM["sentences"][-1]["t1"]; END = round(VOICE_END + 0.55, 3)

# 前の場面とのつなぎ：cut＝切る（場所・時間が変わる）/ whip＝同じ向きに速く振る / whipv＝縦に振る / push＝中へ速く入る / pull＝中から速く引く / dissolve＝時間が飛ぶ
JOIN = dict(s02="whipv", s03a="whip", s03b="push", s04="whipv", s05a="whip", s05b="push", s06="whip", s07="push", s08="cut", s09="whip", s10="pull", s11="push",
            s12a="cut", s12b="whip", s12c="whip", s13="push", s14="cut", s15="cut", s16="whipv", s17="whipv", s18="cut", s19="cut", s20="whip", s21="cut", s22="whipv",
            s23="push", s24="cut", s25="cut", s26="push", s27="whip", s28="pull", s29="cut", s30="cut", s31="push", s32="whip", s33="cut", s34="cut", s35="cut",
            s36="dissolve", s37="push", s38="cut", s39="pull", s40="push", s41="whipv", s42="pull", s43="dissolve", s44="whipv", s45="cut", s46="cut", s47="cut",
            s48="push", s49="cut", s50="cut", s51="cut", s52="cut", s53="cut", s54="whip", s55="cut")
# 速さの山（作り方の直し 1-1）：人が動かない・エフェクトが出ない、カメラが寄るだけのクリップ
RAMP = {"s05b", "s13", "s31", "s37", "s47", "s51", "s36", "s05a"}
# 止め絵を使う場面の元（still）：(元の場面, 使う絵 or クリップ, 切り出しの倍率, cx, cy)
STILL = dict(s21=("s16", "clip", 1.25, 0.5, 0.62), s22=("s02", "start", 1.0, 0.5, 0.5), s46=("s43", "end", 1.0, 0.5, 0.5), s48=("s38", "end", 1.0, 0.5, 0.5),
             s49=("s12a", "clip", 1.2, 0.5, 0.45), s50=("s24", "clip", 1.0, 0.5, 0.5), s54=("s54", "start", 1.0, 0.5, 0.5))
# アプリ：つなぎ・速さの山・止め絵は、場面の表（指示/shots.json の join・ramp・still）から
JOIN, RAMP, STILL = _zg.JOIN(), _zg.RAMP(), _zg.STILL()


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout or 0)


def spans():
    # 文ごとの区切り：前の文の終わりと次の文の始めの、まん中
    out = []
    order = [s for s in SHOTS]
    for i, s in enumerate(order):
        n = s["sent"][0]; a = SEN[n]["t0"]; b = SEN[n]["t1"]
        if "part" in s:
            f0, f1 = s["part"]
            cs = [c for c in CH if c["n"] == n]
            def at(f):
                if f <= 0: return a
                if f >= 1: return b
                tt = a + (b - a) * f
                return min((c["t0"] for c in cs), key=lambda x: abs(x - tt))
            a, b = at(f0), at(f1)
        out.append([s["id"], a, b])
    res = []
    for i, (sid, a, b) in enumerate(out):
        t0 = 0.0 if i == 0 else res[-1][2]
        if i + 1 < len(out):
            na = out[i + 1][1]
            t1 = round((b + na) / 2, 3) if na > b else round(na - 0.05, 3)
        else:
            t1 = END
        res.append([sid, round(t0, 3), t1])
    return res


def main():
    sp = spans(); clips = []; cam = []; sfx = []; tl = []
    side = 1
    for i, (sid, t0, t1) in enumerate(sp):
        s = BYID[sid]; d = t1 - t0
        if sid in STILL:
            src, what, sc, cx, cy = STILL[sid]
            if what == "clip":
                path = _zg.clip_path(src); L = dur(path) or 3.0
                a = max(0.0, L - d / 0.85) if sid != "s21" else 0.2
                b = min(L, a + d * (0.5 if sid == "s21" else 0.85))
                keys = [[t0, a], [t1, b]]
            else:
                img = _zg.still_image(src, what)
                path = f"{W}/work/still_{sid}.mp4"
                if not os.path.exists(path) and os.path.exists(img):
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-i", img, "-t", "6", "-r", "24", "-vf", "scale=1024:1536", "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", path], check=True)
                keys = [[t0, 0.0], [t1, min(5.9, d)]]
            clips.append(dict(name=sid, src=path, t0=t0, t1=t1, keys=keys, interp=False))
            base = sc
        else:
            path = _zg.clip_path(sid); L = dur(path) or float(s["clip"])
            if sid in RAMP and d >= 1.2:
                keys = [[t0, 0.1], [t0 + 0.3, L * 0.5], [t1, L]]
            elif d <= L:
                keys = [[t0, L - d], [t1, L]]          # 頭を切って、終わりのコマまで使う（15-5 の 11）
            else:
                keys = [[t0, 0.0], [t1, L]]            # 足りない時は、ゆっくり（0.7倍まで）
            clips.append(dict(name=sid, src=path, t0=t0, t1=t1, keys=keys, interp=sid in RAMP))
            base = 1.0; cx = cy = 0.5
        # 編集のカメラ：場面の中は、ゆっくり寄る（1.00→1.05）。つなぎの前後は、振る・入る
        j = JOIN.get(sid, "cut"); jn = JOIN.get(sp[i + 1][0], "cut") if i + 1 < len(sp) else "cut"
        z0, z1 = base * 1.02, base * 1.07
        din = 1 if i % 2 == 0 else -1          # この場面の入りの向き（前の場面の出と同じ）
        dout = 1 if (i + 1) % 2 == 0 else -1   # この場面の出の向き（次の場面の入りと同じ）
        if s["kind"] == "still" and sid in STILL:
            cx, cy = STILL[sid][3], STILL[sid][4]
        # 入り
        if j == "whip":
            cam += [[t0, z0 + 0.25, cx - 0.12 * din, cy], [t0 + 0.2, z0, cx, cy, "out"]]
        elif j == "whipv":
            cam += [[t0, z0 + 0.25, cx, cy - 0.12 * din], [t0 + 0.2, z0, cx, cy, "out"]]
        elif j == "push":
            cam += [[t0, z0 + 0.45, cx, cy], [t0 + 0.22, z0, cx, cy, "out"]]
        elif j == "pull":
            cam += [[t0, max(1.0, z0 - 0.0) + 0.5, cx, cy], [t0 + 0.25, z0, cx, cy, "out"]]
        else:
            cam += [[t0, z0, cx, cy]]
        # 出
        tail = 0.18 if jn in ("whip", "whipv", "push", "pull") else 0.0
        cam += [[t1 - tail, z1, cx, cy, "lin"]]
        if jn == "whip":
            cam += [[t1, z1 + 0.25, cx + 0.12 * dout, cy, "in"]]
        elif jn == "whipv":
            cam += [[t1, z1 + 0.25, cx, cy + 0.12 * dout, "in"]]
        elif jn == "push":
            cam += [[t1, z1 + 0.6, cx, cy, "in"]]
        elif jn == "pull":
            cam += [[t1, max(1.0, z1 - 0.06), cx, cy, "in"]]
        # 効果音（つなぎ）
        if i > 0:
            if j in ("whip", "whipv"):
                sfx.append(["S/01-場面転換のシュッ/シュッ（深い・短い）.wav", t0, 19, 0.9, f"{sid} 振ってつなぐ"])
            elif j == "push":
                sfx.append(["Z/whooshLand.wav", t0, 17, None, f"{sid} 中へ入る"])
                sfx.append(["S/02-低いドン・着地/映画風のドン（やわらかい）.wav", t0 + 0.22, 16, 0.7, f"{sid} 着く"])
            elif j == "pull":
                sfx.append(["S/01-場面転換のシュッ/シュッ（短い）.wav", t0, 19, None, f"{sid} 外へ引く"])
            elif j == "cut":
                sfx.append(["S/01-場面転換のシュッ/シュッ（軽い・短い）.wav", t0, 23, None, f"{sid} 切りかえ"])
        if j == "dissolve": clips[-1]["dip"] = True
        tl.append(dict(id=sid, t0=t0, t1=t1, join=j, sent=s["sent"], kind=s["kind"], src=clips[-1]["src"], keys=clips[-1]["keys"]))
    plan = dict(fps=24, W=1080, H=1920, shutter=0.5, clips=clips, cam=cam)
    json.dump(plan, open(W + "/work/plan.json", "w"), ensure_ascii=False, indent=0)
    json.dump(dict(end=END, voice_end=VOICE_END, shots=tl, sfx_join=sfx), open(W + "/work/timeline.json", "w"), ensure_ascii=False, indent=1)
    for x in tl: print(x["id"], x["t0"], x["t1"], round(x["t1"] - x["t0"], 2), x["join"])
    print("尺", END, "場面", len(tl))
    _zg.warn_missing(clips)


if __name__ == "__main__":
    main()
