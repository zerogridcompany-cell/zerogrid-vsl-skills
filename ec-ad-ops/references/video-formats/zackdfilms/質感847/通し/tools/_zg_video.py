"""アプリ（Zero Grid）で、通しの編集の道具（plan.py・render2.py・compose.py・timing.py・clipcheck.py）を回すための共通の部品。
元の道具は「tools の1つ上」を作業フォルダとして読み、1本の動画（針マット_14）の場面の表（shots.py）と、社内の音の棚を直に読んでいた。
アプリでは、同梱する時（scripts/bundle-skills.mjs の SCRIPT_PATCH）に、その所だけをこの部品に向ける。

作業フォルダ：アプリの run_skill_script が、1つ目の引数の作業フォルダを cwd にして、ZG_WORK で渡す（例 <商品>/07_納品/VSL/packA/作業/）。
  指示/shots.json   場面の表（shots.py の SHOTS の代わり）。[{"id":"s01","sent":[1],"clip":3,"kind":"person","join":"cut", …}, …]
                    id：場面の名前（クリップの名前と同じ）／sent：声の何文目か（timing.json の n）／part：[0〜1, 0〜1] 文の一部だけの時
                    clip：作った動画の秒（3・4・5）／kind：person・cutp・cut・still ほか／join：前の場面とのつなぎ（cut・whip・whipv・push・pull・dissolve）
                    ramp：true＝速さの山（人が動かない・寄るだけのクリップ）／still：[元の場面, "clip"|"start"|"end", 倍率, 中心x, 中心y]（止め絵で見せる場面）
                    start・end：始めと終わりの絵の道（商品フォルダか作業フォルダからの道。無ければ 絵/<id>_始め.png）／clip_file：使う動画の道（無ければ下の順で探す）
  声/vo_raw.wav     録った声（全文1回）。声/sentences.json [{"n":1,"disp":"字幕の文"}]・声/fa.json（elevenlabs_align）→ timing.py → 声/timing.json
  声/読み.json      任意。{"REP":[["朝7時","朝しちじ"]], "SUB":[["おろそう","下ろそう"]]}（字幕の字と声の読みの差。timing.py）
  クリップ          <作業>/クリップ/847/<id>.mp4 → <作業>/クリップ/<id>.mp4 → <商品>/07_納品/動画/クリップ/<id>.mp4（Higgsfield の道具の置き場）の順に探す
  音/BGM/           任意。曲を1つ置くと入る（声の約20dB下・1曲を通す）。無ければ曲なし
  音/効果音/        任意。効果音の棚（plan.py の "S/…"・"Z/…" はこの下の S/・Z/）。無い音は飛ばす
  指示/bgm.json     任意。{"hook_until": 3, "cause": [5, "言葉"], "product_from": 36, "close_from": 47}（曲の大きさの山。sound-rules 4章）
  fx.json・badges.json・work/sfx_extra.json  任意（指す輪・札・場面の出来事の効果音。overlays.py と同じ形で write_file で書く）
"""
import json, os, re, subprocess

W = os.path.abspath(os.environ.get("ZG_WORK") or os.getcwd())
os.makedirs(os.path.join(W, "work"), exist_ok=True)
_P = os.environ.get("ZG_PRODUCT") and os.environ.get("EC_ROOT") and os.path.join(os.environ["EC_ROOT"], os.environ["ZG_PRODUCT"])
PRODUCT = _P if _P and os.path.isdir(_P) else None


def _json(rel, default=None):
    f = os.path.join(W, rel)
    if not os.path.exists(f):
        return default
    with open(f, encoding="utf-8") as fh:
        return json.load(fh)


_SHOTS = None


def shots():
    """指示/shots.json の場面の表"""
    global _SHOTS
    if _SHOTS is not None:
        return _SHOTS
    d = _json("指示/shots.json")
    if d is None:
        raise SystemExit("指示/shots.json（場面の表）がありません。形は _zg_video.py の頭の説明を見る")
    L = d["shots"] if isinstance(d, dict) else d
    seen = set()
    for i, s in enumerate(L):
        if not isinstance(s, dict) or not s.get("id"):
            raise SystemExit(f"指示/shots.json の {i + 1} 番目に id がありません")
        if s["id"] in seen:
            raise SystemExit(f"指示/shots.json の id「{s['id']}」が2つあります")
        seen.add(s["id"])
        if isinstance(s.get("sent"), int):
            s["sent"] = [s["sent"]]
        if not s.get("sent"):
            raise SystemExit(f"場面 {s['id']} に sent（声の何文目か）がありません")
        s.setdefault("kind", "person")
        s.setdefault("clip", 3)
    _SHOTS = L
    return L


def JOIN():
    return {s["id"]: s.get("join", "cut") for s in shots()}


def RAMP():
    return {s["id"] for s in shots() if s.get("ramp")}


def STILL():
    return {s["id"]: tuple(s["still"]) for s in shots() if s.get("still")}


def _resolve(p):
    if not p:
        return None
    for base in [W, PRODUCT]:
        if base:
            q = p if os.path.isabs(p) else os.path.join(base, p)
            if os.path.exists(q):
                return os.path.abspath(q)
    if PRODUCT and p.startswith(os.environ.get("ZG_PRODUCT", "\0") + "/"):
        q = os.path.join(os.environ["EC_ROOT"], p)
        if os.path.exists(q):
            return q
    return None


def _shot(sid):
    try:
        return next(s for s in shots() if s["id"] == sid)
    except (StopIteration, SystemExit):
        return {}


def clip_path(sid):
    """場面のクリップの道（無ければ、置かれるはずの道）"""
    s = _shot(sid)
    f = _resolve(s.get("clip_file"))
    if f:
        return f
    dirs = [os.path.join(W, "クリップ", "847"), os.path.join(W, "クリップ")]
    if PRODUCT:
        dirs.append(os.path.join(PRODUCT, "07_納品", "動画", "クリップ"))
    for d in dirs:
        q = os.path.join(d, f"{sid}.mp4")
        if os.path.exists(q):
            return q
    return os.path.join(dirs[-1], f"{sid}.mp4")


def still_image(src, what):
    """止め絵の場面の元の絵（start＝始め・end＝終わり）"""
    s = _shot(src)
    f = _resolve(s.get("start" if what == "start" else "end"))
    if f:
        return f
    return os.path.join(W, "絵", f"{src}_{'始め' if what == 'start' else '終わり'}.png")


def warn_missing(clips):
    miss = [c["name"] for c in clips if not os.path.exists(c["src"])]
    if miss:
        print("まだ無いクリップ（render2.py の前にそろえる）:", " ".join(miss))


def readings(kind):
    d = _json("声/読み.json", {}) or {}
    return [tuple(x) for x in d.get(kind, [])]


# 自社の音の棚（効果音の Z と BGM）。ZG_SOUNDS で場所を渡す。無ければ、この道具の上のフォルダを順に見て「音の棚」を探す（リポジトリの一番上にある）
def _find_sounds():
    d = os.path.dirname(os.path.abspath(__file__))
    for _ in range(12):
        c = os.path.join(d, "音の棚")
        if os.path.exists(os.path.join(c, "sounds.json")):
            return c
        d = os.path.dirname(d)
    return ""


SOUNDS = os.environ.get("ZG_SOUNDS") or _find_sounds()


def _sounds():
    p = os.path.join(SOUNDS, "sounds.json")
    return json.load(open(p, encoding="utf-8")) if SOUNDS and os.path.exists(p) else None


def _bgm_file():
    """曲：作業フォルダの 音/BGM/ に置いた物 → 指示/bgm.json の track（同梱の曲の id）→ 型の既定の曲（ZackDFilms は W-MOOD-27）"""
    for d in [os.path.join(W, "音", "BGM"), os.path.join(W, "音")]:
        if os.path.isdir(d):
            for n in sorted(os.listdir(d)):
                if n.lower().endswith((".wav", ".mp3", ".m4a", ".aac", ".flac")) and (d.endswith("BGM") or n.lower().startswith("bgm")):
                    return os.path.join(d, n)
    S = _sounds()
    if not S:
        return None
    cfg = _json("指示/bgm.json") or {}
    if cfg.get("track") == "none":
        return None
    want = cfg.get("track") or S.get("default_bgm", {}).get("zackdfilms")
    for b in S.get("bgm", []):
        if b["id"] == want:
            p = os.path.join(SOUNDS, b["file"])
            return p if os.path.exists(p) else None
    return None


def _sfx_file(f):
    """効果音：作業フォルダの 音/効果音/ → 同梱の自社の音（Z/ はそのまま。S/ は他社のパックなので、役目の同じ Z の音に置きかえる）"""
    base = os.path.join(W, "音", "効果音")
    if f.startswith("Z/") or f.startswith("S/"):
        p = os.path.join(base, f)
    else:
        p = f if os.path.isabs(f) else os.path.join(base, f)
    if os.path.exists(p):
        return p
    S = _sounds()
    if not S:
        return None
    sd = os.path.join(SOUNDS, S.get("sfx_dir", "効果音"))
    if f.startswith("Z/"):
        q = os.path.join(sd, f)
    elif f.startswith("S/"):
        role = f.split("/")[1] if f.count("/") >= 2 else ""
        z = S.get("s_fallback", {}).get(role)
        q = os.path.join(sd, "Z", z) if z else ""
    else:
        q = ""
    return q if q and os.path.exists(q) else None


def _bgm_vol(CH):
    """曲の大きさの山（指示/bgm.json がある時だけ。無ければ一定）"""
    cfg = _json("指示/bgm.json")
    if not cfg:
        return "1"
    sen = {s["n"]: s for s in _json("声/timing.json")["sentences"]}
    parts = []
    try:
        if cfg.get("close_from") in sen:
            parts.append((f"gte(t,{sen[cfg['close_from']]['t0'] - 0.2:.2f})", "0.708"))
        if cfg.get("product_from") in sen:
            parts.append((f"gte(t,{sen[cfg['product_from']]['t0'] - 0.2:.2f})", "1.259"))
        if cfg.get("cause"):
            n, w = cfg["cause"][0], cfg["cause"][1] if len(cfg["cause"]) > 1 else ""
            c = [x for x in CH if x["n"] == n and w in x["text"]]
            ct = c[0]["t0"] if c else sen[n]["t0"]
            parts.insert(0, (f"between(t,{ct - 1:.2f},{ct + 0.5:.2f})", "0.5"))
        if cfg.get("hook_until") in sen:
            parts.insert(0, (f"lt(t,{sen[cfg['hook_until']]['t1']:.2f})", "0.631"))
    except (KeyError, IndexError, TypeError):
        print("指示/bgm.json の文の番号が timing.json に無いので、曲の大きさは一定にした")
        return "1"
    expr = "1"
    for cond, val in reversed(parts):
        expr = f"if({cond},{val},{expr})"
    return expr


def compose_audio(TL, END, CH, lufs, htp):
    """compose.py の audio() と同じ混ぜ方（声 −14 LUFS・効果音・曲を声の20dB下）。曲・効果音の棚が無ければ、その分を飛ばす"""
    notes = []
    vo_in = os.path.join(W, "声", "vo_raw.wav")
    if not os.path.exists(vo_in):
        raise SystemExit("声/vo_raw.wav（録った声）がありません")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", vo_in, "-af", f"apad=whole_dur={END},acompressor=threshold=-24dB:ratio=3:attack=5:release=80,loudnorm=I=-14:TP=-1.5:LRA=7,aresample=48000,atrim=0:{END}",
                    "-ar", "48000", "-ac", "2", "work/vo.wav"], check=True)
    vg = -14.0 - lufs("work/vo.wav")
    SFX = TL["sfx_join"] + (json.load(open("work/sfx_extra.json", encoding="utf-8")) if os.path.exists("work/sfx_extra.json") else [])
    SFX = sorted(SFX, key=lambda r: r[1])
    keep = []
    for r in SFX:
        if keep and r[1] - keep[-1][1] < 0.3 and "着く" not in r[4] and "ピキッ" not in r[4]:
            continue
        keep.append(r)
    have, missing = [], []
    for r in keep:
        p = _sfx_file(r[0])
        (have if p else missing).append((r, p))
    if missing:
        notes.append(f"効果音 {len(missing)} 個は 音/効果音/ にも同梱の棚にも無いので飛ばした（{', '.join(sorted({m[0][0] for m in missing}))[:300]}）")
    BGM = _bgm_file()
    if not BGM:
        notes.append("曲（BGM）なし：同梱の曲が見つからない（指示/bgm.json の track を確かめる）か、track が none")
    ins = ["-i", "work/vo.wav"]
    fc = f"[0:a]volume={vg:.2f}dB,alimiter=limit=0.84:attack=1:release=40:level=false[vo];"
    k = 1
    bgm_gain = None
    if BGM:
        bl = lufs(BGM); bgm_gain = (-14 - 20) - bl
        vol = _bgm_vol(CH)
        fc += (f"[{k}:a]aloop=loop=-1:size=2e9,atrim=0:{END},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo,volume={bgm_gain:.2f}dB,"
               f"volume='{vol}':eval=frame,afade=t=in:d=0.3,afade=t=out:st={max(0.0, END - 2.0)}:d=2.0[bgm];")
        ins += ["-i", BGM]; k += 1
    mix = []; log = []
    for n, ((f, t, below, L, note), p) in enumerate(have):
        h = htp(p); st = max(0.0, t - h); lv = lufs(p)
        if lv < -40:
            lv = -16.0
        g = (-14 - below) - lv
        trim = f"atrim=0:{L},afade=t=out:st={max(0.01, L - 0.08)}:d=0.08," if L else ""
        fc += f"[{k}:a]aformat=sample_rates=48000:channel_layouts=stereo,{trim}volume={g:.2f}dB,adelay={int(st * 1000)}|{int(st * 1000)}[s{n}];"
        ins += ["-i", p]; k += 1; mix.append(f"[s{n}]"); log.append(dict(file=os.path.basename(p), start=round(st, 3), peak=t, below=below, note=note))
    if mix:
        fc += "".join(mix) + f"amix=inputs={len(mix)}:normalize=0,volume=-2.5dB[fx];"
    parts = ["[vo]"] + (["[bgm]"] if BGM else []) + (["[fx]"] if mix else [])
    fc += "".join(parts) + (f"amix=inputs={len(parts)}:normalize=0," if len(parts) > 1 else "anull,") + f"atrim=0:{END},alimiter=limit=0.84:attack=1:release=50:level=false[a]"
    open("work/audio_fc.txt", "w", encoding="utf-8").write(fc)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y"] + ins + ["-filter_complex_script", "work/audio_fc.txt", "-map", "[a]", "-ar", "48000", "work/mix.wav"], check=True)
    base = fc.split("".join(parts))[0]
    for tag in (["bgm"] if BGM else []) + (["fx"] if mix else []):
        sinks = ";".join(f"{x}anullsink" for x in parts if x != f"[{tag}]")
        open(f"work/fc_{tag}.txt", "w", encoding="utf-8").write(base + sinks + f";[{tag}]anull[a]")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y"] + ins + ["-filter_complex_script", f"work/fc_{tag}.txt", "-map", "[a]", "-ar", "48000", f"work/stem_{tag}.wav"], check=True)
    json.dump(dict(voice_gain=vg, bgm=os.path.basename(BGM) if BGM else None, bgm_gain=bgm_gain, sfx=log, notes=notes), open("work/build_log.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for n in notes:
        print("※", n)
