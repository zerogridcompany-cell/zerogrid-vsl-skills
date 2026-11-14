"""札（時計・数字）と、場面の出来事の効果音を、声の言葉の時刻から置く → badges.json・work/sfx_extra.json
指す輪（fx.json）は、組んだ後のコマで測ってから手で書く（16章）。"""
import json, os
W = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(W)
TL = json.load(open("work/timeline.json")); SH = {s["id"]: s for s in TL["shots"]}
CH = json.load(open("声/timing.json"))["chunks"]


def word(n, w):
    """n 文目の、w を含む句の始めの時刻"""
    for c in CH:
        if c["n"] == n and w in c["text"]: return c["t0"]
    raise KeyError((n, w))


def end(n, w):
    for c in CH:
        if c["n"] == n and w in c["text"]: return c["t1"]
    raise KeyError((n, w))


B = []
def bd(t0, t1, text, x=0.5, y=0.16, size=64, **k): B.append(dict(t0=round(t0, 3), t1=round(t1, 3), text=text, x=x, y=y, size=size, **k))

s = SH["s01"]; t7 = word(1, "朝7時")
bd(s["t0"] + 0.25, t7 - 0.05, "18:00"); bd(t7 - 0.05, t7 + 1.3, "7:00"); bd(t7 + 1.3, s["t1"] - 0.1, "18:00")
bd(SH["s02"]["t0"] + 0.25, word(2, "スーパー") + 0.4, "18:00", size=54)
bd(SH["s12a"]["t0"] + 0.1, SH["s12a"]["t1"] - 0.05, "7:00"); bd(SH["s12b"]["t0"] + 0.1, SH["s12b"]["t1"] - 0.05, "10:00"); bd(SH["s12c"]["t0"] + 0.1, SH["s12c"]["t1"] - 0.05, "15:00")
bd(word(13, "夕方6時"), SH["s13"]["t1"] - 0.1, "18:00")
bd(SH["s17"]["t0"] + 0.3, end(17, "とったせい") + 0.25, "50", y=0.12, size=80, pop_out=True)
s = SH["s22"]
for i, (tx, x) in enumerate([("7:00", 0.2), ("10:00", 0.4), ("15:00", 0.6)]):
    bd(s["t0"] + 0.2 + i * 0.12, s["t1"] - 0.1, tx, x=x, y=0.09, size=44, gray=True)
bd(s["t0"] + 0.56, s["t1"] - 0.1, "18:00", x=0.82, y=0.09, size=50)
s = SH["s23"]; d = (s["t1"] - s["t0"] - 0.4) / 4
for i, tx in enumerate(["7:00", "10:00", "15:00", "18:00"]):
    bd(s["t0"] + 0.2 + i * d, s["t0"] + 0.2 + (i + 1) * d if i < 3 else s["t1"] - 0.1, tx)
bd(word(40, "最初の30秒") + 0.1, SH["s40"]["t1"] - 0.1, "30", y=0.14, size=80)
bd(word(41, "5分ほどで"), SH["s41"]["t1"] - 0.1, "5", y=0.14, size=80)
bd(word(42, "寝る前の10分"), SH["s42"]["t1"] - 0.1, "10", y=0.14, size=80)
s = SH["s46"]; bd(s["t0"] + 0.2, s["t0"] + 1.5, "7:00"); bd(s["t0"] + 1.5, s["t1"] - 0.1, "18:00")
bd(SH["s48"]["t0"] + 0.5, SH["s48"]["t1"] - 0.15, "？", y=0.3, size=150, plain=True)
bd(SH["s49"]["t0"] + 0.2, SH["s49"]["t1"] - 0.1, "18:00")
json.dump(B, open("badges.json", "w"), ensure_ascii=False, indent=0)

PI = "S/04-ポン・クリック・表示/画面のピッ5（とても短い）.wav"
X = []
for b in B:
    X.append([PI, b["t0"], 22, None, f"札「{b['text']}」が出る"])
# フック：上がる音の終わり＝「腰に激痛が走り」の頭 → ピキッ・ドン
hit = word(3, "腰に激痛") + (end(3, "腰に激痛") - word(3, "腰に激痛")) * 5 / 12  # 「腰に」の頭（句の中の字の割合で）
X += [["Z/riserRumble.wav", hit - 0.05, 20, None, "フックの上がる音（終わり＝激痛の頭）"],
      ["Z/painSting.wav", hit + 0.02, 15, 0.7, "ピキッ（激痛）"],
      ["S/02-低いドン・着地/映画風のドン（うつろ）.wav", hit + 0.02, 13, 0.8, "激痛の着地のドン"]]
X += [["S/02-低いドン・着地/映画風のドン（基本）.wav", SH["s05a"]["t0"] + 0.05, 6, 1.2, "話の切れ目（問題→原因）「実はね」"],
      ["Z/painSting.wav", SH["s09"]["t0"] + 0.9, 16, 0.6, "ピキッ（酸欠の筋肉）"],
      ["Z/bagRustle.wav", SH["s16"]["t0"] + 1.6, 16, 0.6, "袋が床に着く"],
      ["Z/painSting.wav", SH["s16"]["t0"] + 1.65, 17, 0.6, "ピキッ（置く瞬間）"],
      ["Z/pop.wav", end(17, "とったせい") + 0.25, 18, None, "「50」がはじける"],
      ["S/02-低いドン・着地/映画風のドン（基本）.wav", SH["s36"]["t0"] + 0.05, 7, 1.2, "話の切れ目（原因→商品）"],
      ["Z/spikePricks.wav", word(40, "最初の30秒") + 0.2, 18, 0.8, "チクチク"]]
json.dump(X, open("work/sfx_extra.json", "w"), ensure_ascii=False, indent=0)
print(len(B), "札", len(X), "音")
