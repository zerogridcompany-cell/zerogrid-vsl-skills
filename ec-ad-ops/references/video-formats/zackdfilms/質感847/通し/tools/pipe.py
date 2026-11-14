"""絵を作る（18章の段0〜5）。shots.py から仕事の表を作り、Codex（tools/gen.sh）で同時に3本まで回す。止まっても、できた絵は飛ばして続きから。
usage: pipe.py plan            → work/jobs.json と 指示/*.txt を書くだけ
       pipe.py run [名前...]    → 回す（名前を渡すと、その仕事と、その前に要る仕事だけ）
       pipe.py redo 名前 [足す文] → その絵を消して作り直す（足す文は指示の最後に足す）
出す先：work/gen/<名前>.png。始めの絵＝絵/<場面>_始め.png、終わりの絵＝絵/<場面>_終わり.png
"""
import json, os, sys, subprocess, time, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shots import SHOTS, BYID, REF, DOF
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); G = W + "/work/gen"; P = W + "/指示"
os.makedirs(G, exist_ok=True); os.makedirs(P, exist_ok=True); os.makedirs(W + "/絵", exist_ok=True)
PY = os.path.expanduser("_env/venv/bin/python")
LIMIT = 320

ROLE = dict(
    A2="match this skin and face modeling exactly: smooth porcelain CG skin with no pores, warm red-orange shading in the eyelid creases and nostrils, simple painted eyebrows, glassy eyes, hair as smooth clumped strands. Do not copy this face itself.",
    A3="match this older CG face: the same smooth game skin with soft painted age shading (no photographic wrinkles), hair rendered as smooth clumped strands. Do not copy this face itself.",
    B9="match this cloth rendering: one flat color with a few broad soft baked folds, no fabric weave. Do not copy the garment itself.",
    B10="match this T-shirt rendering: one flat color, a few broad baked folds. Do not copy the garment itself.",
    B11="match this wall-surface rendering (clean cyan-blue surfaces, soft even light). Do not copy the room.",
    S2="match these surfaces: the left part shows how cloth is rendered, the right part how a cyan-blue wall is rendered. Copy only the surface look.",
    C13="match this CG hand: a simple game-mesh hand, smooth skin, simplified knuckles. Do not copy the hand itself.",
    C14="match this rendering of a hand and cloth. Do not copy them.",
    D16="match this rendering of anatomy: clean glossy red tissue with soft painted striations, like a science-explainer animation. Do not copy its organs.",
    D18="match this rendering of bone (ivory white) and fat (yellow) in a clean cutaway. Do not copy its shapes.",
    E20="match this macro rendering of smooth 3D skin. Do not copy the face.",
    MAT="the REAL PRODUCT (a photo): reproduce the pink acupressure mat (white round flower-shaped discs in tight rows on a pink pad, a pink half-cylinder pillow) and the black drawstring cylinder bag exactly in shape, color and pattern, rendered in the same 3D look; ignore the photo's white background and its photo lighting.",
)
LOOK1 = ("Image 1 is a frame from the 3D-animated short whose look we must match. Match its RENDERING exactly: the same CG character shading, the same smooth, low-detail skin and cloth, "
         "the same soft game-engine lighting with cyan bounce light, the same color grade, contrast, softness and video compression. Take only the look and the camera language from it; "
         "do NOT copy its person, its objects, its posters or its room layout.")
NOTXT = "No text, no captions, no letters, no numbers, no logos, no watermark anywhere."
QUIRK = ("ENGINE QUIRKS (a real-time game-engine render, not offline CG, not an illustration): skin and cloth have a soft waxy satin sheen; folds look like a few broad creases baked into the mesh; "
         "hair is clumped polygon hair cards with a few stray card tips and one streaky highlight; contact shadows are weak and soft (ambient occlusion only); slightly flat, even game lighting.")
AGE = " AGE AND FACE: she must look clearly in her mid-50s exactly like Image 2: a round, full, slightly heavy face with soft cheeks and a slightly wide nose, ordinary and plain; NOT young, NOT pretty, NOT idealized, NOT a 30-year-old."
PERSON3 = """LOOK OF THE PERSON (stock real-time 3D figure of a mid-budget YouTube 3D animation, Unreal / iClone / Character Creator default character; NOT a photo, NOT an AI beauty render, NOT anime, NOT Pixar):
- PROPORTIONS: realistic stock adult head and body, plain average middle-aged face, slightly uncanny; normal-size eyes, real nose and chin; not cute, not idealized, not caricatured.
- SKIN: uniform waxy, slightly plastic real-time skin shader, smooth and even, weak specular with a faint plastic sheen; color only from simple flat painted patches (a bit of redness at nose tip, ears and eyelid rims). No photographic skin, no soft airbrushed gradients.
- BROWS: flat painted brow shapes sitting on the skin surface (a texture), not sculpted, not hairy.
- EXPRESSION: limited blendshapes: brows and mouth move in a stiff stock pose; the skin NEVER creases (no forehead lines, no frown lines, no crow's feet, no nasolabial folds); lips a simple rubbery shape; teeth a plain uniform row; eyes glassy and slightly dead.
- HAIR: discrete game HAIR CARDS: visible separate flat clumps/cards with crisp geometric edges and a few stray card strands, a glossy engine sheen band across the hair; NOT soft wispy hair, NOT airbrushed, NOT sculpted chunky spikes.
- HANDS: simple game-mesh hands, stiff grip, simplified knuckles, exactly five fingers each.
- CLOTH: simple stiff cloth mesh, plain uniform color, a few baked folds, no fabric weave.
- LIGHT ON HER: flat, slightly harsh real-time engine lighting with simple shadows and crisp silhouette edges; NOT soft cinematic or photographic gradient light, no filmic glow on the person."""
SHADOW = """MAKE THESE CONCRETE CHANGES ON HER, only on the parts of her that are visible in the frame (they must be clearly visible side by side with Image 1):
1. Darken the neck and the area under her jaw strongly (like Image 2), and make the inside of the T-shirt collar almost black.
2. Put a dark, soft-edged shadow band across the top of the forehead and temples, cast by her hair fringe.
3. Darken the eye sockets and upper eyelids to a dull gray-olive; darken the nostrils and the inside of the mouth.
4. Raise the exposure of the up-facing planes by about one stop, as if lit by one big white ceiling light (they become bright pale beige with a faint plastic sheen on forehead and nose): forehead below the shadow band, nose bridge, cheekbones, top of the shoulders, top of the hair (one sheen band), top of the hands.
5. Remove the front fill and the soft beauty glow: the side turned away from the light, the underside of the arms and the lower half of the torso fall to about half brightness.
6. Shadow color: as in Image 2, the light is neutral white and the deep shadows on her skin and shirt pick up a cool blue bounce from the blue surroundings; the lit skin stays a clean natural beige-pink (not orange, not glowing).
7. Coral shirt: deep, darker muted coral-red in every fold, in the armpits, under the bust, under the sleeve cuffs and wherever the arm touches the torso; no glow.
8. Contact shadows: small, tight, dark shadows exactly where she touches something (hands on objects, feet on the floor, back and head on the mat).
BRIGHTNESS LOCK: do NOT darken the picture overall. The room, walls, floor and objects keep exactly the brightness and colors of Image 1. On her, the lit planes stay AS BRIGHT as in Image 1 or brighter; only the creases, contacts and down-facing planes get darker, so her contrast increases. Her skin a little less saturated, never orange. No rim light, no bloom, no warm golden light."""
B5 = ("RE-RENDER Image 1 as a real-time game engine frame (Unreal Engine 4 era, not 5): mid-poly stock character, low-resolution skin texture that looks slightly smeared, simple skin shader with a dull sheen, "
      "hair as a solid mass of hair cards with soft alpha edges, cloth as one flat color with a few broad baked folds, slightly plastic look overall, real-time lighting with soft shadow edges and screen-space "
      "ambient occlusion in creases, mild bloom, video compression softness.")
B5CUT = ("RE-RENDER Image 1 as a real-time game engine frame (Unreal Engine 4 era, not 5): mid-poly 3D models with slightly smeared low-resolution textures, simple shaders with a dull sheen, slightly plastic "
         "look overall, real-time lighting with soft shadow edges and screen-space ambient occlusion in creases, mild bloom, video compression softness.")


def stage_refs(s):
    return [REF[k] for k in s["tex"]] + ([REF["MAT"]] if s.get("mat") and "MAT" not in s["tex"] else [])


def roles(keys, start):
    out = []; k = start
    for key in keys:
        out.append(f"Image {k} = {ROLE[key]}"); k += 1
    return " ".join(out), k


def build():
    jobs = {}; scene_first = {}; scene_prev = {}

    def J(name, prompt, refs, kind="gen", **kw):
        ex = f"{P}/{name}.extra.txt"
        if prompt and os.path.exists(ex):
            prompt = prompt + " " + open(ex).read().strip()
        jobs[name] = dict(name=name, kind=kind, prompt=prompt, refs=refs, **kw)
        if prompt:
            open(f"{P}/{name}.txt", "w").write(prompt)

    for s in SHOTS:
        sid = s["id"]
        if s["kind"] == "still" and "reuse" in s:
            continue
        person = s["kind"] in ("person", "cutp")
        start_png = f"{W}/絵/{sid}_始め.png"; end_png = f"{W}/絵/{sid}_終わり.png"
        if "from_shot" in s:
            src, which = s["from_shot"]
            srcpng = f"{W}/絵/{src}_{'始め' if which == 'start' else '終わり'}.png"
            if s.get("start_edit"):
                J(f"{sid}_s", edit_prompt(s, s["start_edit"], person), [srcpng] + look_refs(s, person), out=start_png, deps=[srcpng])
            else:
                J(f"{sid}_s", None, [srcpng], kind="copy", out=start_png, deps=[srcpng])
        else:
            keys = s["tex"] + (["MAT"] if s.get("mat") and "MAT" not in s["tex"] else [])
            rtxt, k = roles(keys, 2)
            refs = [REF[s["comp"]]] + [REF[x] for x in keys]
            sc = s["scene"]; extra = []
            for prev in [scene_first.get(sc), scene_prev.get(sc)]:
                if prev and prev not in extra and len(refs) + len(extra) < 5:
                    extra.append(prev)
            ptxt = " ".join(f"Image {k + i} = OUR OWN earlier frame of the same place: keep the same room, the same furniture and objects, the same colors{', and the same woman' if person else ''}; this is a new camera position in that same place." for i in range(len(extra)))
            p1 = f"{LOOK1} {rtxt} {ptxt} The result must look like another frame from the SAME animated short: same engine, same asset library, same render settings. CONTENT (our own new, original scene): {s['content']} {NOTXT}"
            n1 = f"{G}/{sid}_1.png"
            J(f"{sid}_1", p1, refs + extra, out=n1, deps=extra)
            scene_first.setdefault(sc, n1); scene_prev[sc] = n1
            # 段2 ぼけ
            if person:
                refs2 = [REF[s["comp"]], REF[s["blur"][0]], REF["B8"], REF[s["blur"][-1]], n1]
                t2 = ("Image 2 = another frame of the SAME short showing its LENS BEHAVIOR. MATCH THIS DEPTH OF FIELD: the same amount of out-of-focus blur, the same thin focus plane and the same soft, creamy out-of-focus areas. Take only the focus behavior from it; do NOT copy its person, objects, room or colors. "
                      "Image 3 = match this character asset: a stock CG woman with simple, slightly soft low-detail skin (no pores), a face that moves as one shape, hair as clumped cards. Do not copy her face. "
                      "Image 4 = another frame of the SAME short showing its LENS BEHAVIOR; match its depth of field the same way. Image 5 = OUR OWN earlier version of THIS shot. Keep the same woman (face, short dark bob with gray strands), the same outfit (coral-pink long-sleeve T-shirt, gray sweatpants), the same place and every object, and the same pose and camera angle. Its rendering is too clean and too sharp; re-render it with the depth of field and engine quirks described here.")
            else:
                refs2 = [REF[s["comp"]], REF[s["blur"][0]], n1]
                t2 = ("Image 2 = another frame of the SAME short showing its LENS BEHAVIOR. MATCH THIS DEPTH OF FIELD: the same amount of out-of-focus blur, the same thin focus plane and the same soft, creamy out-of-focus areas. Take only the focus behavior from it; do NOT copy its objects or colors. "
                      "Image 3 = OUR OWN earlier version of THIS shot. Keep every object, shape, color and the camera angle. Its rendering is too clean and too sharp; re-render it with the depth of field and engine quirks described here.")
            p2 = (f"{LOOK1} {t2} The result must look like another frame from the SAME animated short: same engine, same asset library, same render settings, same lens. CONTENT: {s['content']} {DOF[s['dof']]} {QUIRK} "
                  f"NO MOTION BLUR: nothing is streaked or smeared by movement; only out-of-focus blur from the lens. Do not reduce the depth-of-field blur: it is a real feature of this shot, not a defect. {NOTXT}")
            n2 = f"{G}/{sid}_2.png"; J(f"{sid}_2", p2, refs2, out=n2, deps=[n1])
            last = n2
            if person:
                cut_keep = (" Keep the transparent cut-away anatomy window (spine, muscles, vessels and every colored part) exactly as it is and change only her skin, clothes and any visible part of her face/hair." if s["kind"] == "cutp" else "")
                who = ("she becomes the woman of Image 2 aged about twenty years older (mid-70s, gray short bob, the same round face), " if s.get("old") else "she becomes the woman of Image 2 (our character: her identity, age, face shape, haircut and outfit), ")
                multi = (" There are four women: ONLY the woman in her 50s becomes the woman of Image 2; the other three stay different people of other ages, rendered in the same stock 3D look." if sid == "s18" else "")
                p3 = (f"Image 1 is OUR storyboard frame. EDIT it: keep EVERYTHING about the shot exactly (framing, camera angle, pose, action, place, objects, depth of field, colors of the place). Replace ONLY the woman's look: {who}"
                      f"rendered as one more stock 3D figure of the series in Images 3-5 (same shader, hair cards, cloth and light on the person; do not copy their identity). If the face in Image 1 is cartoon-like (big eyes, small chin, smooth doll face), do NOT keep it; rebuild her head with the realistic stock proportions of Image 2. "
                      f"Her coral-pink top has LONG sleeves reaching the wrists; gray sweatpants.{multi}{cut_keep} If only part of her is visible (hands, legs), change only that visible part.{AGE if not s.get('old') else ''}\n{PERSON3}\nNo text, no logos, no graphic effects except the ones already in Image 1. A single image.")
                n3 = f"{G}/{sid}_3.png"; J(f"{sid}_3", p3, [n2, REF["Y4"], REF["T10"], REF["T07"], REF["T13"]], out=n3, deps=[n2])
                p4 = (f"Image 1 is OUR storyboard frame. EDIT it as a RE-LIGHT of the person: keep the shot exactly (framing, camera angle, pose, action, place, objects, depth of field, colors of the place). Images 2 and 3 are SHADOW EXAMPLES, real frames of the 3D animation series we must match; their role: match this light and shadow on the person (do NOT copy their identity, clothes, logos, phone, room or pose). "
                      f"Image 4 is our character (identity, haircut, outfit only; ignore its flat lighting). Image 5 is another real frame of the series for the stock 3D figure look.{cut_keep}\n{SHADOW}\n"
                      f"She stays a stock real-time 3D figure (not a photo, not Pixar, not anime): realistic adult proportions, plain average face, waxy skin shader, flat painted brows, no expression wrinkles, hair cards. Coral-pink LONG-sleeved top to the wrists, gray sweatpants. No text, no logos. A single image.")
                n4 = f"{G}/{sid}_4.png"; J(f"{sid}_4", p4, [n3, REF["SH1"], REF["SH3"], REF["Y4"], REF["T10"]], out=n4, deps=[n3])
                last = n4
            lr = look_refs(s, person)
            if person:
                p5 = (f"Image 1 is our storyboard frame (layout only). Images 2 and 3 are frames of the 3D animation series we must match. {B5} Same Japanese woman in her 50s{' (here aged about 75)' if s.get('old') else ''}, same haircut, same coral long-sleeve top, same gray sweatpants, same expression and same pose as Image 1 ({s['pose5']}), "
                      f"exactly the same number of hands as Image 1, same place and background blur. Keep every colored glow, outline, arrow and cut-away window of Image 1. Keep the framing, the camera angle and every object of Image 1 at exactly the same place. No motion blur, no streaks. Match the rendering of Images 2-3 exactly; do not copy their people. Image 4 is OUR OWN approved frame of this same woman in another scene: her face must look like Image 4 (a round, plain mid-50s face{', but aged 20 years' if s.get('old') else ''}), and the colors must be as clean and bright as Image 4 (saturated bright cyan-blue walls, clean whites, not grayish, not dim); do NOT copy its room, its sink or its pose. {NOTXT}")
            else:
                p5 = (f"Image 1 is our storyboard frame (layout only). Images 2 and 3 are frames of the 3D animation series we must match (their rendering only). {B5CUT} Same objects, same anatomy, same colors, same layout and same background blur as Image 1; keep every colored glow, outline and arrow of Image 1. "
                      f"Keep the framing, the camera angle and every object of Image 1 at exactly the same place. No motion blur, no streaks. Match the rendering of Images 2-3 exactly; do not copy their content. {NOTXT}")
            J(f"{sid}_5", p5, [last] + lr + ([REF["K847"]] if person and sid != "s18" else []), out=start_png, deps=[last])
        # 終わりの絵
        e = s["end"]
        if e[0] == "edit":
            J(f"{sid}_e", edit_prompt(s, e[1], person), [start_png] + look_refs(s, person), out=end_png, deps=[start_png])
        elif e[0] == "crop":
            J(f"{sid}_e", None, [start_png], kind="crop", crop=e[1:], out=end_png, deps=[start_png])
    json.dump(jobs, open(W + "/work/jobs.json", "w"), ensure_ascii=False, indent=1)
    return jobs


def look_refs(s, person):
    if person:
        return [REF["T10"], REF["T19"]]
    if s["scene"].startswith(("cut", "red", "skin")):
        return [REF["D16"], REF["D18"]]
    return [REF["B7"], REF["S2"]]


def edit_prompt(s, change, person):
    if person:
        return (f"Image 1 is the finished frame of our shot (already rendered in the final look). EDIT Image 1 into the frame of the same shot a moment later. Change ONLY: {change}. "
                f"Everything else stays exactly as in Image 1, pixel for pixel where possible: the framing, the camera angle and position, the place, the lighting, the colors, the depth of field and background blur, every object (same place, same shape, same size), her face identity, her clothes, her hair and the render style (a real-time game-engine frame, Unreal Engine 4 era, exactly like Image 1). "
                f"Images 2 and 3 are frames of the 3D animation series we match: for the character look and for how the face changes as one stiff shape only; do not copy their people. All hands stay connected to her own arms; exactly five fingers per hand; no new hand. No motion blur, no streaks. {NOTXT}")
    return (f"Image 1 is the finished frame of our shot (already rendered in the final look). EDIT Image 1 into the frame of the same shot a moment later. Change ONLY: {change}. "
            f"Everything else stays exactly as in Image 1: the framing, the camera, the layout, every other part and object, the colors, the background, the depth of field and the render style (a real-time game-engine frame, Unreal Engine 4 era, exactly like Image 1). "
            f"Images 2 and 3 are frames of the series for the rendering only. No motion blur, no streaks. {NOTXT}")


def crop(src, dst, s, cx, cy):
    subprocess.run([PY, W + "/tools/crop.py", src, dst, str(s), str(cx), str(cy)], check=True, capture_output=True)


def attempts():
    f = G + "/gen.log"
    return sum(1 for l in open(f)) if os.path.exists(f) else 0


def run(names=None, redo_extra=None):
    jobs = build()
    want = set(jobs)
    if names:
        want = set(); stack = list(names)
        byout = {j["out"]: n for n, j in jobs.items()}
        while stack:
            n = stack.pop(); want.add(n)
            for d in jobs[n].get("deps", []):
                if d in byout and byout[d] not in want and not os.path.exists(d): stack.append(byout[d])
    running = {}; failed = {}
    while True:
        # 終わった物
        for n, (pr, t0) in list(running.items()):
            if pr.poll() is not None:
                del running[n]; j = jobs[n]; tmp = f"{G}/{n}.png"
                if os.path.exists(tmp):
                    if os.path.abspath(tmp) != os.path.abspath(j["out"]): shutil.copy(tmp, j["out"])
                else:
                    failed[n] = failed.get(n, 0) + 1
        pending = [n for n in jobs if n in want and not os.path.exists(jobs[n]["out"]) and n not in running and failed.get(n, 0) < 2]
        ready = [n for n in pending if all(os.path.exists(d) for d in jobs[n].get("deps", []))]
        for n in ready:
            j = jobs[n]
            if j["kind"] == "copy":
                shutil.copy(j["refs"][0], j["out"]); continue
            if j["kind"] == "crop":
                crop(j["refs"][0], j["out"], *j["crop"]); continue
        ready = [n for n in ready if jobs[n]["kind"] == "gen"]
        while ready and len(running) < 3:
            if attempts() + len(running) >= LIMIT:
                print("絵の上限", LIMIT); ready = []; break
            n = ready.pop(0); j = jobs[n]
            pr = subprocess.Popen(["zsh", W + "/tools/gen.sh", G, n, f"{P}/{n}.txt"] + j["refs"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            running[n] = (pr, time.time())
        if not running and not [n for n in jobs if n in want and not os.path.exists(jobs[n]["out"]) and failed.get(n, 0) < 2 and all(os.path.exists(d) for d in jobs[n].get("deps", []))]:
            break
        time.sleep(5)
    left = [n for n in jobs if n in want and not os.path.exists(jobs[n]["out"])]
    print("できていない:", left, "失敗:", failed, "Codex を打った数:", attempts())


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "plan":
        js = build(); print(len(js), "仕事", sum(1 for j in js.values() if j["kind"] == "gen"), "枚を Codex で")
    elif cmd == "run":
        run(sys.argv[2:] or None)
    elif cmd == "redo":
        js = build(); n = sys.argv[2]; j = js[n]
        for f in [j["out"], f"{G}/{n}.png"]:
            if os.path.exists(f): os.remove(f)
        if len(sys.argv) > 3:
            open(f"{P}/{n}.extra.txt", "a").write(" " + sys.argv[3])
            js = build(); j = js[n]
        pr = subprocess.run(["zsh", W + "/tools/gen.sh", G, n, f"{P}/{n}.txt"] + j["refs"])
        if os.path.exists(f"{G}/{n}.png") and os.path.abspath(f"{G}/{n}.png") != os.path.abspath(j["out"]): shutil.copy(f"{G}/{n}.png", j["out"])
        print(n, "できた" if os.path.exists(j["out"]) else "無い")
