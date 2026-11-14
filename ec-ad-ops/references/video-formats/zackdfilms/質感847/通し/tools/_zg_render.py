"""アプリ：render2.py を時間で区切って同時に書き出し、最後に継ぐ（出来上がりの絵は1本で回した時と同じ。継ぎ目は動画の圧縮の区切りだけ）。
親の回：先に全クリップの中間コマ（upsampled）を作ってから、子の回を K 本立てる（同じファイルを同時に作らない）→ ffmpeg の concat で継ぐ → 親は終わる。
子の回（環境変数 ZG_SEG=1）：ZG_F0〜ZG_F1 のコマだけ書く。
K：Mac のコアの数まで・24コマ（1秒）に1本まで。ZG_RENDER_JOBS で上限（1 で区切らない）。"""
import json, os, subprocess, sys


def frames(nfr):
    if os.environ.get("ZG_SEG"):
        return int(os.environ.get("ZG_F0", 0)), min(nfr, int(os.environ.get("ZG_F1", nfr)))
    return 0, nfr


def split(plan, OUT, FPS, upsampled):
    if os.environ.get("ZG_SEG"):
        try:
            import cv2; cv2.setNumThreads(1)
        except Exception:
            pass
        return
    nfr = int(round(plan["clips"][-1]["t1"] * FPS))
    K = max(1, min(os.cpu_count() or 2, nfr // 24, int(os.environ.get("ZG_RENDER_JOBS", "99"))))
    if K <= 1:
        return
    # クリップの中間コマ（72コマ/秒）を、先に同時に作る（子の回が同じファイルを同時に作らないように）
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max(1, (os.cpu_count() or 2) // 2)) as ex:
        list(ex.map(upsampled, plan["clips"]))
    step = -(-nfr // K); segs = []; procs = []
    for k in range(K):
        f0, f1 = k * step, min(nfr, (k + 1) * step)
        if f0 >= f1:
            break
        so = OUT.replace(".mp4", f"_seg{k}.mp4"); segs.append(so)
        env = {**os.environ, "ZG_SEG": "1", "ZG_F0": str(f0), "ZG_F1": str(f1), "OMP_NUM_THREADS": "1"}
        procs.append(subprocess.Popen([sys.executable, "-B", os.path.abspath(sys.argv[0]), sys.argv[1], so], env=env))
    bad = [i for i, p in enumerate(procs) if p.wait() != 0]
    if bad:
        print("区切って書き出した所が失敗した：", bad, file=sys.stderr); sys.exit(1)
    lst = OUT.replace(".mp4", "_segs.txt")
    with open(lst, "w") as f:
        for so in segs:
            f.write("file '" + os.path.abspath(so).replace("'", "'\\''") + "'\n")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", OUT], check=True)
    log = []
    for so in segs:
        m = so.replace(".mp4", "_map.json")
        if os.path.exists(m):
            log += json.load(open(m)); os.remove(m)
        os.remove(so)
    os.remove(lst)
    json.dump(log, open(OUT.replace(".mp4", "_map.json"), "w"))
    print("frames", len(log), OUT, f"（{len(segs)} 本に区切って同時に書き出した）")
    sys.exit(0)
