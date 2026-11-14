"""クリップを作る（Higgsfield kling_o3_flf・pro・音なし。tools/clip.sh）。同時に3本まで・合計340クレジットまで・作り直しは1本に1回まで。
usage: clips.py plan          → 指示/clip_<場面>.txt を書く
       clips.py run [場面...]  → 絵がそろった物から打つ（できている物は飛ばす）
       clips.py redo 場面 [足す文] → 作り直し（1本に1回まで）
"""
import json, os, sys, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import SHOTS, BYID
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); P = W + "/指示"; CD = W + "/クリップ/847"
CAP = 340
os.makedirs(CD, exist_ok=True)


def prompt(s):
    person = s["kind"] in ("person", "cutp")
    src = s if s.get("content", "").startswith("(made") is False else BYID[s["from_shot"][0]]
    desc = src["content"].split(" Keep everything inside")[0]
    fixed = s.get("fixed", "the background")
    t = f"{desc} FIXED THINGS: {fixed} are fixed in place; only {'the person' if person else 'the parts named in the ACTION'} and the camera move. "
    t += f"ACTION, in order, big and clear: {s['act']}. "
    if person and s["kind"] == "person" and "walk" not in s["act"] and "shuffles" not in s["act"]:
        t += "Her feet stay on the same spots the whole time; she does not walk. "
    t += (f"PHYSICS: {fixed} do not move at all: nobody touches them, so they stay exactly where they are, in the same pose, from the first frame to the last. "
          "Nothing falls, tips over, rolls, slides, opens or closes by itself. ")
    t += f"HANDS: {s.get('hands', 'no hands are in the frame')}. No other hand, arm, finger or person ever enters the frame. Solid things never pass through each other. "
    if s.get("attached"):
        t += f"ATTACHED: {s['attached']} the whole time, at the same point; they move only together with the body, never slip off, never pass through the body, never float. "
    if s.get("contact"):
        t += f"CONTACT: {s['contact']}. "
    if s["kind"] == "cutp":
        t += "The transparent cutaway window stays glued to the same place on her body; the spine, the muscles and the vessels keep the same shape, size, number and position except the change named in the ACTION. "
    t += f"CAMERA: {s['cam']}. LENS: {'a handheld wide-angle lens close to the subject' if person else 'a macro lens'}. Nothing passes in front of the lens. "
    t += "FOCUS: keep the shallow depth of field of the first frame: the subject stays in focus and the background stays softly out of focus. "
    t += ("BACKGROUND: solid 3D geometry; the objects only shift by correct parallax. Nothing appears, disappears, multiplies or changes shape, size or color. Natural real-time speed. No cuts, no scene change. ")
    if person:
        t += ("Same 3D game-engine render style, same skin, same hair, same light, same coral-pink long-sleeve top and gray trousers from first frame to last. "
              "The face keeps its shape and stays the same 3D game character the whole time. ")
    else:
        t += "Same 3D game-engine render style and the same colors from first frame to last. "
    t += "The camera never stops. No text, no captions, no subtitles, no logos."
    return t


def todo():
    return [s for s in SHOTS if s.get("clip")]


def used():
    f = W + "/クリップ/credits.log"
    return sum(float(l.split()[3]) for l in open(f)) if os.path.exists(f) else 0.0


def tries(sid):
    f = W + "/クリップ/credits.log"
    return sum(1 for l in open(f) if l.split()[1] == sid) if os.path.exists(f) else 0


def launch(s):
    a = f"{W}/絵/{s['id']}_始め.png"; b = f"{W}/絵/{s['id']}_終わり.png"
    return subprocess.Popen(["perl", "-e", "alarm 1080; exec @ARGV", "zsh", W + "/tools/clip.sh", "847", s["id"], a, b, str(s["clip"]), f"{P}/clip_{s['id']}.txt", str(CAP)],
                            stdout=open(f"{CD}/{s['id']}.run.txt", "a"), stderr=subprocess.STDOUT)


def run(names):
    for s in todo():
        open(f"{P}/clip_{s['id']}.txt", "w").write(prompt(s) + ((" " + open(f"{P}/clip_{s['id']}.extra.txt").read().strip()) if os.path.exists(f"{P}/clip_{s['id']}.extra.txt") else ""))
    want = [s for s in todo() if not names or s["id"] in names]
    running = {}
    while True:
        for k, pr in list(running.items()):
            if pr.poll() is not None: del running[k]
        left = [s for s in want if not os.path.exists(f"{CD}/{s['id']}.mp4") and s["id"] not in running and tries(s["id"]) < 2]
        ready = [s for s in left if os.path.exists(f"{W}/絵/{s['id']}_始め.png") and os.path.exists(f"{W}/絵/{s['id']}_終わり.png")]
        if os.environ.get("APPROVE"):
            ok = set(open(W + "/work/approved.txt").read().split()) if os.path.exists(W + "/work/approved.txt") else set()
            ready = [s for s in ready if s["id"] in ok]
            if os.path.exists(W + "/work/clips_stop"): break
        while ready and len(running) < 3:
            s = ready.pop(0)
            if used() + {3: 3.75, 4: 5, 5: 6.25}[s["clip"]] > CAP: print("上限"); ready = []; break
            running[s["id"]] = launch(s); time.sleep(3)
        if not running and not ready:
            # 絵を待っている物があるか
            wait = [s for s in left if not (os.path.exists(f"{W}/絵/{s['id']}_始め.png") and os.path.exists(f"{W}/絵/{s['id']}_終わり.png"))]
            if (not wait and not os.environ.get("APPROVE")) or os.environ.get("NOWAIT"): break
        time.sleep(10)
    print("使ったクレジット", used(), "無い:", [s["id"] for s in want if not os.path.exists(f"{CD}/{s['id']}.mp4")])


if __name__ == "__main__":
    c = sys.argv[1]
    if c == "plan":
        for s in todo():
            open(f"{P}/clip_{s['id']}.txt", "w").write(prompt(s))
        print(len(todo()), "本", sum({3: 3.75, 4: 5, 5: 6.25}[s["clip"]] for s in todo()), "クレジットの見こみ")
    elif c == "run":
        run(sys.argv[2:])
    elif c == "redo":
        sid = sys.argv[2]
        if tries(sid) >= 2: sys.exit("作り直しは1回まで")
        if len(sys.argv) > 3: open(f"{P}/clip_{sid}.extra.txt", "a").write(" " + sys.argv[3])
        f = f"{CD}/{sid}.mp4"
        if os.path.exists(f): os.rename(f, f"{CD}/{sid}.v1.mp4")
        run([sid])
