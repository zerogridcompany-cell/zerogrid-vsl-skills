# ZackDFilms 版の映像の作り方 — 第1版（2026-10-08 運営者 確定「原稿以外の ZackDFilms のシステムは完成でいい」）

**ZackDFilms の人物の質感と、作る順は18章が先。** **先に 15章を読む（2026-10-10。作る順・物のバグを出さない・カメラ。ほかの全部の章より先）。** 作る時は、15-0 の順のとおりに進め、そこから指された章だけを開く。読む順：15章 → 14章（絵の質感・終わりの絵の作り方・動画の指示の形）→ 12章 → 13章（話し手が2人以上の時）→ 9章（コマ割りの表）→ 6・7・8章（エフェクト・カメラ・効果音の文）→ 11-4・11-5（音・声）。3章の絵柄の見本 `style_確定_2-2.png` は、もう渡さない。

**どの商品にも使う。** ここには商品の中身を書かない。何を写すかは原稿から決める。原稿の作り方は別（[v1-zackdfilms-script.md](ec-ad-ops/references/_archive/台本の作り方_20261008/2_ZackDFilms版の原稿の書き方/v1-zackdfilms-script.md)。2026-10-08 にハーネスの外へ出した。このファイルは、できた台本を受け取ってからの作り方）。
見本：`zackdfilms/見本_15秒.mp4`（この手順で作った15秒。絵柄だけは確定前の物）。絵柄の見本：`zackdfilms/style_確定_2-2.png`（**運営者 が選んだ絵柄**）。実物のコマ：`zackdfilms/実物のコマ_*.png`。組み立ての見本：`zackdfilms/build_見本.py`。
調べた物：`（作業フォルダ：アプリには同梱していない見本）`（実物9本を1秒4コマで見た表と数）。

## 1. 実物を測った結果（決まりの元）
| 見る所 | 実物 |
|---|---|
| つなぎ | 122回のうち、切るのは10回（8%）。カメラが流れて、寄った先が次の場面になる |
| 場面の長さ | 平均2.3秒。止まっているコマは2%弱 |
| カメラの高さ | 目の高さ46%・低い位置24%・真上24%。正面の左右対称はほぼ無い |
| 人物 | ゲームの3D。ふつうの頭身、服に1色強い色 |
| 中を見せる絵 | 1回2〜4.5秒。明るい地に主役1つ。話している物だけ色か光を変える |
| 光・印 | 話している物が0.5〜1.5秒光る（赤＝痛い・危ない／黄＝ここを見て／緑＝これの事・うまくいく／水色＝りんかく・冷たい）。立体の矢印・輪・印が場面の中にある。**説明の文字は0** |
| 字幕 | 白の太字に黒いふち。字の高さは画面の幅の約6%。上から78%。1〜4語ずつ |
| 音 | 曲は切れずに小さく鳴る。効果音は10秒に3〜6個 |

## 2. 道具
絵：**Codex の画像生成だけ**（Higgsfield で絵を作らない）。動画：Higgsfield の `kling_o3_flf`（始めの絵と終わりの絵を渡す）。声：ElevenLabs `eleven_v4`。組み立て：ffmpeg と Pillow（`zackdfilms/build_見本.py`）。

## 3. 絵柄（確定）
**14章が先**（見本の絵・STYLE BASE・ピント・人物の文は、14-4 と 14-5 を使う。この章の STYLE BASE と `style_確定_2-2.png` は、もう渡さない。下の「書いてはいけない言葉」「写したくない所」「絵の大きさ」は、そのまま）。
全部の絵に、見本として `zackdfilms/style_確定_2-2.png` と `zackdfilms/実物のコマ_人物.png` を渡し、次を書く。
```
STYLE BASE: the first attached image is the target rendering style: a low-detail real-time 3D render like a 2016 video game cutscene or The Sims: simple character model with smooth uniform skin and almost no skin detail, hair as a few large solid chunks, clothes with flat color and only large folds, room made of simple models with flat surfaces. Slightly muted color grading, a little gray in the shadows, neutral daylight (not bright candy colors). Realistic adult body proportions. Everything in sharp focus. Clearly computer animation: not a photograph, not a cartoon, not Pixar. The second attached image is a frame of the reference series, for style only: do not copy its content or its caption words. No text, no letters, no captions, no logos. Vertical 9:16.
```
- 書いてはいけない言葉（別の絵柄になった）：`smooth simplified skin`＋`cute`・`stylized`・`soft light`・`pastel`・`dark moody`・`photorealistic`・`pores`・`film grain`。
- 人物：服に1色、強い色。場所：ふつうの場所（部屋・外）。物を8〜10個、名前で書く。
- 写したくない所は `Nothing below [the waistband] appears in the frame` と書く。それでも写ったら、上を切り出して 1080×1920 に伸ばす。
- 絵は 941×1672 で出る。組み立ての時に 1080×1920 に合わせる。

## 4. 手順
### ① 声と場面割り
1. 声を先に録り、句ごとの時刻を取る。できた声を書き起こして、原稿と照合する。
2. **1場面＝声の1〜2句＝2.5〜4秒**に割る。場面ごとに「始めの絵・終わりの絵・カメラの動き・光や印」を表にする。
3. 外の絵 → 中の絵へは、切らずにつなぐ（前の場面の終わりの絵＝次の場面の始めの絵）。中 → 外へ戻る所は、切ってよい。

### ② 絵
**14章が先**（カメラが動くクリップの終わりの絵は、始めの絵から下絵で作る＝14-2・14-6。1〜3 と 7 は 14-18 の表。4・5・6・8・9 は、そのまま）。
1. **人物と場所の基準の絵を1枚**作る。
2. **同じ向きの絵は、基準の絵を元にして「ここだけ変える」で作る**：`EDIT the first attached image. Keep the camera, framing, body, clothes, background, lighting and [貼った物・置いた物] at exactly the same position, size and angle. Change ONLY: …`。別々に作ると、物の位置・服・窓の大きさがずれる。
3. **外から写す向きは、1本の中で変えない。** 向きを変える絵には、位置が問題になる物（貼った物など）を写さない。
4. **手に取る物は、最初の絵から手に持たせておく。** 途中の絵で急に出すと、動画で「手から湧いて出る」（2026-10-08 運営者）。
5. **光・矢印・印は、絵の中に立体で入れる**（1章の色の意味で）。影と奥行きを付ける。文字は入れない。
6. **変化は「前」と「後」の2枚で見せる。** 後の絵は、色だけでなく形も変える（細くなる・こぶになる・しぼむ）。色だけだと伝わらない。
7. 中を見せる絵は、明るい地に主役1つ。話していない物（骨など）は「描かない」と名前で書く。窓は画面の幅の3〜4割。
8. 体の中の絵が安全判定で断られたら、言いかえる：`medical education 3D diagram`・`clean like a plastic classroom anatomy model`・`transparent viewing window`。「切る・しぼる・むき出し・肌の大写し」を書かない。
9. 全部の絵を横に並べて見る：人物・服・物の位置・絵柄がそろっているか。

### ③ 動画
**14章が先**（始めと終わりの絵の決まり・毎回付ける文・秒数は、14-10 と 14-18 の表。コマンドと、速さ 0.95〜1.15倍は、そのまま）。
- 作る秒数は、場面の長さに一番近い3秒か4秒。**速さは 0.95〜1.15倍まで**（それより速めると早送りに見える）。
- 始めの絵と終わりの絵は、大きさか高さが違う2枚にする（同じ大きさ同士だと止まって見える）。変化だけを見せる場面は、同じ構図でよい。
- 指示は「起きる順」に書く：まず何が動く → 次に何が出る → 最後にどう変わる。
- **光や印は「動かす」と書く**：輪が外へ3回広がる／印がゆれて点滅する／ふちが点滅する／矢印が出てきて押しこむ・2回はずむ／光がまたたく。
- 毎回付ける文：
```
Natural real-time speed. No cuts, no scene change. Same 3D render style, same lighting, same clothes, same objects from first frame to last. [貼った物] never moves. The camera never stops. No text, no captions, no subtitles, no logos.
```
- コマンド：`higgsfield generate create kling_o3_flf --prompt "…" --start-image a.png --end-image b.png --aspect_ratio 9:16 --duration 3 --mode pro --sound off --multi_shots false --wait --wait-timeout 15m --wait-interval 10s`（`--multi_shots false` が無いと失敗する。3秒で約3.8、4秒で約5クレジット）。
- できたら1秒3コマで並べて見る：物の位置／手や服の崩れ／写したくない所が大きく写っていないか／変化が、声の言葉の時刻に来ているか。だめなカットだけ作り直す。

### ④ 字幕
白の太字（ヒラギノ角ゴ W7）・1080幅で68px・黒いふち5px・上から77%。声の句ごとに差し替え。句読点は出さない。

### ⑤ 音
- **効果音は、できた動画のコマを見て、出来事の時刻に置く**（物が当たる・開く・色が変わる・中へ入る・印が出る）。原稿の時刻から置かない。10秒に3〜6個。変化の山には、上がる音 → 当たる音を重ねる。
- 曲は切らずに敷く。**声より 10 LU 下**、全体 −14 LUFS。書き出した後に測る。

### ⑥ 検品
1秒2.5コマで全部のコマを見る（崩れ・位置・字幕と絵の時刻）。完成の音を書き起こして原稿と照合。**音を耳で聞いていない時は、そう報告する。**

## 5. 失敗した形（こうしない）
| した事 | どうなった |
|---|---|
| 絵の指示に「なめらかな肌・やわらかい光・水色」と書いた | かわいい3Dイラストになり、実物と別物 |
| 5秒の動画を1.6倍に速めた | 早送りに見えた |
| 3〜5秒の動画を引きのばして遅くした | 同じ絵で止まって見えた（止まったコマ38%） |
| 絵を1枚ずつ別々に作った | 貼った物の位置が、向きが変わるたびに動いた |
| 体の中を40秒続けた・暗い背景にした | 実物と違う。中は短く、明るく、主役1つ |
| 色だけ変えて「弱った」を見せた | 伝わらなかった。形も変える |
| 効果音を原稿の時刻で置いた | 動きとずれた |
| 光や矢印を「無い」と決めつけた | 実物は入れている。文字だけが無い |

---

# 分析2で足した章（2026-10-08。実物4本を1秒6コマで見て、エフェクト44個・カメラ77場面・効果音82個を測った）

調べた物：`（作業フォルダ：アプリには同梱していない見本）`（`A_コマ割り_*.md` 4つ・`B_効果音.md`・`C_エフェクトの図鑑.md`・`D_カメラ.md`・`E_生成の指示の部品.md`・見たコマ `sheets/`）。
**確かめていない事：6〜8章の英語の文で、絵も動画もまだ作っていない**（分析だけ。画像生成と Higgsfield は使っていない）。秒数・回数・大きさは実物を測った数。最初に使う時は、1種類ずつ試してから本番に入れる。効果音の手持ちの音は、耳で聞かずに名前と長さで当てた。

## 6. エフェクト
**14章が先**：人や体の一部・物をまるごと透かす時は、⑪a と「⑪入る」ではなく 14-13 を使う。ほかは、この章のまま。
**1章の「緑＝これの事・うまくいく」と、4章③の「輪が外へ3回広がる／ゆれて点滅する／ふちが点滅する／2回はずむ／光がまたたく」は、この章が先。** 4章②7の「窓」は、わくを付けない形（下の⑪）が先。

### 実物の決まり（44個）
| 見る所 | 実物 |
|---|---|
| 点滅 | **0個。** 全部「出る → そのまま → 消える」の1回きり |
| 出る速さ | 光は0.07〜0.17秒でくっきり。立体の印は小さく出て0.15〜0.3秒で大きくなる。矢印は0.3〜0.6秒かけて向きへ伸びる |
| 出ている長さ | 部品を1つ光らせる0.2〜0.3秒／物やふちの光0.4〜1.0秒／矢印・重り・時計1.0〜1.8秒 |
| 声との合い方 | その物の名前を言いはじめる**0〜0.2秒前**に出はじめる（21か所の中央の値−0.13秒） |
| カメラとの合い方 | カメラが着いて、ゆっくり流れている時に出す（速い動きの最中に出たのは44個中3個） |
| 数 | 1場面で新しく出すのは1つ。同時に見えるのは3つまで。次は、前が消えはじめてから。エフェクトのある場面は全体の約45%（出来事を語る場面はほぼ0） |
| 置き方 | 場面の中に、奥行き・陰・うつる光を持って置く。画面にはりついた平らな図は0個（電話や計器の画面の中の印だけ平ら） |
| 字 | 説明の字は0個。出たのは数と単位だけ（「2 Times」「lbs」「SEC」） |
| 色 | **指さし＝うすい黄色**（一番多い）／良い向き・足りた・ぶじ＝緑／悪い・足りない・じゃまする力・要る動き＝赤／目あての形・数・電気・流れ＝水色〜白。背景や物の色にうもれる時は色をずらす（水色の中は青白）。悪くなる・良くなる途中は だいだい・黄 を通す |

### どこで出すか
- エフェクトが「出きった形」を、始めの絵か終わりの絵に描く。**出す時**＝始めに無し・終わりに有り。**消す時**＝始めに有り・終わりに無し。**出して消す**（0.4〜1秒の指さしの光）＝両方に無しで、動画の指示だけで出す（外れたら「出す」のクリップにして、消えるのは次のクリップの頭に回す）。
- 編集で後から足すのは、効果音と字幕だけ。（15-5 の 9 で、光・輪・線を編集で重ねる道も使う。その時は 16章）

### 絵の指示に足す文
エフェクトのある絵に、必ず付ける：
```
EFFECT (part of the 3D scene, not an overlay). The effect described below is a real object or real light inside the scene: it has volume, shading and perspective, anything in front of it partly hides it, and it throws a soft colored light onto nearby surfaces. It is NOT a flat sticker, NOT a 2D graphic, NOT a user-interface element. Exactly one effect in this image; everything else looks normal.
```
字のある印（⑥⑦）の時だけ、後ろに `The only characters in the image are "[字]".` を足す。エフェクトは主役のすぐ上か横の空いた所に置き、字幕の帯（上から72〜82%）にかけない。主役は幅の25〜45%にして空きを残す。

| 番 | 種類（何を伝えるか） | 絵の指示に足す文 |
|---|---|---|
| ① | 物が光る（今これの話） | `[THING] itself is lit up: its whole surface has turned pale warm yellow, as if lit from inside, with a soft yellow halo about one-fifth of its width around it. Its shape, edges and shading stay fully visible; nothing else in the image is yellow.` |
| ② | 流れる光の帯（ここからここへ伝わる・この全体） | `A soft pale-yellow band of light wraps around [THING] at [where]. The band is about 15% of the length of [THING], follows the curve of its surface, and has blurred front and back edges. The rest of [THING] keeps its normal color.` |
| ③ | ふちの光（大きい物の一部・道すじ・体の部分） | `The outline of [PART] glows: a thin bright yellow line, about 1% of the frame width, runs along its edge with a faint yellow halo outside the line. The line follows the 3D shape and is hidden wherever the shape turns away from the camera. The inside of [PART] keeps its normal color.` |
| ④ | 小さな輪（ふれた点） | `Exactly where [A] touches [B], a small bright yellow ring lies flat on the surface of [B]: thick line, about 3% of the frame width, seen in perspective as an ellipse.` |
| ⑤a | 立体の矢印（力の向き。緑＝助ける・赤＝じゃまする） | `One solid 3D arrow floats just [above/below/beside] [THING], pointing [straight up]. It is glossy [green], thick like molded plastic, with a light side, a dark side and a soft shadow on [surface]. It is about 15% of the frame width and does not touch [THING].` |
| ⑤b | 曲がった矢印（要る動き） | `One solid 3D curved arrow, glossy red, thick like molded plastic, bends in an arc over [THING] from [A side] to [B side], showing the direction [THING] has to turn. It is about 20% of the frame width and does not touch [THING].` |
| ⑥a | 重り（重さ） | `A solid 3D weight, toy-like: a [blue] trapezoid block with a ring handle on top, glossy, with shading and a contact shadow, rests on top of [THING] and presses it down slightly. About 20% of the frame width. The only characters in the image are "[unit]" in white on its front.` |
| ⑥b | 電池（たまり具合） | `A solid 3D battery icon floats beside [SUBJECT] at [head] height: a black body with a glowing [red] rim and [1] of 5 [red] bars lit inside. About [20]% of the frame height. It is an object in the room: it has thickness and a soft glow on the wall behind it.` |
| ⑥c | 丸い時計（時間） | `A round timer dial floats just above [THING]: a white and light-blue ring, [one-third] filled clockwise, with white digital digits "[18]" and the small word "SEC" inside. About 15% of the frame width, slightly glowing. These are the only characters in the image.` |
| ⑥d | 比べる物（大きさ・重さ） | `Right next to [THING], at the same size and on the same floor, sits a real [familiar object of the same size or weight], in one saturated color, with its own contact shadow.` |
| ⑦ | 数える立体の字（何倍・何秒） | `Floating in the air in front of [THING], at 30% from the top of the frame: the glowing 3D text "[2 Times]" in light cyan with a soft cyan halo, bold rounded sans-serif, about 40% of the frame width. This is the only text in the image.` |
| ⑧ | 透ける体（目あての形・動く先） | `A see-through light-cyan copy of [THING] overlaps the real one, turned to [the target position]. Only its outline glows bright cyan-white; its inside is almost fully transparent, so the real [THING] stays clearly visible through it.` |
| ⑨a | 電気 | `A jagged bolt of electricity, bright cyan-white, about [3]% of the frame width thick, arcs from [A] over [B] to [C]. It glows, and it lights the floor and nearby surfaces cyan.` |
| ⑨b | 流れの線（流れ・ていこう） | `Three or four glowing white-cyan wavy lines, each about 1% of the frame width thick, run horizontally past [THING] at different heights, showing [the flow / the resistance] around it.` |
| ⑩ | 画面の中の印（結果を物が答える） | `The screen of [DEVICE] shows one simple flat icon and nothing else: [a red empty battery outline with a red question mark / a green full battery / a gauge needle resting at the far-left mark]. The icon sits on the glass, tilted in perspective with the device, with a faint reflection.` |
| ⑪a | 中を見せる：表面が透ける | `Around [SPOT], the outer surface of [THING] has become see-through and fades out softly at its border (no cut edge, no frame, no window rim), so the inside is visible. The outer shape of [THING] is unchanged. INSIDE show ONLY: (1) [hero part], [its color]; (2) [second part], [color]; (3) [third part], [color]. Clean like a plastic classroom teaching model; nothing is injured.` |
| ⑪b | 中を見せる：開いた模型 | `[THING] is shown as a clean cutaway teaching model: its near side is open along one smooth curve, and the open edge has a thin pale-pink bright line. Behind it the background is a plain flat sky-blue. INSIDE show ONLY: (1) [hero part] in its own real colors; everything else inside is one plain [pink]. Nothing is injured.` |
| ⑪c | 中を見せる：さやが下がる | `The dark outer sleeve of [THING] has slid down to its bottom third, exposing the inside of the upper two-thirds: [center part, color] in the middle, [side parts, color] on both sides. The sleeve's top edge is a clean ring.` |
| ⑪d | 面で上下に割る | `Split-level side view: the [surface line] runs straight across the frame at 37% from the top. Above the line: [what is above]. Below the line, seen through clear [water/glass/ground]: [what is below]. Camera exactly side-on at the height of the line. Plain background above the line.` |

矢印だけは「1つの考え」なら3本まで：`Three arrows in total: one green pointing up above [X], two red pointing down below [Y] and [Z].`

### 動画の指示に足す文
エフェクトのあるクリップに、必ず付ける：
```
The effect happens once. It does not blink, pulse, flicker, bounce or repeat. It stays attached to [THING] in 3D as the camera moves. The camera is already settled into a slow drift before the effect begins.
```
［秒］はクリップの頭からの秒。

| 番 | 種類 | 動画の指示に足す文 |
|---|---|---|
| ① | 物が光る | `At about [0.4] s [THING] lights up pale yellow from inside, reaching full brightness within 0.15 s; it stays steadily lit for about [0.7] s, then returns to its normal color within 0.15 s.` |
| ①' | 部品を順に光らせる | `[PART 1] lights up for 0.25 s at about [1.0] s, then [PART 2] for 0.25 s at about [1.6] s, then [PART 3] for 0.25 s at about [2.2] s; only one part is lit at any moment, each lights once.` |
| ①'' | 色が変わったまま（悪くなった） | `Starting at about [0.6] s, [PART] changes color from [pink] through orange to [red] over about 0.6 s and stays [red] to the end.` |
| ② | 流れる光の帯 | `At about [0.4] s a soft pale-yellow band of light appears at [A] and glides once along [THING] to [B] in about 0.6 s, then it is gone. One pass, one direction, no return.` |
| ③ | ふちの光（順に2か所） | `At about [0.4] s the outline of [PART 1] lights up as a thin yellow glowing line, fully bright within 0.1 s, and holds steady for 0.4 s; it goes out at the same moment the outline of [PART 2] lights up, which holds 0.4 s and goes out.` |
| ③' | ふちの光が伸びる | `At about [0.5] s a yellow glow starts at [A] and grows along [the branch] to [B] in 0.2 s, holds steady for 0.3 s, then dims.` |
| ④ | 小さな輪 | `At the moment [A] touches [B], a yellow dot appears at the contact point, expands once into a small ring within 0.2 s, holds 0.2 s and fades out. One expansion only.` |
| ⑤ | 立体の矢印 | `At about [0.5] s the arrow appears small, as just its tip, and stretches in the direction it points over 0.5 s to its full length; it holds 0.2 s, then shrinks back and vanishes within 0.2 s.` |
| ⑥a | 重りが落ちる | `At about [0.5] s the weight drops in from above the frame, tumbling half a turn, and lands on [THING] 0.5 s later; on landing it squashes very slightly and [THING] sinks a little under it; then it stays still.` |
| ⑥b | 電池が出て色が変わる | `At about [0.5] s the battery icon pops in small beside [SUBJECT] and scales up to full size within 0.3 s; it then stays beside [SUBJECT] while its rim shifts from red through orange and yellow to green and its bars fill one by one.` |
| ⑥c | 時計が数える | `The timer dial appears instantly at about [0.4] s; its digits count up quickly and its ring fills clockwise for about 1.4 s; then it vanishes.` |
| ⑦ | 数える字 | `The glowing text appears small and scales up to full size within 0.15 s; only its number changes, counting up from [2] to [7] over about 1.2 s while [THING] grows [wider] in step; then the text shrinks and vanishes.` |
| ⑧ | 透ける体 | `At about [0.4] s a see-through cyan outline copy of [THING] fades in within 0.1 s, turned toward [the target position], and stays visible to the end, moving together with the real [THING].` |
| ⑨a | 電気 | `At about [0.3] s the bolt grows from [A] over [B] to [C] in 0.4 s, then keeps flickering to the end, changing its jagged shape on every frame; its glow on the floor flickers with it.` |
| ⑨b | 流れの線 | `The wavy lines drift steadily from [left to right] the whole time, like current; they never stop and never change color.` |
| ⑨c | 流れが止まる | `The stream of [air/water] flows past [THING] and gets thinner from about [0.5] s until it stops completely at about [1.5] s.` |
| ⑩ | 画面の中の印 | `At about [0.5] s the icon appears on the screen within 0.1 s; then [its bars fill from the bottom one by one / the needle swings from the far-left mark to the far-right mark in 0.2 s and stays there / the screen changes from green to red in one step and stays red].` |
| ⑪入る | 表面が透ける／開く／下がる | `During the last 0.2 s of the fast camera move, the outer surface around [SPOT] becomes see-through and fades away, revealing the inside; the outer shape stays.` ／ `…the near side of [THING] opens along one smooth curve, revealing the inside, and the background becomes plain sky-blue.` ／ `…the outer sleeve of [THING] slides down in 0.2 s, exposing the inside.` |
| ⑪出る | 表面がもどる | `In the first 0.2 s the outer surface fades back in and covers the inside again while the camera pulls away.` |

- **書かない言い方**：`blinks` `pulses` `flashes three times` `bounces twice` `ripples outward repeatedly`、電気（⑨a）以外の `flickers`。
- 字や数字が動く物（⑥c・⑦）がくずれたら、数を物で見せる形に変える（⑩の針・⑥bの電池の棒・⑥dの比べる物）。

## 7. カメラ
**14章が先**：動画の指示は 14-10 の形で書く。「速い動きは、クリップの頭の0.3秒に置く」は、14-10 の「クリップの長さの3割までに着く」が先。カメラの種類の表・山の形・型は、この章のまま。
**1章の「場面の長さ 平均2.3秒」と、4章①2の「1場面＝声の1〜2句＝2.5〜4秒」は、この章が先**（1秒6コマで見ると、カメラの動き1つは平均1.5秒。1クリップ3秒の中に山を2つ入れる）。4章③の毎回付ける文は、そのまま使う。

### 実物の決まり（77場面）
| 見る所 | 実物 |
|---|---|
| 動き1つの長さ | 平均1.5秒（説明の回1.3秒・出来事の回2.0秒）。切るつなぎは73か所中4か所（5%） |
| 動きの種類 | 寄る27%・引く18%・回りこむ16%・下がる10%・止まり気味10%・追う8%・上がる6%・中へ入る4%。同じ種類を3回続けない（寄ったら次は引くか回る） |
| 速い動き | 場面の36%にある。**0.17〜0.5秒（中央の値0.25秒）**。1コマ目から速く、ぼける。着く時に2〜3コマで遅くなり、**そのまま同じ向きへゆっくり流れ続ける** |
| 止まり | 0.2秒以上まったく止まった所は、4本で5か所・合計1.2秒（全体の1%） |
| 寄る大きさ | ゆっくり：1.2〜2倍を1.5〜2.5秒で。速く：3.5〜6倍を0.25〜0.5秒で。速く引く：4〜13倍 |
| どこまで寄るか | 名前を言う物は**幅の25〜45%で止める**（まわりにエフェクトの空き）。結果の画面と顔だけ、画面いっぱい（顔は幅70〜80%） |
| 始まり | 4本とも、1コマ目は寄りの絵で、もう動いている |
| ゆれ | 物が当たった瞬間だけ（77場面中3場面）。1回ゆれて0.2秒で落ち着く |
| 言葉との合い方 | 速い動きは、言葉の切れ目とつなぎの語の上で済ませる。**強い語の0〜0.36秒前（中央の値0.18秒）に着く**（12か所中11か所）。強い語の間は、ゆっくり寄るか止まり気味で、そこでエフェクトが出る |
| 終わり | 最後の2〜3秒（結果を言う所）は、ゆっくり寄るか、ゆっくり引くだけ |

### 動画の指示に入れる文
全部のクリップ：
```
CAMERA: [下の1文]. The camera is already moving on the first frame. It never comes to a full stop: after the main move it eases out and keeps drifting slowly in the same direction until the last frame.
```
この後ろに、4章③の毎回付ける文を続ける。**速い動きは、クリップの頭の0.3秒に置く**（途中や終わりに置かない）。大きさは画面に対する割合で書く。

| 種類 | 動画の指示に入れる文 |
|---|---|
| ゆっくり寄る | `One slow continuous push-in at constant speed: [SUBJECT] grows from about [35]% to about [70]% of the frame width over the whole shot.` |
| 速く寄って、流れる | `A fast push-in during the first 0.3 s, with motion blur: from [SUBJECT] at about [60]% of the frame height to [its PART] filling about [75]% of the frame width. The camera then eases out and keeps creeping forward slowly for the rest of the shot.` |
| ゆっくり引く | `One slow continuous pull-back at constant speed: [SUBJECT] shrinks from about [80]% to about [60]% of the frame height, revealing [what appears].` |
| 速く引いて、流れる | `A fast pull-back during the first 0.3 s, with motion blur: from [PART] filling the frame to the whole [SUBJECT] at about [55]% of the frame height. The camera then eases out and keeps pulling back very slowly.` |
| 回りこむ（ゆっくり） | `The camera orbits about [45] degrees to the [left] around [SUBJECT] at [chest] height over the whole shot, constant speed, keeping [SUBJECT] centered at the same size.` |
| 回りこむ（速い） | `During the first 0.25 s the camera swings 90 degrees from the front of [SUBJECT] to its [left] side, with motion blur, then drifts on slowly in the same direction.` |
| 上がる（真上へ） | `Within the first 0.4 s the camera rises and tilts down to a straight top-down view of [SUBJECT] at about [45]% of the frame height, then slowly rotates and rises.` |
| 下がる（面の高さへ） | `Within the first 0.2 s the camera drops from [the top-down view] to [surface/eye] level, exactly side-on to [SUBJECT]; then it holds almost still with a very slow sideways drift.` |
| 追う（物について行く） | `The camera follows [OBJECT] as it moves [direction], keeping it centered and at the same size the whole time.` |
| 追う（線をたどる） | `The camera travels along [the cable/line] from [A] to [B] in about 0.5 s, then settles on [B] at about [30]% of the frame height and keeps drifting slowly.` |
| 中へ入る | `The camera pushes fast straight into [SURFACE]. For two frames the blurred [surface-colored] surface fills the whole frame; then the view is right at/inside it: [what is seen]. The whole entry takes about 0.35 s. Then the camera drifts slowly [sideways just above the surface].` |
| 止まり気味 | `Almost still: only a very slow drift to the [right], about 5% of the frame width over the whole shot.` |
| 当たった時のゆれ（足す） | `At the moment of impact the camera shakes once, slightly, and settles within 0.2 s.` |
| 時間が飛ぶ | `The camera pulls back at a steady speed for the whole shot. [SUBJECT] stays in the same pose at the center while the surroundings are replaced [3] times, each change inside a 0.1 s white flash: first [PLACE 1], then [PLACE 2], then [PLACE 3].` |

### 体や物の中へ入る手順（5回とも同じ形）
1. 前のクリップで、入る物（幅の50〜80%）を外からゆっくり寄っておく（1.5〜2.3秒）。
2. 言葉の切れ目で、速く動く（寄る・振り下ろす・90度回りこむ・下がる）。**0.17〜0.5秒**。
3. 画面をふさぐのは**入る物の表面そのもの**（その色が1〜2コマ）。または、表面が0.13〜0.2秒で透ける・開く・下がる。黒や白で一度消さない。丸い窓は開けない。
4. 中の景色に着く。背景は無地。カメラはゆっくり流れるだけ。
5. 着いて0.2〜0.5秒あとに、最初のエフェクト。中にいるのは1.3〜4.4秒（長くて7秒）。その間、速く動かない。
6. 出る：表面がもどる（0.17秒）＋引く／溶ける（0.3秒）／上へ速く振りぬく。

### 山の形と、型（3秒のクリップ）
```
つなぎの語                … 速いカメラ（0.2〜0.3秒）＋ シューか低いドン
強い語の 0.1〜0.2秒前      … カメラが着いて流れはじめる ＝ エフェクトが出はじめる
強い語の頭                … エフェクトが出きっている ＋ 高いキラかポン
強い語の終わり〜次の語      … エフェクトが消える ／ 次のエフェクトが出る
```
1つの山＝1.3〜2秒。**1クリップ（3秒）＝山2つ**、4秒＝山2〜3つ。

| 型 | 使う時 | 0.0〜0.3秒 | 0.4〜1.5秒（山1） | 1.5〜3.0秒（山2） | 始めの絵／終わりの絵 |
|---|---|---|---|---|---|
| 1 着いて、指さす | 物の名前を言う | 速く寄る | ①か③（0.4秒に出て1.1秒に消える） | 2つ目の名前に①か③。または② | 引きの絵／主役が幅25〜45%の寄りの絵 |
| 2 中へ入る | 中の仕組みを言う | 速い動き。最後の0.2秒で⑪ | 着く。0.8秒に①'の部品1 | 1.6秒に部品2、2.2秒に部品3 | 外の寄りの絵／中の絵 |
| 3 力を見せる | 押す・引く・支える・ていこう | 面の高さへ下がる | 0.4秒に⑤が伸びる→1.3秒に縮む | 1.4秒に③。または⑧→⑤b | 上からの絵／真横の低い絵（⑪d） |
| 4 量を見せる | 重さ・たまり具合・時間・何倍 | 止まり気味 | 0.5秒に⑥が落ちる・出る | 印の中身が変わる。ゆっくり寄る | 印の無い絵／印が着いた絵 |
| 5 物が答える | 結果・くらべた答え | 画面や目盛りへ速く寄る | 0.5秒に⑩が変わる | 変わったまま。ゆっくり寄る | 道具の全体の絵／画面の大写しの絵 |
| 6 大きさ・時間を比べる | とても大きい・とても長い | 速く引く（4〜13倍） | 主役が小さく、比べる物が大きい | 「時間が飛ぶ」＋⑥bが浮いたまま変わる | 主役の寄りの絵／主役が高さ10〜15%の引きの絵 |
| 7 出来事（人物） | 話の始め・終わり | 追う | 当たった時に1回ゆれる | 回りこむか、ゆっくり寄る。エフェクト無し | 上半身の絵／同じ人の別の向きの絵 |
| 8 中から出る | 説明の終わり→結果 | ⑪がもどる＋速く引く | 外の絵。ゆっくり引く | エフェクト無し | 中の絵／外の引きの絵 |

- 説明の所は「型2 → 型1・3・4を1〜3回 → 型8」。
- 溶けるつなぎ（0.3秒）は、時間や場所が飛ぶ所だけ。
- **編集での合わせ方**：できた動画を1秒6コマで並べ、エフェクトが出はじめるコマの秒（E）を読む。声でその物の名前を言いはじめる秒（W）に対して、**E＝W−0.1秒**になるようにクリップを置く。ずれが0.2秒より大きい時は、クリップの頭を切るか、0.95〜1.15倍の中で合わせる。合わなければ作り直す。

## 8. 効果音
**4章⑤の「10秒に3〜6個」と「曲は声より10 LU 下」は、この章が先。**

### 実物の決まり（82個）
| 見る所 | 実物 |
|---|---|
| 数 | 10秒に約7個（説明の所7〜10個・出来事の所5〜6個） |
| 時刻 | **76%は絵の出来事と同時（±0.1秒）**。前17%（速いカメラの0.1〜0.3秒前のシュー／山の前の上がっていく音）。後7% |
| 何に鳴るか | 速いカメラ・切りかわり38%／エフェクト33%／物や体の動き29% |
| 鳴らない所 | 溶けるつなぎ（7か所中6か所で無音）／色がゆっくり変わるだけの所／流れ続ける小さな光／ゆっくり流れるだけのカメラ |
| 高さ | **光には高い音・当たりと着地には低い音・速い動きにはシュー・印が出る時は短いポン** |
| 長さ | 8割が0.3秒以下。長いのは「上がっていく音」と「低いうなり」だけ |
| 大きさ（その時の声との差） | キラ・チッ・シュー＝20〜27dB下／ポン・ふつうの低いドン＝11〜20dB下／強い当たり・カメラが着くドン＝7〜10dB下。**声と同じ大きさの低いドンは1本に1〜2回だけ**（話が大きく切りかわる所のカメラの動き） |
| 曲 | 4本とも頭から終わりまで切れない（0.3秒以上の無音0回）。**曲＋効果音の全体で、声より15.5〜17 LU 下**（曲だけなら声より約19〜25dB下）。全体は −14〜−10 LUFS。終わりの2秒で小さくなる |

### 置き方（できた動画のコマの時刻で置く）
手持ち：`（作業フォルダ：アプリには同梱していない見本）`（説明は同じ場所の `_sounds.json`）。

| 出来事 | 音（高さ・長さ） | いつ | 声より | 手持ちで当てる音 |
|---|---|---|---|---|
| 速いカメラ（寄る・引く・振る・飛ぶ） | シュー（2kHz以上・0.2〜0.5秒） | 動き出しの0.1秒前〜同時 | 20〜25dB下 | `whoosh`。物が飛びこむ時は `cardWhoosh` |
| 速いカメラが着く・切りかわる | 低いドン（30〜200Hz・0.1〜0.3秒） | 着くのと同時 | 10〜20dB下 | `whooshLand`（着地を着く時刻に）か `don` の頭 |
| 話が大きく切りかわる所（1本に1〜2回） | とても大きい低いドン | カメラの動きと同時 | 0〜3dB下 | `boom` |
| 中へ入る | 前ぶれの音→入り切って低いドン | 入る0.2秒前〜入り切り | 14〜16dB下 | `reverseCymbal`（終わりを入り切る時刻に）＋ `don` |
| 物・ふち・帯が光る | 高いキラ（2〜5kHz・0.1〜0.4秒） | 光の出はじめと同時 | 17〜27dB下 | `sparkle` の頭0.4秒。短くは `ding` の頭0.3秒 |
| 小さな輪・ふれた点 | 高いチッ（0.07秒） | 同時 | 27dB下 | `click` |
| 部品を順に光らせる・画面の印が出る・さす | 短いポン（0.1〜0.25秒） | 同時 | 13〜26dB下 | `pop` を1つずつ（`pop3` は間が決まっているので使わない） |
| 立体の矢印が伸びる | 風を切る音（0.3秒） | 出はじめと同時 | 21dB下 | `swipeSoft` の頭0.4秒か `whoosh` |
| 立体の印が落ちてくる | 上がる音→着く時に高いカチ | 落ちはじめの0.3秒前から／着くのと同時 | 17〜24dB下 | `riserSoft`（終わりを着く時刻に）＋ `click` |
| 立体の印がぽんと出る | 低いドン（0.17秒） | 同時 | 11dB下 | `don` の頭0.3秒か `pop` |
| 印が消える | 高いチッ | 同時 | 20dB下 | `click`（小さく） |
| 物や体が当たる・落ちる・たたく | 低いドン（50〜200Hz・0.1〜0.2秒） | 当たるのと同時 | 7〜17dB下 | `don`。一番強い1回だけ `boom` |
| 場所や時間が飛ぶ | シュー（0.2〜0.5秒） | 入れかわる0.1秒前 | 14〜27dB下 | `swipeLight` の頭0.5秒か `whoosh` |
| 山の前（1〜2秒） | 上がっていく音（1.3〜2.3秒） | 終わりが山に来るように | 18〜24dB下 | `riserRumble` か `riserSoft` |
| 物そのものの音（電気・水・切る 等） | 物による | 同時 | 6〜18dB下 | 切る＝`scissors`、水＝`spill`・`drip`。電気のバチバチ・水しぶきは手持ちに無い |
| 溶けるつなぎ／色がゆっくり変わる／ゆっくりのカメラ | — | — | — | **置かない** |

- 同じ音を3回続けない。低いドンが続く所（たたく・当たる）は0.5秒おきまで。
- 書き出した後に測る：声と、曲＋効果音の差が約16 LU。全体 −14 LUFS。**音を耳で聞いていない時は、そう報告する。**
- 波形だけでは言えなかった事：何の音か（太鼓・木・金属・水の区別）／低いドンが効果音か曲の太鼓か／小さく長い音（時計のカチカチ・ピーという音）があるか／響きや左右の広がり。

## 9. コマ割りの表の作り方
絵を1枚も作らないうちに、この表を全部うめる。声を先に録り、語ごとの時刻を取ってから（4章①1）。

### 表の列
`番｜クリップの秒（声の何秒〜何秒）｜声の言葉｜強い語と、その語が始まる秒｜型（7章の1〜8）｜始めの絵｜終わりの絵｜カメラ（7章の種類・主役の大きさ「始め何%→終わり何%」・速い動きは頭の0.3秒）｜エフェクト（6章の番号・何に・何色・クリップの何秒に出て何秒に消える）｜効果音（8章：何を・どの出来事に・声より何dB下）｜次へのつなぎ`

### うめ方
1. 声の語の時刻から、**強い語**（物の名前・数・結果）に印を付ける。つなぎの語と、言葉の切れ目にも印を付ける。
2. **クリップの頭を、つなぎの語か言葉の切れ目に置く**（そこに速いカメラが来る）。1クリップ3秒の中に、強い語が2つ入るように割る（＝山2つ）。強い語が1つしか無い3秒は、型7（出来事）か、ゆっくり寄るだけにする。
3. クリップごとに型を決め、カメラを7章の文から1つ選ぶ。**同じ種類を3回続けない。** 寄りと引きの割合は、寄る3：引く2：回る2：その他3。
4. エフェクトは、**強い語が始まる秒 −0.1秒**に出はじめるように、クリップの何秒かを書く。1クリップに新しく出すのは2つまで（山ごとに1つ）。同じ種類を続けない。
5. 始めの絵・終わりの絵に、エフェクトを描くかどうかを決める（6章「どこで出すか」）。次のクリップの始めの絵＝前のクリップの終わりの絵（4章①3）。
6. 効果音の列は、絵の出来事に対して書く（秒は後で、できた動画のコマから読む）。
7. 表ができたら数える：エフェクトのある場面が全体の半分をこえていないか／中の絵の合計が全体の3割をこえていないか／声と同じ大きさのドンが2回までか／最後の2〜3秒に速い動きが無いか。

### できた動画の見方（6コマ／秒）
- 4章③の「1秒3コマ」ではエフェクトの出はじめが読めない。**1秒6コマで並べ、エフェクトの出る所だけ1秒30コマで見る。**
- 並べる道具：`（作業フォルダ：アプリには同梱していない見本）`（この機械の ffmpeg には字を焼く機能〈drawtext〉が無いので、Pillow でコマに秒を書いて並べる）。
```
ffmpeg -v error -y -i <動画> -vf "fps=6,scale=480:854" -q:v 3 <コマの置き場>/%04d.jpg
python3 道具/sheet.py <コマの置き場> <出す場所> <名前>     # 横6コマ×たて4段＝1枚4秒
```
- 出る瞬間を30コマで見る：`道具/strip.py`（中の `rows` に「動画・始まる秒・名前」を書く）。
- 見る事：エフェクトが出はじめるコマの秒（E）／カメラが着くコマの秒／点滅していないか／エフェクトが物にくっついているか（カメラが動いても位置がずれないか）／字や数字がくずれていないか。

### 実物を新しく調べる時
`映像の分析2/` と同じ手順：①動画を落とす（インスタは `uvx --quiet yt-dlp`）②1秒6コマで並べて全部見る ③声を語ごとの時刻で書き起こす（`whisper --model large-v3-turbo --word_timestamps True --output_format json`）④声と曲＋効果音を分ける（demucs）⑤`道具/sfx.py` で音の立ち上がりを出し、コマと照らす ⑥A〜D の形の表にする。

## 10. 絵コンテを先に作って見せる（この順でやる）
**14章が先**：2 の「1枚目を見本に渡して作る」は、場所の見本を先に作り、14-4 の表で渡す形に替える。絵コンテの絵は、14-5 の質感の文で描き、通った絵は、そのまま「始めの絵」に使う。
動画にする前に、**10場面ぶんの絵**を作って1枚に並べ、運営者 に見せる（見本：`zackdfilms/見本_絵コンテ10場面.jpg`）。動画は絵が通ってから。
1. 原稿を10前後の場面に割る：書き出し2〜3枚／なぜ要るか（たとえ・中の絵）2〜3枚／昔1枚／今1枚／商品1枚／最後の絵1枚。
2. 1枚目で人物と場所を決める（3章の絵柄の指示＋`zackdfilms/style_確定_2-2.png`）。2枚目からは、1枚目を見本に渡して、同じ人・同じ部屋で作る。
3. 1枚に、エフェクトは1つ（6章の書き方）。体や物の中は、わくの無い「透ける」で見せる。
4. 場面ごとに「声の言葉・絵・エフェクト」の表を付けて見せる。
5. 絵が通ったら、声を録り、句の時刻で場面の長さを決め、足りない絵（つなぎ・前と後）を足して動画にする。**最初の10秒を先に組んで見せ**、その間に残りを作る。

## 11. 1本目を通して作って分かった事（2026-10-08 運営者。**ここは、上の章より先。ただし 14章が、この章より先**。エフェクトとカメラは「ほぼ完璧」と言われたので、6・7章はそのまま使う）

### 11-1. 部屋や物の位置を、場面をまたいで変えない
**14章が先**（場所の基準の絵は「渡す見本」にする。人は「足す」ではなく、場所と1枚の絵として描く。寄りの背景は、切り出して貼らず、14-6 の下絵から。場所の物の並びを1つの文に決める事は、そのまま＝14-5 B）。
失敗：場面が替わるたびに、家具・時計・観葉植物の位置が少しずつ変わった。
- **場所ごとに「場所の基準の絵」を作る。** 人のいない、その場所だけの絵を、**使うカメラの向きの数だけ**（多くても3つ：正面・右ななめ・寄り用）先に作る。1枚目を作ったら、ほかの向きは1枚目を見本に渡して「同じ部屋を、別の向きから」と作る。
- **場所の物の並びを、言葉で1つに決めて、その場所の全部の絵の指示に同じ文を入れる**（例の形：「左から、カーテン・ソファ・スタンドの明かり・本だな・テレビ台。時計は本だなの上の壁。床に青いマット」）。場面ごとに書き方を変えない。
- **人や手を写す絵は、その向きの「場所の基準の絵」を元にして「ここに人を足す」で作る**（`EDIT the first attached image. Keep the room, every piece of furniture, the clock and the plants exactly where they are. Add ONLY: …`）。部屋を毎回いちから描かせない。
- 手元の寄りは、背景をぼかさずに写すと位置のずれが目立つ。寄りの絵は、**基準の絵を切り出して背景にする**か、背景の物を3つまでに減らす。
- **検品**：その場所の絵を全部並べて、時計・明かり・テレビ・植物・ソファの位置を1つずつ見比べる。ずれた絵は作り直す。動画にするのは、その後。

### 11-2. 体の大きな動きを、動画の道具にまかせない
**14章が先**（同じ所に立ったまま上半身が大きく動く動きは、14-10 の ACTION の形で、1本でやらせる。立つ⇄すわる⇄寝る・物をまたぐは、この項のまま切る）。
失敗：すわった所から寝転ぶ動きで、手や腕が崩れた。
- **体の向きが大きく変わる動き**（立つ ⇄ すわる ⇄ 寝る、ふり返る、物をまたぐ）は、1本のクリップでやらせない。**動きの前で切り、動きの後の絵から始める**（すでに寝ている所から始める）。どうしても見せる時は、始めと終わりの絵で手足の位置を近くして、動きを小さくする。
- 手が物に触れる・持ちかえる動きも同じ。手は、始めの絵で、もうその形にしておく。
- できたクリップは、1秒6コマで手・指・腕・足を見る。崩れたら、切る位置を変えるか、作り直す。

### 11-3. 止まって見える場面を作らない
**14章が先**（人の出る場面の半分以上で、体の形が変わる動きを書く＝14-17。`freezedetect` の検品は、そのまま）。
失敗：すわっている場面・寝ている場面で、人もカメラも動かず、止まって見えた（機械で測ると、0.5秒以上の止まりが7か所）。
- **人が動かない場面ほど、カメラを動かす**（寄る・回りこむ・上から下りる）。始めの絵と終わりの絵は、必ず大きさか向きを変える。同じ構図どうしは、中の変化（透ける・色が変わる）だけになるので、3秒より長く使わない。
- 人にも、小さい動きを1つ書く（息をする・手を動かす・顔を上げる）。
- **検品（必ず）**：`ffmpeg -i <完成> -vf "freezedetect=n=0.003:d=0.4" -map 0:v -f null -` で、止まりが**0か所**になるまで直す。

### 11-4. 効果音が主役。曲（BGM）は、小さく1曲を通す（2026-10-12 に直した）
- **音の決まり（効果音を入れる時・入れない時・10秒に何回まで・BGM・検品と報告）は、[sound-rules.md](sound-rules.md)。ぶつかる所は、sound-rules.md が先。**
- **ZackDFilms 版は、曲（BGM）を入れる。小さく、1曲を通す。声より 20 LU 下**。前の決まり（2026-10-08「曲は入れない。効果音ベース」）は、これで替わった。効果音が主役なのは、そのまま。曲は、権利のはっきりした自社の曲だけ（音ボックスの `雰囲気別/7-忍び足・好奇心（Zack D型）` の2曲。危機感を強く出す話は `1-暗い・緊張`）。**「かも」だったので、最初の1本は「曲あり」「曲なし」を両方書き出して、運営者 に聞いてもらう。**
- 声 −14 LUFS 前後。効果音は声より 8〜18 dB 下（当たりや山は大きめ、光や印は小さめ。出来事ごとの数は 8章と sound-rules.md 2章）。効果音は、10秒に 4〜6個・上限 7個。
- **新しい効果音の棚**：`（作業フォルダ：アプリには同梱していない見本）`（`棚の一覧.md`・`sounds.json`。出どころの確かさ A〜D つき）。探す順は sound-rules.md 1章。
- **効果音の棚**：`zackdfilms/sfx/`（一覧と中身の説明は `zackdfilms/sfx/一覧.md`）。**手順**：①コマ割りの表から、音が要る出来事を全部書き出す（何の音か・何秒か）②棚の一覧を見て、合う音があるかを1つずつ決める ③**無い音は、足す**：ElevenLabs の効果音を作る口（`POST https://api.elevenlabs.io/v1/sound-generation`、`{"text":"<英語で音の説明>","duration_seconds":<0.5〜3>}`。鍵は `（鍵はアプリの接続で管理）`）で作り、棚に入れて、一覧に1行足す（名前・どんな音・長さ・何に使ったか）。次からは、棚にあるので作らなくて済む ④音は、できた動画のコマを見て、出来事の時刻に置く。
- 権利の分からない音（動画から抜いた音・有料の音の試し聞き）は、棚に入れない。

### 11-5. 声の読みと抑揚
失敗：読みや抑揚がおかしい所があった。
- 声に渡す文は、読みが分かれる言葉を**かなで書く**（その商品の `06_原稿/読みの辞書.md` に、まちがえた言葉と直し方をためる。無ければ作る）。数字も読みで書く（10分＝じゅっぷん）。
- **3回録って、書き起こしで比べる。** 原稿と違う言葉が出た文は、**その文だけ**録り直して差し替える（前後0.15秒の無音でつなぐ）。
- 抑揚は機械では確かめられない。**抑揚がおかしくなりやすい形を、文の側で避ける**：かぎかっこの中の言葉、読点の多い文、文の頭の一語（「今、」「朝、」）、同じ言葉のくり返し。こういう文は、読点を減らすか、2文に分けてから渡す。
- 納品の時に、「耳で聞いていない」と必ず書く。運営者 が聞いておかしいと言った言葉は、読みの辞書に足す。

## 12. 1本目の水準を、毎回出す（**ここは、ほかの章より先。ただし、絵の作り方・ずれ・質感は 14章が先**）

1本目（見本の動画の作業フォルダ：`（作業フォルダ：アプリには同梱していない見本）`。144秒・47場面・使った絵87枚・切り替わり14か所。**数は、どの商品・どの台本の動画にも当てる**）の後、同じ作り方のファイルで2本作ったら、アングル替えが弱くなった。測ると、差は次の4つだった。**「切らずにつなぐ」と書いてあっても、数が無いと、楽な方（切る・同じ構図にする・編集で寄る）に流れる。** だから、数で決める。

### 12-1. 守る数（書き出しの後に測る。外れたら、直してから出す）
**14章が先**：この5つは、そのまま守る。14-17 の7つを足す。絵の枚数には、場所の見本・下絵・数の図・ぼかす前の絵を入れない。
| 測る物 | 決まり | 1本目 | 弱かった2本 |
|---|---|---|---|
| **絵が切り替わる所**（つながずに切る所） | 場面の数の **3割まで** | 14／47（30%） | 32／51（63%）・19／50（38%） |
| **絵の枚数** | 場面の数の **1.8倍以上**（どのクリップも、始めと終わりが別の絵） | 87／47（1.9倍） | 85／51（1.7倍）・61／50（1.2倍） |
| **4秒より長い場面** | 場面の数の **1割まで** | 4／47 | 3／51・16／50 |
| **1場面の平均** | **2.8〜3.2秒** | 3.06秒 | 2.96秒・3.40秒 |
| **編集で足した寄り・引き**（クリップではなく、編集のズーム） | 場面の数の **1割まで** | 少ない | 13／51 |

測り方：`python3 zackdfilms/measure.py <完成の mp4> <seg.json> <kf のフォルダ> [使った絵の一覧.txt]`（絵の枚数は、**動画に使った絵だけ**を数える。作り直しで捨てた絵・場所の基準の絵で使わなかった物は入れない。フォルダに捨てた絵が混ざっている時は、使った絵のファイル名を1行ずつ書いた一覧を4つ目に渡す）（切り替わり・場面の長さ・絵の枚数を出す）。編集のズームの数は、`build.py` で足した数を自分で数えて報告に書く。

### 12-2. つなぎ方（コマ割りの表に「前の場面と、どうつなぐか」の欄を必ず作る）
**14章が先**：つなぐクリップの絵は、全部、つながりの組の最初の絵から作る（14-3 ⑦）。別々に描いた2枚を、1本のクリップでつながない。
- **基本は「つなぐ」**：前の場面の終わりの絵を、そのまま次の場面の始めの絵にする。カメラは、場面をまたいで動き続ける
- **切ってよいのは、3つだけ**：① 見えない所（体や物の中）から、外へ戻る時 ② 場所が変わる時 ③ 時間が飛ぶ時。それ以外で切りたくなったら、つなぎの絵を1枚足して、つなぐ
- **2つの物を行き来する台本**（人と、別の物。外と、中）は、行き来のたびに切らない。**同じ画面の中に両方を入れた絵**（手前に物・奥に人、など）を作り、カメラの寄り・回りこみで、片方からもう片方へ移る
- 表の「つなぎ方」の欄には、`つなぐ` か `切る（①②③のどれか）` を書く。**絵を作る前に、切る所を数えて、3割をこえていたら表を直す**

### 12-3. アングル替え（カメラの道すじを、絵より先に決める）
**14章が先**：「1つの場所につき、カメラの向きを3つ用意する」は、14-3 ⑤（場所の見本を2〜3枚）と 14-6（終わりの向きは、始めの絵から下絵で出す）に替える。終わりの絵に、始めと同じ向きの見本を渡さない。ほかの行は、そのまま。
- コマ割りの表に、場面ごとのカメラの動きを書く：寄る／引く／回りこむ／上から下りる／下から上がる／横へすべる／中へ入る／中から出る
- **同じ動きを、2場面続けない。**「寄る → 寄る → 寄る」は、止まって見えるのと同じ
- **始めの絵と終わりの絵は、大きさ（引き・寄り）か、向き（正面・ななめ・上から）を、必ず変える。** 同じ構図どうしで、中の変化だけを見せるクリップは、1本の動画で5つまで
- 1つの場所につき、カメラの向きを3つ用意する（正面・ななめ・寄り用。11-1 の「場所の基準の絵」）。同じ向きだけで通さない
- 人が動かない場面ほど、カメラを大きく動かす（11-3）

### 12-4. 止まって見える所の直し方（順番を守る）
1. 絵を直す（始めと終わりの大きさ・向きの差を大きくする）
2. クリップを作り直す（カメラの動きを指示に足す）
3. それでも残った所だけ、編集でゆっくり寄る。**編集のズームは、最後の手段**（場面の1割まで）。`freezedetect` を通すためだけに、編集のズームをまとめて足さない

### 12-5. 作り直しの枠を、最初から取る
- 1回目を全部つないだ後に、**全部のコマを見て、弱いカットを10本選んで作り直す**（選ぶ基準：切り替わりが急／カメラが動いていない／同じ構図／手や物の崩れ／声の言葉と変化の時刻がずれている）
- クレジットの見こみは、「1回目の分＋その2割（作り直しの分）」で出す。上限を低く決めて、作り直しを止めない
- 人（別の Claude）に作らせる時も同じ。**コマ割りの表（つなぎ方・カメラの欄つき）ができた所で1度見て、12-1 の数に入っているかを確かめてから、絵を作らせる**

### 12-6. 報告に書く数
12-1 の5つの数を、表にして書く。外れている物を、外れたまま「完成」と言わない。

## 13. 話し手が2人以上の時（台本にかぎかっこのせりふがある時は、必ずここを当てる）

### 13-1. 声を、話し手ごとに変える
- 台本の頭の「話し手の一覧」と、行の頭の札（`【本人】`・`【◯◯】`）で、どの文をだれが話すかを決める。**札の無いかぎかっこが台本にあったら、作り始めずに、台本を直してもらう**
- **語りは、いつもの声**（`W8wofKLOWnsM57L8hIx2`）。**ほかの話し手には、1人に1つ、別の声を当てる。** 声は、ElevenLabs の声の一覧（`GET https://api.elevenlabs.io/v1/voices`）から、話し手の性別・年ごろ・感じに合う物を選ぶ（モデルは `eleven_v4`）。語りと聞き分けられる事が一番（性別・高さ・速さのどれかが、はっきり違う声）
- **画に出ている人のせりふは、その人の見た目に合う声**（性別・年ごろを合わせる）
- **人でない物が話す時**（体の一部・物・商品）は、語りとも、人とも違う声にする（高さ・若さを変える）。1本の中で、その物の声を変えない
- 選んだ声は、作業フォルダの `ad/voices.json` に書く（`{"語り": "...", "本人": "...", "◯◯": "..."}`）。同じ商品の次の動画でも、同じ役には同じ声を使う（商品の `06_原稿/読みの辞書.md` の下に「声の割り当て」として写しておく）
- 録り方：**文ごとに、その話し手の声で録って、つなぐ**（話し手が替わる所は、0.15〜0.25秒の間を置く）。句の時刻（`phrases.json`）に、話し手の名前を入れる
- 検品：完成の声を書き起こして台本と照合するのに加えて、**話し手が替わる所を一覧にして、声のファイルが替わっているかを確かめる**。耳で聞いていない時は、そう報告する

### 13-2. 話している人・物を、画面に出す
- **せりふの間は、その話し手を画面に写す。** 語りの絵のまま、別の人のせりふを流さない
- **人のせりふ**：その人の顔が見える絵にする（口が動いて見える向き。後ろ姿・手元だけにしない）。動画の指示に「口を動かして、一言話す」と書く
- **人でない物のせりふ**：その物を画面の主役にして、**その物から出ている吹き出し（立体の、文字の無い吹き出しの形）**を1つ付ける。話している間、吹き出しが軽くはずむ・その物が声に合わせて小さく脈を打つ、と動画の指示に書く。吹き出しの色は、その話し手の色（下の字幕の色）にする
- 吹き出しの中に、絵で文字を入れない（文字は字幕で出す）
- 同じ話し手が何度も出る時は、**毎回、同じ見せ方**にする（同じ向き・同じ吹き出し）。見る人が「また、あの声の主だ」と分かる

### 13-3. 字幕を、話し手で分ける
- 語りの字幕は、いつもの白
- **ほかの話し手の字幕は、色を変える**（1人に1色。エフェクトの色の意味〈1章〉とぶつからない色。吹き出しと同じ色）。太さ・大きさ・ふち・位置は同じ
- せりふの字幕には、かぎかっこを出す（語りと見分けるため。4章④の「かぎかっこは出さない」は、語りの中の強調のかぎかっこの事）
- 人でない物のせりふは、字幕を吹き出しの近く（その物のすぐ上か下）に置いてよい。その時も、画面の下3分の1より上に出さない

### 13-4. 効果音
話し手が替わる所に、短い合図の音を1つ（その話し手ごとに決まった音。毎回同じ）。語りに戻る所には、置かなくてよい。

## 14. 質感・動き・ずれない作り方（**ここは、15章のほかの全部の章より先**。ぶつかる所は 14-18 の表。物のバグ・カメラの数は 15章が先）

**どの商品・どの場所・どの人物にも、このまま当てる。** 文の中の［ ］と ◯◯ だけを、その案件の物に書きかえる。
道具：`T=ec-ad-ops/references/video-formats/zackdfilms/tools`（一覧と打ち方は `tools/README.md`）。見本の絵・数の例・指示の例：`M=ec-ad-ops/references/video-formats/zackdfilms/見本`。python は `PY=（作業フォルダ：アプリには同梱していない見本）`（cv2・numpy 入り。`python3` では動かない道具がある）。
工程を絵つきで見る：`（作業フォルダ：アプリには同梱していない見本）`。

### 14-0. 先に読む
**まだ確かめていない事**
- **この作り方で、1本通しの動画は、まだ作っていない。** 試したのは、場所1つ・商品1つ・人物1人、クリップは「人に寄る5秒」と「物に寄る3秒」の2種類だけ。
- だから、**最初の1本は、頭の10秒ぶん（クリップ3〜4本）を先に作り、14-11 と 14-17 の数を測ってから、先へ進む。** 数が外れたら、残りを作る前に直す。
- 確かめていない場面：外の場所（かべ・床・天井の箱で書けない場所）／人が2人いる場面／模様の無い商品に寄る場面／クリップの終わりの絵を次のクリップの始めにして3本より長くつないだ時／引きから引きへ30度より大きく回りこむ場面。当たったら、3秒で1本試してから本番に入れる。
- 動画は、試験でも、コマを並べて見ただけ。**再生して見ていない時は、そう報告する。**

**どの場面に、どの手順を当てるか**
| 場面 | 当てる物 |
|---|---|
| **同じ場所・同じ物が、始めと終わりの両方に写るクリップ**（人のいる場面・物に寄る場面・回りこむ場面。主役が人でも物でも同じ） | **全部**（14-1〜14-12）。終わりの絵は、始めの絵から作る |
| 体や物の中だけの絵（背景が無地・中の模型） | 下絵の手順は当てない。絵の指示（14-5 の A〜C）・14-13・動きの線（14-11 の動きの行）だけ |
| 外から中へ入るクリップ（始め＝外の寄り／終わり＝透けた絵） | 始めの絵は 14 の手順で作った絵。終わりの絵は 14-13。位置は「外の形が変わらない」で守る（終わりの絵は、始めの絵を1枚目に渡して EDIT で作る） |
| 場所が変わる所・時間が飛ぶ所（12-2 の「切ってよい3つ」） | 切る。次の場所は、新しい「つながりの組」として 14-2 の 1 から |

### 14-1. 芯（なぜ、この順か）
1. **ずれの正体**：始めの絵と終わりの絵を別々に描くと、2枚が「同じ1つの世界を、2つのカメラから見た絵」にならない。合わない分を、クリップの道具が、物を動かして（すべらせて・ゆがめて・消して）つなぐ。**主役が人でも物でも同じ。** 人の場面でばれにくいのは、人が動く事と、寄りのぼけにかくれるだけ。だから、確かめの線は、場面で変えない。
2. **位置の伝え方の強さ**（試験で測った）：言葉だけ＝守られない ／ 灰色の箱の下絵＝幅の5〜13%ずれる ／ **色のついた絵そのものを下絵にして「塗り直すだけ」＝1画素以下。** だから、**終わりの絵は、新しく描かせない。始めの絵を、終わりのカメラから見た形に動かして下絵にし、「位置・大きさ・数は変えず、塗り直すだけ」と仕上げさせる。**
3. 確かめは、**ぼかす前の絵**でする。ぼけで、ずれをかくさない。ぼかすのは、通った後。寄りは、背景だけをぼかす。
4. 寄りの速さは、絵ではなく、**動画の指示**で決まる（14-10）。

### 14-2. 作る順（番号を変えない）
| 順 | する事 | 所 |
|---|---|---|
| 1 | **場所の表・商品の表・人物の文**を、文で1回だけ書く。数が命の模様がある商品は、**数の表**と数の図を作る | 14-3 |
| 2 | **場所の見本**を作る（人も商品も無い場所の絵。向き違いで2〜3枚） | 14-3・14-5 D |
| 3 | コマ割りの表（9章・12-2・12-3）に、**つながりの組**と、クリップごとの「始めのカメラ → 終わりのカメラ」を言葉で書く | 14-3 |
| 4 | **始めの絵**を、質感の文でふつうに描く（全部にピント）。人物が写真か人形に寄ったら、人物だけ直す。模様のある商品は、数を機械で数える | 14-5 A〜E・14-8 |
| 5 | 始めの絵から、**カメラを出す**。床・かべ・家具・人・目印を、数にする | 14-6 |
| 6 | **終わりのカメラ**を決める。下絵を何枚も出して（0円）、穴の % と、物の見え方で決める | 14-7 |
| 7 | **下絵**を1枚目に渡して、**仕上げ**させる（同じ文で2枚同時に出す） | 14-5 F |
| 8 | **ぼかす前に、機械で確かめる。** 通った方を取る。外れたら、仕上げだけやり直す（2回まで） | 14-8 |
| 9 | 寄りで終わる絵は、**背景だけぼかす**（位置は1画素も動かさない） | 14-9 |
| 10 | **クリップ**を作る（先に3秒で試してよい。動きとカメラを秒で書く） | 14-10 |
| 11 | **クリップを測る**：動かないはずの物が動いていないか・模様の数・動き・寄りの速さ | 14-11 |
| 12 | 外れたら、14-12 の順で直す。通った絵・数・指示は、次の場面で使い回す | 14-12・14-16 |

### 14-3. 先に用意する物（1つの動画で1回）
**作業フォルダの形**（道具が、この形で読み書きする）：`ref/`（場所の見本・人物の基準・形の見本）・`kf/`（始めの絵・下絵・仕上げ・終わりの絵。指示の文と渡した見本も残る）・`work/`（数の json・確かめの絵）・`clips/`（クリップ・指示・クレジットの記録）。

**① 場所の表**（その場所が写る全部の絵に、一字も変えずに入れる。14-5 B）。物は、引きで5〜8個。色・材料・変わりやすい部品を1つずつ書く。
**② 商品の表**（商品が写る全部の絵に、一字も変えずに入れる）。**同じ形がならぶ模様（行×列）を持つ商品**は、行と列の数・1個の形を書く。
**③ 数の表と数の図**（模様の数が1個違ってもだめな商品だけ）：形の表（`$M/数の例_物/PROD_model2.json` を写して、大きさ・行・列・間かく・1個の形を書きかえる）→ `$PY $T/make_relief.py <形の表.json> kf/PROD` → `kf/PROD_top.jpg`（＝数の図。真上から）と `kf/PROD_pts.json`（模様の中心の表）。数の図の例：`$M/数の図の例_真上から.jpg`。
**④ 人物の文**（その人が写る全部の絵に、一字も変えずに入れる）：性別・年ごろ・髪・服（1色、強い色）を1〜2文。質感は 14-5 C の文（4番）で決まるので、ここには書かない。
**⑤ 場所の見本**：人も商品も無い、その場所だけの絵を、質感の文で、**向き違いで2〜3枚**（1枚目＝一番多く使う引きの向き。2〜3枚目＝1枚目を渡して、別の向き・低い向き）。例：`$M/場所の見本の例_A〜C.png`。**完成の絵に貼る物ではなく、毎回渡す見本。** よく効く（物の形・色がそろう）。
**⑥ 形の見本**（高さのある模様・突起を、低い角度から写す場面がある時だけ）：その模様1個を、**低い角度から見た、正しい形の絵**を1枚（質感の文で描く。数や並びは問わない）。例：`$M/形の見本の例_低い角度.png`。
**⑦ つながりの組**：切らずにつなぐクリップの列（12-2）。**1つの組の中の絵は、全部、その組の最初の「始めの絵」から作る**（終わりの絵 → 次のクリップの始めの絵 → その終わりの絵 …）。別々に描いた2枚を、1本のクリップでつながない。組を短くするコツ：
  - **行って戻る**：引き → 寄り のクリップで作った2枚は、逆にして 寄り → 引き のクリップにも使える（同じ2枚なので、ずれない。未確認：逆向きのクリップは試していない）。
  - 組が替わる所（別の始めの絵に移る所）は、12-2 の「切ってよい3つ」か、中へ入る・中から出る（7章）に当てる。
  - 12-1 の「切り替わりは3割まで」は、そのまま。3割をこえそうな時は、別々に描いた絵をつなぐのではなく、組をのばす（終わりの絵を次の始めにする・途中の絵を足す）。それでもこえる時は、数を報告して、依頼主に聞く。

### 14-4. 毎回渡す見本の絵（4枚まで。**1枚目が一番強く効く**）
| 作る絵 | 1枚目 | 2枚目 | 3枚目 | 4枚目 |
|---|---|---|---|---|
| 場所の見本 1枚目 | `$M/本物_人物_日光.png`（質感） | `$M/人物_4番_引き.png`（質感。人は写さない、と文に書く） | — | — |
| 場所の見本 2〜3枚目 | 場所の見本 1枚目 | `$M/本物_人物_日光.png` | — | — |
| **始めの絵・人のいる引き** | 場所の見本（その向きに近い物） | 場所の見本（別の向き） | `$M/人物_4番_引き.png` | `$M/本物_人物_日光.png` |
| **始めの絵・物の引き** | 場所の見本（その向きに近い物） | **数の図**（模様のある商品） | 商品1個の形の見本（商品の写真か、通った絵） | `$M/本物_人物_日光.png` |
| 人物だけの直し | 直す絵 | `$M/本物_人物_日光.png` | `$M/人物_4番_引き.png`（寄りは `人物_4番_寄り.png`） | — |
| **終わりの絵（仕上げ）・人** | **下絵** | **始めの絵** | `$M/人物_4番_寄り.png`（引きで終わる時は `_引き`） | 人の借り元の絵（14-6 の A5。無ければ、**始めと違う向き**の場所の見本） |
| **終わりの絵（仕上げ）・物** | **下絵** | **始めの絵** | **始めと違う向き**の場所の見本（低いカメラで終わる時は、低い向きの見本） | 形の見本（⑥。無ければ、商品の寄りの見本） |
| 透けて中を見せる絵 | 始めの絵（外の寄り） | `$M/参考_透ける_頭.png` | `$M/本物_透ける_腕.png` | — |

- **終わりの絵に、始めと同じ向きの場所の見本を渡さない。** 渡すと、背景だけ、始めのカメラのまま写してしまう（物が床をすべるクリップになった原因）。渡してよいのは、別の向きの見本だけ。文にも `never copy its framing or its object positions` と書く（14-5 F）。
- 2本目からの動画では、3〜4枚目の質感の見本を、**その動画の通った絵**に替えてよい。
- **`style_確定_2-2.png` は、渡さない**（渡すと、なめらかで全部にピントの、人形に寄った絵に戻る）。
- 灰色の箱の下絵（`layout.py`）は、始めの絵の構図を細かく決めたい時だけ、1枚目に足してよい。位置は幅の5〜13%ずれる物として使う（並ぶ順・大きさ・カメラの向きを伝えるだけ）。終わりの絵には使わない。
- `$M/本物_*.png` は本物（ZackDFilms）のコマ、`$M/参考_*.png` は依頼主が足した参考動画のコマ。絵柄の手本にだけ使い、完成の動画には1コマも使わない。

### 14-5. 絵の指示に必ず入れる文（そのまま写す。［ ］だけ書きかえる）
始めの絵・場所の見本は、**A → B → C（人がいる時）→ D か E** の順に、1つの文につなぐ。終わりの絵は **F** だけ（F の中に C が入る）。

**A. 絵柄・光・レンズ・ピント**（全部の絵。3章の STYLE BASE は使わない）
```
STYLE BASE: the attached reference frames show the target LOOK. Match their rendering quality, lens, light and color; do NOT copy their content, their people or their caption words. RENDER: a real-time game-engine 3D render, like a modern Unreal Engine cutscene. Clearly computer animation at first glance: not a photograph, not photorealistic, and also not a smooth toy, not clay, not Pixar, not a cartoon. LIGHT: one hard key light from [the upper front-left / the window on the left / the sun]. Crisp cast shadows with a clear shape fall on the body and on the ground; the shadow side is darker but still shows color; a thin bright rim of light runs along the edge of the hair and shoulders. No flat even light, no haze, no glow. COLOR: clean and contrasty but not oversaturated; one strong clothing color; deep (not black) shadows; plants and floors are simple, without tiny detail. LENS: [下の「レンズ」から1文] FOCUS: [下の「ピント」から1文] No text, no letters, no captions, no logos. Vertical 9:16.
```
レンズ（絵ごとに1つ。**カメラの高さと距離を、必ず書く**）
- 引き・上半身：`a wide-angle lens (about 20 mm) placed close to the subject: things nearer to the camera are clearly bigger than things farther away, vertical lines lean and converge, the horizon is tilted 3-5 degrees. The camera is at [hip / chest / ground / above-head] height, about [1.8] meters from [SUBJECT], looking [up / down] at it. Never a flat, straight-on, eye-level view.`
- 寄り：`a wide-angle lens (about 20 mm) only [20] cm from [SUBJECT], [below / above] it, looking steeply [up / down]: the part nearest to the camera looks large, the far part smaller.`
- 真横で見せる絵（透けて中を見せる絵など）：`a normal lens at the height of [PART], exactly side-on.`

ピント
- **始めの絵・終わりの絵（ぼかす前）は、全部これ**：`deep focus. [SUBJECT] AND everything behind it are razor sharp; no background blur, no depth of field, no bokeh, no haze, no glow.`（確かめのため。ぼけは、通った後に機械でかける＝14-9）
- 下絵を使わない寄りの絵（体や物の中へ入る前の、つながりの組の最初の絵が寄りの時だけ）：`shallow depth of field, like a portrait lens wide open: ONLY [主役のどこ] is razor sharp. Everything behind it is strongly out of focus: big soft blurred shapes of color, no readable detail, no sharp edge anywhere in the background.`

**B. 場所の表・商品の表**（14-3 の ①②。全部の絵に、一字も変えずに）
```
PLACE ([場所。時刻]; this list is FIXED, every item exists exactly once): [かべ・床・天井の色と材料]. Along the [どのかべ], from left to right: (1) ONE [◯◯：色・材料・部品]; (2) ONE [◯◯]; … Along the [別のかべ]: (n) ONE [◯◯]. Nothing else: no [出やすい余分な物を3つ].
```
```
PRODUCT (FIXED): ONE [商品] [置き方]: [形・大きさ(cm)・厚み・色・材料]. On [どの面] sit [模様1個の形・大きさ・材料]. They form a perfectly regular straight grid: EXACTLY [列の数] along the long side and EXACTLY [行の数] across the short side = [合計] on [どこ], evenly spaced with [地の色] visible between them, none missing, none extra, none merged, all the same size. Every [模様1個] is complete and of identical size: no half one, no squashed one, none squeezed between two others. The [商品] is a solid 3D object: real thickness, a soft contact shadow, every [突起] casts its own small crisp shadow.
```
（模様の無い商品は、`On [どの面] sit …` から `… between two others.` までを外し、形・部品・色を書く。）
数の図を渡した絵には足す：`The [n-th] attached image is the COUNT CHART of the [商品] seen from straight above (gray diagram, not a style reference): [図の見方]. Count the columns on the chart and paint exactly that many: [列の数] columns of [行の数].`

**C. 人物の質感＝4番**（人が写る全部の絵。**14-2 の案にあった「CG skin shader … faint surface texture … realistic face shape」の人物の文は使わない**。見本：`$M/人物_4番_引き.png`・`_寄り.png`。なぜ効くか：`（作業フォルダ：アプリには同梱していない見本）`＝本物の人物は「形は実寸の大人・表面は模型」）
```
PERSON RENDERING (match the way the PEOPLE are rendered in the attached person reference images: skin, eyes, eyebrows, hair, hands, cloth; not their content, not their faces, not their backgrounds): [He / She] is a simpler, older-generation real-time 3D game character (around 2010), obviously a video game model. The surface is SMOOTH-shaded: no visible flat polygon facets, no faceted low-poly art look. SHAPE: a simpler model with less modeled detail: the facial features are clear-cut and simple: a simple firm nose, a firm jaw line, lips as a simple clean shape, eyelids as crisp edges, simple ears. No wrinkles at all except one crease between the eyebrows and one from the nose to each mouth corner. SKIN: a single flat skin color, completely smooth, close to hard semi-gloss plastic, like a shop mannequin, with small crisp white highlights on forehead, nose, cheekbone and knuckles; no pores, no texture, no flush. EYES: simple and clear, a flat iris with one white dot highlight. EYEBROWS: solid dark painted bands. TEETH: one white block. HAIR: five to eight big solid smooth chunks with a few painted lines, a hard edge at the hairline, glossy like molded plastic. HANDS: simple and smooth, with a single line at each joint and nails drawn as flat lighter patches. CLOTH: [服] keeps only a very faint knit texture and three or four big simple folds; [ほかの服] is flat [色]. Still realistic adult proportions and a normal-size head and eyes: NOT a toy, NOT clay, NOT Pixar, NOT a cartoon, NOT anime, not cute.
```
人物が写真に寄った・人形に寄った時の直し方（その絵を1枚目に渡して、もう1回。試験で「4番」を作った文）
```
EDIT the first attached image. Keep the composition, camera, lens, pose, hands position, clothes, background, light, shadows and depth of field exactly. Do not move, zoom or re-frame anything. [He / She] stays the same [人物の文] with the same face shape, the same hairstyle and the same expression. Change ONLY the rendering of the person: [上の PERSON RENDERING の文を、"[He / She] is a simpler" の代わりに "[he / she] becomes a simpler" として、全部入れる] No text, no letters, no captions, no logos. Vertical 9:16.
```
直した後は、直す前と後を並べて、背景と構図が変わっていない事を見る（`$PY $T/sheet.py out.jpg 800 前.png 後.png`）。

**D. 場所の見本を作る絵・場所の見本を渡した絵に入れる文**
```
The attached color image(s) of the empty [場所] are the PLACE REFERENCE: they show the same [場所] from other camera positions. Every object must be the SAME object as there: the same design, the same colors, the same materials, the same parts ([目印ごとに、変わりやすい部品を1つずつ]), and the same [光]. Take the look of the objects from the place reference; never copy its framing.
```
場所の見本そのものを作る絵は、頭を `Create a NEW image: an empty [場所], no people, no [商品].` にして、A・B を続ける（全文の例：`$M/指示の例/場所の見本.txt`）。

**E. 始めの絵の頭と、人・物の文**
```
Create ONE finished picture: [主役] AND [場所] together, rendered as one image and lit by the same light.
```
- 人：人物の文（14-3 ④）＋体の形を1〜2文。**人が動く場面は「動きの途中のコマ」にする**（`frozen mid-motion` と書く。立っているだけ・すわっているだけにしない）。手に取る物は、最初から持たせる（4章②4）。
- 始めの絵の**構図で、先に手を打つ事**（後で直せない）：
  - **奥行きのある大きい物（大きい家具など）を、カメラの動きの道から外す。** 見え方が大きく変わりながら画面の外へ出て行く物は、クリップの途中でゆがみやすい（14-12 の 4）。始めの絵で、その物がしめる面積を小さくするか、動く向きと反対のはしに置く。
  - 寄りで終わるクリップは、主役の大きさを6倍以上変える（始め：全身が高さの20〜25%・物は全体が写る／終わり：主役の一部が幅の60〜75%）。
  - カメラの高さか向きを、終わりで必ず変えられる構図にする（腰の高さで見上げる → あごの下／上からななめ → 床すれすれ）。
  - 目印（色か形がはっきりした、動かない物）が、主役にかくれずに4個以上写る事。
- 全文の例：`$M/指示の例/人の始めの絵.txt`・`物の始めの絵.txt`（**試験の場面の言葉が入っている。型だけ見る**）。

**F. 終わりの絵＝仕上げの文**（1枚目＝下絵。**新しく描かせない**）
共通（頭から終わりまで、この順で1つの文にする。F1〜F5 は、当たる物だけを、`FINISH PASS ONLY …` の文の後ろに入れる）
```
EDIT the first attached image. The first image is a CAMERA-MOVE PREVIEW of [場所] with [主役]. It was made by re-projecting the SECOND attached image (the same place and the same [主役] a moment earlier, seen from [始めのカメラを言葉で]) into the new camera, which [終わりのカメラを言葉で]. Its camera, lens, perspective, tilt, framing and the position, size and outline of every object are FINAL and correct. Keep the camera and every existing object at exactly the same pixel position, size, outline, proportions and color; keep the same image size and aspect ratio. Do not move, resize, rotate, add, remove or redesign anything: every object appears exactly once, with the same parts in the same places ([下絵に写っている物だけを、ONE ◯◯ の形で、画面のどこにあるかと一緒に並べる]). Do NOT add [その場所の物のうち、下絵に写っていない物] or any other object: those are hidden behind [主役] or outside the frame. FINISH PASS ONLY: repaint the surfaces of what is already there so that everything reads as SOLID 3D geometry in the same materials and the same render style as the SECOND attached image: real thickness, front, side and top faces, crisp straight edges, a soft contact shadow where each object meets the floor. LIGHT: [始めの絵と同じ光を1文]; keep the light patches and the cast shadows exactly where they are drawn. Clean up render defects: blotchy halos around objects, smeared or streaked patches, torn, stretched or doubled edges become clean plain [wall, floor and ceiling]. [F1〜F5] FOCUS: deep focus. [主役] AND everything behind it are razor sharp; no background blur, no depth of field, no bokeh, no haze, no glow. RENDER: a clean real-time game-engine 3D render, clearly computer animation, exactly the style of the second image; not a photograph, not a toy, not clay, not a cartoon. No text, no letters, no numbers, no captions, no logos. Vertical 9:16.
```
- **F1. 写っていなかった所をうめる**（穴がある時は必ず。穴の絵 `_hole.png` を見て、所ごとに書く）
```
FILL THE UNSEEN AREAS as the same [場所] (the preview has flat or smeared placeholder patches where the earlier camera could not see): (a) [画面のどこ] is [その場所の何か：同じかべ・同じ床・天井]: paint it as the same [色・材料], meeting [となりの面] in one straight line; (b) … Do not put any new object into these areas.
```
  穴が広い時（**絵の3割近く**）は、**始めと違う向きの**場所の見本を渡して足す：`The [THIRD] attached image shows the same [場所] from another camera: use it ONLY to see the materials and what the [場所] looks like beyond the edges of the first image; never copy its framing or its object positions.`
- **F2. 人**（下絵の人の、画面での位置を、下絵の info の数から % で書く）
```
THE [PERSON]: keep [him / her] exactly where [he / she] is drawn in the first image, at the same size and with the same outline: [頭のてっぺん・鼻・あご・足などを "at N% from the left and N% from the top" で3〜4点。頭が幅の何%〜何%か]; seen from [終わりのカメラの向き]; [表情と手の形を1〜2文]. Do not move, zoom, shrink, enlarge, mirror or re-pose [him / her]. Repaint [him / her] cleanly as one solid 3D figure lit by [光], and paint [下絵の人のまわりの、引きのばされた所] as the normal [服の部分]. [He / She] is the same [人物の文] as in the SECOND [, THIRD and FOURTH] attached image[s]. [C の PERSON RENDERING の文]
```
- **F3. 主役の物**
```
PRODUCT: the [商品] is FINAL in position. Do not move, simplify or restyle the layout: keep every [模様1個] at exactly the same position, the same count of rows and columns, the same size and the same outline. The edges, the corners and the thickness of the [商品] stay exactly as drawn. Nothing is added on or around it.
```
- **F4. 画面のはしで切れる、奥行きのある物**（箱で動かした物。14-6 の B2）
```
[OBJECT] AT THE [LEFT / RIGHT] EDGE: the [色] block at the [left / right] edge of the first image is the end of the [OBJECT] of the second image, cut by the edge of the frame. Its position, its size, its height and the pixel where its front corner meets the floor are FINAL: keep its outline as drawn, do not widen it, do not lengthen it, do not move it toward the centre, do not add [その物の部品]. The [THIRD] attached image shows the same [OBJECT] from another low camera: use it only to paint this block as that same [OBJECT], repainted in place.
```
- **F5. 形の見本**（高さのある模様を、低い角度から見る絵は、必ず。入れないと、仕上げが形を作りすぎる＝大きい山が少しだけ、になった）
```
SHAPE OF ONE [模様1個]: the [FOURTH] attached image shows this same product up close. The shape of one [模様1個], the size and number of its [突起] and its gloss must be THE SAME AS IN THE [FOURTH] IMAGE: [形を言葉で：大きさ・数・材料・つや]. Do NOT draw [作りすぎた形：a few big …, tall …, flat folded-paper facets]: wherever the first image shows [下絵の大まかな山], replace them, in place, with [見本の突起]. Take from the [fourth] image only the shape and material of one [模様1個], not the camera, not the number and not the arrangement: the position, the grid and the count stay exactly as in the first image.
```
  F5 を入れる時は、F3 に「突起の数・高さは下絵のまま」と書かない（下絵の山の形を守らせると、見本の形にならない）。守らせるのは、模様1個の位置・大きさ・輪かくだけ。下絵の模様も、形の見本に近い大きさ・数で出しておく（形の表の突起を「小さく・多く・低く」）。
- 全文の例：`$M/指示の例/人_仕上げ.txt`・`物_仕上げ.txt`（**試験の場面の言葉が入っている。型だけ見る**）。下絵と仕上げの例：`$M/人の場面_2下絵.png` → `_3仕上げ_ぼかす前.png`、`$M/物の場面_2下絵.png` → `_3仕上げ_ぼかす前.png`。
- 仕上げは、**同じ文で2枚同時に出し**（`gen.sh` を2つ、名前を変えて）、14-8 の数の良い方を取る。

絵を作る打ち方（Codex だけ。Higgsfield で絵を作らない）：`$T/gen.sh <作業フォルダ>/kf <名前> <指示の文.txt> <見本1> [見本2 見本3 見本4]`

### 14-6. 始めの絵から、下絵を作る（道は2つ。どちらも0円・何回出してもよい）
**どちらの道でも、カメラと物の位置は、描かれた絵そのものから出す。** 絵を描かせる時に決めた数（灰色の下絵のカメラ・数の図の向き）は使わない（描かれた絵は、それと1m・50度ちがう事があった）。画素を読む時は `$PY $T/gridview.py <絵> out.jpg [x0,y0,x1,y1] [倍率]`（50画素ごとの目もり）。

| | **道A：場所の線から**（`calib.py` → `warp.py`） | **道B：商品の模様から**（`lock_calib.py` → `lock_render.py`） |
|---|---|---|
| 使う場面 | **人のいる場面**。模様の無い物の場面（未確認） | **行×列の模様を持つ商品が、床に大きく写る場面** |
| 要る物 | 場所の大きさ（m。大まかでよい。絵の中でつじつまが合えばよい）・かべと床と天井の線が始めの絵に写っている事 | 形の表・模様の中心の表（14-3 ③）・`layout.json` の `product` |
| 人 | 切りぬいて運べる | 運べない（人のいない場面だけ） |
| 奥行きのある物 | 立てた1枚の面だけ（箱は無い） | **箱にできる**（B2） |
| 数の例 | `$M/数の例_人/` | `$M/数の例_物/` |

**道A（作業フォルダで打つ）**
1. カメラ：始めの絵で、場所の線の上の点を読む（奥のかべと天井の角 1点・奥のかべと天井の線 2点・奥のかべと床の線 3点・横のかべと天井の線 1点）。`work/calib.json`（例を写して書きかえる）→ `$PY $T/calib.py work/calib.json work/views.json S`。**残りが幅の1%以下**なら使う。
2. `work/scene.json`（例を写して書きかえる。書き方は `warp.py` の頭）：物ごとに、始めの絵でその物をかこむ線（`poly`）と、床に付く所（`line` か `at`。m は、床に付く点の画素を床に当てて出す）。人の足もとのまん中（`person_at`）。**目印**（`marks`）：確かめに使う、動かない物の点を6〜9個（かべの上の物・床の上の角・物の脚）。
3. 人の切りぬき：`$T/fgmask person kf/start.png work/person.png`。白黒に直す：`$PY -c "import cv2,sys;m=cv2.imread(sys.argv[1],0);cv2.imwrite(sys.argv[2],((m>127)*255).astype('uint8'))" work/person.png work/person_bin.png`。人を消した絵：`$PY $T/plate.py kf/start.png work/person_bin.png <始めと同じ向きの場所の見本> work/plate.png [--erase "x,y,r"]`（見本の中で、始めの絵と位置がちがう物は `--erase` で先に消す。消さないと、その物が2個になる）。ここだけは、同じ向きの見本を使ってよい（人の後ろをうめるだけ）。
4. 下絵：`$PY $T/warp.py work/scene.json S <終わりのカメラ> kf/under.png --info work/under.json`。終わりのカメラは `work/views.json` に `{"名前": {"pos":[x,y,z], "look":[x,y,z], "roll":度, "hfov":始めと同じ}}` で足す（X右・Y上・Z奥・m。主役の足もとを中心に、角度・きょり・高さから pos を出す）。出た数のうち、穴の %（`hole_pct`）を見る。始めのカメラの層の絵も出す（クリップの確かめに使う）：`$PY $T/warp.py work/scene.json S S work/startview.png --info work/startview.json`。
5. **人に寄って終わる時**（始めの全身の切りぬきを近くから見ると、使えない）：背景だけを動かし（`$PY $T/cands.py <主役の点x> <y> [前かがみの m]`。`work/cands.json` に案を書く）、人は「大まかな位置」だけ入れる：`$PY $T/paste_person.py work/c_<案>.png work/c_<案>.json kf/under.png <倍率> <右へ 幅の割合> <下へ 高さの割合> <人の借り元の絵> <その切りぬき>`。**人の借り元の絵**＝同じ人を、終わりに近い向き・大きさで、ふつうに描いた寄りの絵（A・C・E の文で1枚。背景は使わない。位置も問わない）。終わりの絵に写る目印（主役にかくれない物）は、下絵を目もりつきで見て、`work/under.json` の `marks` に足す。横の線の目印には `"axis":"y"` を付ける（線にそった向きは位置が決まらないため）。
6. 引きから引きへ、人ごと回りこむ時：人は平らな切りぬきで運ばれる。**回りこみは12度まで**が試した範囲。それより回す時は、仕上げの後に、人だけを直す（その絵を1枚目に渡し、「背景は1画素も変えない。人だけ、体ごと少し回す。頭・足の位置と大きさは同じ。小さな変化・横向きにしない・輪かくはほぼ同じ」と書く。強く書くと回しすぎる）。

**道B（作業フォルダで打つ）**
1. カメラ：`$PY $T/lock_calib.py kf/start.png --layout work/layout.json --bg <地の色 R,G,B> --fg <模様の色 R,G,B> --tol 40 --out work/camS.json --sheet work/camS.jpg`。見る数：`rms_px`（1画素前後なら良い）・`f_each` の2つが近い事。印の絵で、行・列の番号の向きを目で見る。色は、描いた絵から取り直す。
2. `work/world.json`（例を写して書きかえる。書き方は `lock_render.py` の頭）：かべが床に付く線（`walls`）・うすい物は立て板（`boards`）・床の上の目印（`marks`）・商品（`product`）。**奥行きのある物（上の面が始めの絵に大きく写っている物）は、立て板にせず、箱にする**（`boxes`：前の面が床に付く線の2点・始めの絵でのわく・直方体の 長さ a・奥行き d・高さ h）。箱の数は `$PY $T/box_fit.py work/world.json out.jpg` で、線が物の角に乗るまで直す（大まかでよい）。1枚の板のままだと、低いカメラから見えないはずの面（上の面）が下絵に出て、クリップの途中でゆがむ。
3. 下絵：`work/views.json` に `{"名前": {"pos":[x,y,z], "look":[x,y,z], "roll":度}}` → `$PY $T/lock_render.py work/world.json <名前> kf/under.png --info work/under.json --depth work/under.npy`。

### 14-7. 終わりのカメラの決め方（下絵を3〜8つ出して、並べて決める）
1. **「写っていなかった所（穴）」の % が小さい範囲で、できるだけ大きく動かす**（高さ・上下の向き・かたむき・近さ・回りこみ）。目安：**5%まで**＝そのまま。**5〜30%**＝F1 を所ごとに書き、別の向きの場所の見本を渡す。**30%より上**＝カメラを直す（上へ向けすぎ・回しすぎ）。
2. 回す向きは、目印が主役の後ろへ入らない方。寄りで終わる時は、主役の横に目印が2個以上残る向き（残らない向きは、背景が無地だけになり、絵がさびしく、確かめも弱い）。
3. 箱の物は、**画面のはしに少しだけ残る（絵の2〜4%）か、まったく写らない**向きにする。位置と高さは変えず、見る点だけを左右に動かして合わせる。
4. 寄りの終わりの大きさは、7章のとおり（名前を言う物は幅の25〜45%。顔と結果の画面だけ、幅の60〜75%）。
5. **写して使える数**（試験で通った数。場所の大きさがちがっても、見当に使う）：
   - 人の顔へ寄る：主役の点から 0.4〜0.5 m・主役より 12度下から・始めの向きから 30〜40度回りこむ・かたむき −2度・レンズは始めと同じ。（下から20度より大きいと、背景が天井だけになる。30度より大きく回すと、穴が10%をこえやすい）
   - 床の物へ寄る：高さ 1.1 m でななめ上から → 高さ 0.1 m・物の角のすぐ外・かたむき −8度。上へ向けると穴が20〜30%になるので、向きは下げる。
   - 引きのまま回りこむ：主役から見て 12度・きょり 1.9 → 2.3 m・高さ 1.27 → 1.15 m。
6. 決めたカメラの数（回りこみの度・きょり・高さ）は、**仕上げの文と動画の指示に、同じ数で書く**（文だけ別の数を書かない）。

### 14-8. ぼかす前に、機械で確かめる（通す線。**場面で線を変えない**）
| 絵 | 見る事 | 道具 | 通す線 |
|---|---|---|---|
| 始めの絵 | 模様の数と並び（模様のある商品。全体が写る絵） | `$PY $T/check_pattern_clip.py <絵> --bg R,G,B --fg R,G,B --tol 30 --grid 行x列` | 行・列・個数が表と同じ。あな 0・余分 0・ずれ 12%以下 |
| 始めの絵 | 人物 | 並べて目で見る | 写真に見えない・人形に見えない。顔が、ほかの絵と同じ人 |
| 始めの絵 | ぼけ（全部にピントか） | `$PY $T/bokeh.py a=<絵>` | soft 0.15以下 |
| **終わりの絵（道A）** | 目印が、計算の位置にあるか | `$PY $T/check_end.py <仕上げ> --under kf/under.png --info work/under.json --sheet out.jpg --json out.json` | **目印のずれ 幅の2%以下・全体の上位5%も2%以下**（試験で通った絵は 0.1〜0.3%）。「測れない」目印は、重ねた絵で目で見る |
| **終わりの絵（道B）** | 仕上げが、下絵から動いていないか | `$PY $T/lock_drift.py kf/under.png <仕上げ> --info work/under.json --json out.json` | **ずれ 幅の1%以下**（通った絵は、模様のまん中 0.11%・最大 0.24%） |
| 終わりの絵（箱の物がある時） | **カメラより高い上の面が、写っていないか** | `$PY $T/box_overlay.py work/world.json work/under.json <仕上げ> out.jpg` を目で見る | 見えるはずのない面が0。角のずれ 幅の1%以下（角が合っていても、面がまちがっている事がある。必ず目で見る） |
| 終わりの絵 | 下絵に無い物が足されていないか・人が同じ人か・4番の質感か | 下絵・仕上げ・始めの絵を並べて目で見る（`$PY $T/sheet.py out.jpg 800 絵1 絵2 絵3`） | 足された物 0・模様の形が見本の形 |
- 模様の数は、**1回で通らない事がある**（試験では、6枚描いて通ったのは1枚の時があった）。2枚ずつ同時に出す。3回（6枚）外れたら 14-14 の逃げ道。**通った始めの絵は、同じ商品のほかの場面でも使い回す**（14-16）。
- 低い大写しの終わりの絵は、模様が重なって数えられない。数は「下絵（数が決まっている）から、模様1個ずつが動いていない」（`lock_drift.py`）で確かめる。

### 14-9. 通った後に、ぼかす（寄りで終わる絵だけ。**背景だけ**。位置は1画素も動かさない）
- 人：`$T/fgmask person <仕上げ> work/end_person.png` → `$PY $T/blur_bg.py <仕上げ> work/end_person.png kf/end.png 26`（半径 26画素。絵の幅 941 の時）。
- 物（道B）：`$PY $T/lock_blur.py <仕上げ> work/under.npy kf/end.png --focus 0.3 --max 9 --keep 0.35`（ピントの距離から遠いほど強く。主役の手前はぼかさない）。
- ぼかす前の絵は `kf/end_sharp.png` で残す（確かめた絵。次のクリップの下絵を作る時の元にもなる）。クリップに使うのは、ぼかした `kf/end.png`。
- 線：`$PY $T/bokeh.py a=kf/end.png` の **soft 0.30以上**。ただし、**主役が絵の7割より多くをしめる絵・背景が無地のかべや空ばかりの絵は、数が上がらない**（試験の通った絵で 0.11）。その時は、ぼかす前と後を並べて、背景の物のふちが消えている事を目で見て、そう報告に書く。
- 引きで終わる絵は、ぼかさない（soft 0.15以下）。

### 14-10. 動画の指示に必ず入れる文（この順で1つの文にする。4章③の「毎回付ける文」と 7章の CAMERA の文は、この形にまとめた）
```
[場所と主役を1文]. FIXED THINGS: [場所の物を全部] are fixed to the [room / ground]; only [動く物：the person and the camera / the camera] move[s]. [人がいる時] ACTION, in order, big and clear (the face keeps its shape and stays the same 3D game character the whole time): (1) 0.0-[0.4] s: [動きだし]; (2) [0.4]-[1.6] s: [体の形が大きく変わる]; (3) [1.6]-[3.2] s: [その形のまま、次の動き]; (4) [3.2]-[5.0] s: [終わりの絵の形になる]. [His / Her] feet stay on the same spot the whole time; [he / she] does not walk. CAMERA: starts [始めのカメラの高さ・距離・向き], with the whole [場所] behind in sharp focus. [下の「速さ」から1つ] LENS: a handheld wide-angle lens close to the subject. Nothing passes in front of the lens. FOCUS: [下の「ピント」から1つ] BACKGROUND: the [場所] is solid 3D geometry. [目印を全部、色つきで] are the same objects at the same places from the first frame to the last; as the camera [動き] they only shift by correct parallax, [終わりにどうなるかを、物ごとに：slide behind the subject / leave the frame on the right / stay at the left edge] and get blurred. Nothing slides on the floor or along the wall, nothing appears, disappears, multiplies or changes shape, size or color. Natural real-time speed. No cuts, no scene change. Same 3D game-engine render style, same smooth plastic-like CG skin, same hair, same [光], same [服] from first frame to last. The camera never stops. No text, no captions, no subtitles, no logos.
```
**速さ**（寄りの速さは、ここで決まる。秒は、クリップの長さに合わせて書きかえる）
- **寄りで終わるクリップ（必ずこの形）**：
```
TIMING IS CRITICAL: by [1.5] s the camera has ALREADY ARRIVED close to [主役のどこ]. 0.0-0.3 s: it starts moving at once. 0.3-[1.3] s: it RUSHES toward [主役のどこ] in one fast arc with strong motion blur, swinging about [35] degrees around [主役] and dropping to [終わりのカメラの高さ]; at [1.5] s [主役のどこ] already fills most of the frame. [1.5]-[5.0] s: the camera stays this close and only drifts slowly, a slight orbit and a very small push-in, never holding still. Do NOT spread the approach evenly over the clip; the big move is finished by [1.5] s. At the end [主役のどこ] is in the middle of the frame and fills about [two thirds] of its width.
```
  **「0.4〜1.6秒が一番速い」とだけ書くと、寄りはクリップの全体にならされる**（5秒の全体に広がり、大写しになるのが3.5〜4秒になった）。「◯秒までに、もう着いている。その後は、近くでゆっくり流れるだけ。ならさない」と書くと直った。着く秒は、クリップの長さの3割まで（5秒なら1.5秒・3秒なら0.9〜1.0秒）。
- 引きのまま回りこむ・下がる・上がる：`It [swings in one arc around / drops beside / rises over] [SUBJECT] to [終わりのカメラの高さと向き]. From the very first frame the camera is already travelling: it never waits and no frame repeats. 0.0-0.3 s: starts slowly, already moving. 0.3-[1.6] s: the fastest part, with motion blur, the horizon rolling from one tilt to the other. [1.6]-[3.0] s: eases out and keeps drifting in the same direction, never holding still.`
- 速さの文を強めるだけ（`wide fast arc` など）では、止まったコマが出た。秒で書く。

**ピント**
- 寄りで終わる：`the focus stays locked on [主役のどこ]. For the first [second] the [場所] is still sharp; as the camera gets close, everything behind [主役] melts into a strong soft blur and stays blurred to the last frame.`
- 寄りで始まって寄りで終わる：`[主役] stays razor sharp; the background stays a soft blur from the first frame to the last.`
- 引きで終わる：`deep focus for the whole shot: [主役] and everything behind stay razor sharp from the first frame to the last; no background blur, no rack focus.`

**主役が、動かない物の時に足す**（FIXED THINGS の後ろ）
```
The [商品] and everything else in the scene are FIXED TO THE FLOOR: nothing moves, slides, turns or changes size. ONLY THE CAMERA MOVES. The [商品] stays glued to the same spot of the [床の物] from the first frame to the last: the [床の物] around the [商品] never slips relative to the [商品], and the [商品] never drifts across it.
```
模様のある商品には、さらに：`The [商品] is rigid: [行の数] across and [列の数] along it, every [模様1個] stays in its own place in the straight grid, the number of rows and columns never changes, none appears, disappears, merges, splits or slides.`
**画面の外へ出て行く、奥行きのある物がある時に足す**
```
The [OBJECT] is a RIGID SOLID BOX standing on the floor: it never bends, stretches, squashes, melts, shrinks or morphs; its parts keep the same proportions in every frame. As the camera [drops and turns], the [OBJECT] simply slides out past the [left / right] edge of the frame by pure perspective, as a rigid object, at a steady rate; it NEVER GETS SHORTER: it is carried out of the picture THROUGH THE [LEFT / RIGHT] EDGE, cut off by the frame edge, not compressed. The camera sinks below the height of [その物の上の面], so the top is hidden behind its own front edge.
```
（この文だけでは、ゆがみは短くなるが、消えなかった。構図とカメラで手を打つ＝14-12 の 4。）
- エフェクトのあるクリップは、6章の文を後ろに足す（そのまま使う）。書かない言い方：`[手前の物] sweeps across the frame`（手前の物がレンズの前をぼけて横切った）・`round bokeh highlights`（寄りの終わりで外した）。
- 全文の例：`$M/指示の例/人_動画_速い寄り.txt`・`物_動画.txt`（**試験の場面の言葉が入っている。型だけ見る**）。
- 打ち方：`$T/clip.sh <作業フォルダ> <名前> <始めの絵> <終わりの絵> <秒 3|4|5> <指示の文.txt> <クレジットの上限>`（3秒 3.8・4秒 5.0・5秒 6.3 クレジット。`clips/credits.log` に足して、上限をこえる時は作らない）。**人が大きく動いて寄るクリップは5秒・物に寄るだけのクリップは3秒**が、試験で通った長さ。場面の長さに合わせる時の速さは、4章③のまま（0.95〜1.15倍）。

### 14-11. クリップを測る（通す線）
| 見る事 | 道具 | 通す線 |
|---|---|---|
| **動かないはずの物が、場所に対して動いていないか（道A）** | `$PY $T/check_rigid_room.py <クリップ> --scene work/scene.json --cam S --label work/startview_label.png --info work/startview.json --sheet out.jpg --json out.json` | **速い動きが始まる前（始めの1秒）**：全部の点の、コマごとのまん中の値の最大 **幅の1%以下**。物ごとの最大 **2%以下**（こえた物は、画面のはしから出る直前だけか、消える・すべるが見えるかを、コマで見て書く） |
| **主役の物が、床に対してすべっていないか（道B）** | `$PY $T/lock_slide.py <クリップ> --bg <地の色> --tol 17 --json out.json --sheet out.jpg` | 一番大きいすべり **幅の2%以下** |
| 目印が消えない・別の物に変わらない | `$PY $T/check_clip_marks.py <クリップ> --marks work/marks_start.json --sheet out.jpg --json out.json` | 背景にピントが合っている間、全部の目印が通る。外れは「主役の後ろへ入っただけ」かをコマで見て書く |
| 模様の数・かたさ（模様のある商品） | `$PY $T/check_pattern_clip.py <クリップ> --bg … --fg … --grid 行x列`・`$PY $T/check_rigid_clip.py <クリップ> --bg … --fg …` | 数えられる間の全コマで、行×列が表と同じ・あな 0。数えられる間が 0.5秒より長い。かたさ 0.60以上 |
| 奥行きのある物の輪かく | `$PY $T/lock_shape.py <クリップ> --poly "<始めの絵でのわく>" --polysize 幅,高さ --name ◯◯ --sheet out.jpg` | **数だけでは、良し悪しを分けられなかった。** `--sheet` で輪かくを目で見る：ちぢむ・のびる・別の形になる、が無い。クリップの後ろ半分に「とび」が無い |
| 動き | `$PY $T/measure_look.py out.json <クリップ>` | `flow_med` 7以上 または `flow_p90` 40以上。`still_frac` 0.05まで。`jumps` 0 |
| **寄りの速さ**（寄りで終わるクリップ） | 同上の `t_half`（寄りが半分まで進む秒）・`peak` | **`t_half` がクリップの長さの3割まで**（5秒なら1.5秒まで。直す前 2.33秒 → 直した後 1.0秒）。`peak` 80以上 |
| 終わりのぼけ | `$PY $T/bokeh.py a=<クリップ>@<最後の0.1秒前>` | 14-9 と同じ |
| 目で見る | 0.5秒おきのコマ：`$PY $T/make_frames2.py <クリップ> out.jpg <始めの絵> <下絵> <ぼかす前> <ぼかした後>`。速い所は1秒8コマ | 物がすべる・ゆがむ・消える・増える、が無い。同じ人・4番の質感。写っていない物が出ない |
- **道Aの「まん中の値 1%以下」と、寄りの `peak` 80以上は、仮の線**（通ったクリップ2本と、ずれていた前のクリップ1本の数から置いた。始めの1秒のまん中の値は、ずれていたクリップでも 0.29% で、この数だけでは分けられなかった。分けたのは、上位1割の最大〈通った物 0.56%・ずれた物 3.43%〉と、コマを並べた目）。ゆっくり動くクリップでは、**上位1割の最大 1%以下**も見る。
- **機械で測れない間がある。** 速く寄って背景がぼけた後は、点が追えない（承認された速い寄りのクリップを測ると、測れたのは1.2秒まで、その間の物ごとの最大は 3.7%・まん中の値は 0.69% と出た。速く動く間は、数が大きく出る）。だから、**機械の線は「速い動きが始まる前」に当て、その後は、コマを並べて目で見る。** 報告に、何秒まで測れたかを書く。
- 道具が「作り直す」と出したのに通す時は、訳を書く（例：主役が絵からはみ出す大写しを、道具が外れと数えた）。
- 並べた絵の例：`$M/人の場面_コマの並び.jpg`・`$M/物の場面_コマの並び.jpg`。

### 14-12. 外れた時の直し方（上から順に。1つ直したら、測り直す）
1. **終わりの絵のずれ（14-8）**：仕上げだけ、やり直す（同じ文で2枚。2回まで）→ 下絵に無い物を足された時は、F の `Do NOT add …` に、その物の名前を足す → それでも外れる時は、終わりのカメラを、穴の小さい向きへ直す。
2. **背景だけ、始めのカメラのまま写された**：渡した場所の見本が、始めと同じ向きになっていないかを見る。別の向きの見本に替えるか、外す。
3. **物が床をすべる・背景が流れる（14-11）**：終わりの絵を見直す（1・2）。クリップの文だけを強めても直らない。終わりの絵が通っているなら、クリップを作り直す（FIXED THINGS・BACKGROUND の文が入っているか）。
4. **奥行きのある大きい物が、途中でゆがむ・ちぢむ**：① 立て板で動かしていたら、箱にする（14-6 の B2）② 終わりの絵に、見えるはずのない面が描かれていないかを見る（14-8）③ **始めの絵の構図で、その物を動きの道から外す**（始めの絵から作り直す。一番効く）④ カメラを「先に寄って、後で下がる」の2段にする（その物が画面から出てから、高さを変える）⑤ それでもだめなら、**途中の絵を1枚足して、2本つなぐ**（道A：`warp.py … --t 0.5` で、まん中のカメラの下絵を出して仕上げる。つなぐのは `$PY $T/join_clips.py a.mp4 b.mp4 out.mp4`）。**④⑤は、まだ試していない。**
5. **高さのある模様が、作りすぎた形になる**：形の見本を渡し、F5 を入れる。下絵の模様を、見本に近い大きさ・数で出し直す。
6. **模様の数が外れる**：2枚ずつ出し直す。数の図を渡しているか・商品の表の数が絵ごとに同じかを見る。余分の1個だけを、指示や機械で消そうとしない（消えない・あとが残る）。3回外れたら 14-14。
7. **寄りが遅い（`t_half` が3割より後）**：14-10 の「寄りで終わるクリップ」の形になっているかを見る。絵は直さない。
8. **人が写真・人形に寄る**：C の直し方の文で、人物だけ直す（その後、背景が変わっていない事を見る）。
9. **止まって見える**：12-4 の順（絵 → クリップ → 編集のズームは最後）。
10. **寄りで出た穴のうめ方がおかしい**：F1 を所ごとに書き直す。広い時は、別の向きの場所の見本を渡す。

### 14-13. 透けて中を見せる（6章⑪a に足す。⑪e とする。人や体の一部・物をまるごと透かす時は、こちらを使う。物の一部だけを透かす時は、⑪a のまま）
見せ方は「外の皮が、ガラスの殻になる」。わく・窓・切り口は付けない。見本：`$M/参考_透ける_頭.png`・`$M/本物_透ける_腕.png`。
絵の指示に足す文（始めの絵＝外の寄りの絵を1枚目に渡して、EDIT で作る。外の形・位置は変えない）：
```
SEE-THROUGH (part of the 3D scene, not an overlay): the [skin / outer surface] of [the whole PART] has turned into a thin, perfectly clear glass-like shell. The outer silhouette of [PART] is exactly unchanged, and the shell catches a few soft white highlights along [its top edge]. There is no cut edge, no frame, no window, no hole. Through the shell the inside is fully visible, bright and evenly lit, as bright and as saturated as the world around it: (1) [中の物1], [色]; (2) [中の物2], [色]; (3) [中の物3], [色]; (4) [中の物4], [色]. Clean like a plastic classroom teaching model, a medical education 3D diagram; nothing is wet, nothing is injured. Where [PART] ends, the normal surface continues; the change from glass to normal is a short soft fade. The background is the SAME place, strongly out of focus (it is not replaced by a plain color and it is not darkened).
```
動画の指示に足す文：
```
SEE-THROUGH, in order: (1) During the last 0.1 s of the fast camera move (at about [0.65] s), the [skin / outer surface] of [the whole PART] turns into a thin clear glass-like shell, all at once, within 3 frames: not a fade spreading from a spot, not a window, no cut edge. The outer shape stays, with soft highlights on the glass. [変わらない物] stay normal. (2) At about [0.9] s [次のエフェクト]. The see-through happens once and stays to the end; it stays attached to [PART] as the camera moves.
```
- 中の物は4種類まで。色は、はっきり分ける。話している物だけ、後からエフェクトで光らせる（6章）。
- 中は、まわりと同じか、少し明るく。暗い背景・白くぼけた丸い窓は使わない。背景は、その場のままぼかす（説明だけの場面は、無地でもよい）。
- 透ける直前に、速いカメラを入れる（0.2〜0.4秒）。透けきった0.1〜0.3秒後に、次のエフェクト。
- 検品：前後を1秒30コマで並べ、透けはじめから出きるまで0.25秒以内。わく・窓・切り口が無い。

### 14-14. 逃げ道（使ったら、報告に書く）
| 困った事 | 逃げ道 |
|---|---|
| 模様の数が、3回（6枚）続けて外れた | その絵だけ、高さの絵から出した下絵を仕上げる（`make_relief.py`・`scene3d_v3.py`。やり方は `（作業フォルダ：アプリには同梱していない見本）`）。質感がほかの絵と少し違うので、その商品の「通った始めの絵」として使い回し、別の絵と混ぜる場面を減らす |
| 場所の線が写っていない・箱で書けない場所（道Aのカメラが出ない） | 床の上の、大きさの分かる四角の4点から出す（未確認）。出ない時は、その場面は、カメラをあまり動かさない構図（止まり気味＋人の動き）にして、始めの絵を EDIT して終わりの絵を作る（4章②2 の形）。寄りは、編集ではなく、次の場面を切って作る |
| 人に寄る場面で、人の借り元の絵が無い | A・C・E の文で、寄りの人の絵を1枚ふつうに描いて、借り元にする |
| 大きい物のゆがみが、14-12 の 4 を全部やっても残る | その物が写らない向きから始まる構図に、場面を作り直す |
| 穴が30%より小さくならない | 終わりのカメラを近づける（動きを小さくする）か、途中の絵を足して2本にする |

### 14-15. やらない事（試して、だめだった）
| した事 | どうなった |
|---|---|
| 始めの絵と終わりの絵を、別々に描いた（場所の表・見本・灰色の下絵があっても） | 2枚が同じ世界にならず、クリップの道具が、物をすべらせて・ゆがめて・消してつないだ |
| 位置を、言葉だけ・灰色の箱の下絵だけで伝えた | 言葉は守られない。灰色の下絵は幅の5〜13%ずれる |
| 終わりの絵に、始めと同じ向きの場所の見本を渡した | 背景だけ、始めのカメラのまま写された（主役の物が床をすべった） |
| 絵を描かせる時に決めたカメラの数で、下絵を作った | 全部ずれた。カメラは、描かれた絵から出す |
| 奥行きのある物を、1枚の板として動かした | 低いカメラから見えないはずの面が描かれ、途中でゆがんだ |
| 角の位置だけで、終わりの絵を通した | 角は合っていたのに、見えるはずのない面が描かれていた |
| 高さのある模様の低い角度の絵を、形の見本なしで仕上げた | 形を作りすぎた（大きい山が少しだけ） |
| 「◯〜◯秒が一番速い」とだけ書いて寄らせた | 寄りが、クリップの全体にならされた |
| ぼかした絵で確かめた・寄りの絵は「ゆるく」見た | ずれがぼけにかくれた。確かめは、ぼかす前に、同じ線で |
| 人の場面は、線をゆるくした | ずれの正体は同じ。ばれにくいだけ |
| 全身の切りぬきを、そのまま顔の寄りの下絵に使った | 使えない形になる。背景だけ動かし、人は借り元から大まかに置く |
| 人だけを直す文に「◯度回す」と強く書いた | 回しすぎ・大きくなった。「小さな変化・輪かくはほぼ同じ」と書く |
| 場所の見本を、位置のちがう物ごと、人の後ろにはめた | その物が2個になった（`--erase` で先に消す） |
| `style_確定_2-2.png` を見本に渡した・3章の STYLE BASE を使った | なめらかで全部にピントの、人形に寄った絵に戻る |
| 人物の文に `faint surface texture`・`realistic face shape`・`a few simple modeled folds` と書いた | 写真の人に寄った（4番の文を使う） |

### 14-16. 速く作るコツ
1. **通った絵を使い回す**：通った始めの絵（とくに、模様の数が通った絵）・場所の見本・人の借り元の絵は、同じ商品・同じ場所のほかの場面、ほかの動画でも使う。行って戻る（14-3 ⑦）で、1組の絵を2本のクリップに使う。
2. **道具と数を、写して使う**：`$M/数の例_人/`・`$M/数の例_物/` の json を写して、画素と名前だけ書きかえる。カメラは 14-7 の 5 の数から始める。同じ始めの絵を使う場面は、`calib`・`scene`／`world` を1回作れば、終わりのカメラを足すだけ。
3. **読む物をしぼる**：この章と `tools/README.md` だけで作る。試験のフォルダの `how.md` は、道具が思ったとおりに動かない時だけ読む。
4. **3秒で試してから、長くする**：新しい型のクリップは、まず3秒（3.8クレジット）で、ずれと動きを測る。通ったら、5秒で本番。
5. 下絵は0円。迷ったら、カメラの案を並べて出す。絵（Codex）は、同じ文で2枚同時。場面どうしで待ちが重ならないよう、絵を待つ間に、次の場面の数を読む。
6. 1場面の手作業（画素を読む・わくを書く）は10〜15分かかった。**始めの絵の種類を、1つの場所につき2〜3枚にしぼる**と、全体が速い。

### 14-17. 完成の動画で守る数（12-1 の5つに足す。書き出しの後に測る。外れたら、直してから出す）
測り方：`$PY $T/measure_look.py out.json <完成の mp4>`・`$PY $T/skin_bokeh.py out.json 名前=<完成の mp4>`
| 測る物（道具の出す名前） | 決まり | 本物11本 | 前の作り方の3本 |
|---|---|---|---|
| 画面の動きの速さ・中央（`flow_med`） | 幅の12%/秒以上 | 18〜37 | 3.5〜5.1 |
| ゆっくりなコマの割合（`slow_frac`） | 25%まで | 2〜14% | 49〜60% |
| 止まりの最長（`still_max_s`） | 0.5秒まで | 0〜0.8秒 | 1.7〜7.0秒 |
| 物・人の動き・中央（`obj_p90_med`） | 幅の25%/秒以上 | 36〜63 | 5.9〜7.9 |
| 速い動きの回数（`fast_bursts_per_10s`） | 10秒に4回以上 | 5.0〜12.0 | 1.2〜2.5 |
| 背景がぼけたコマの割合（`soft_frames_30`） | 15%以上 | 5〜33% | 0〜1% |
| 彩度の平均（`tex_sat`） | 0.30〜0.45 | 0.21〜0.49 | 0.29〜0.35 |
- この7つの線は、3秒のクリップ3本と、本物11本から決めた。**1本通しでは、まだ当てていない。頭の10秒で1度測る。** 線に届かない物が出たら、数と一緒に報告する（線の方が合っていない事もある）。
- コマ割りの表で数える：目の高さ・水平の絵が、全体の半分まで。人の出る場面の半分以上で、体の形が変わる動きを書く。
- 報告に書く：12-1 の5つ・この7つ・クリップごとの 14-8 と 14-11 の数（通った数・外れた数を、道具の言葉のまま）・何秒まで機械で測れたか・逃げ道を使った絵・再生して見たか。**外れている物を、外れたまま「完成」と言わない。**
- **終わりの長さ（2026-10-12 運営者。スケルトンの最後の「ください」が途中で切れた）**：完成品の尺は、**声の最後の字の終わり（声の wav の末尾の無音を除いた所）＋0.5秒以上**。組む前に、声の wav の長さと場面の表の最後の終わりを機械で比べ（`ffprobe -show_entries format=duration`）、足りなければ最後の場面を延ばす（声に合わせて尺を切らない。止め絵で埋めない）。組んだ後に、完成品の最後の6秒を whisper で起こして最後の1文が全部あるかと、`ffmpeg -af areverse,silencedetect` で末尾に0.3秒以上の声の無い所があるかを見る。報告に「声の終わり◯秒／尺◯秒」を書く

### 14-18. 前の章とぶつかる所（**全部、14章が勝つ**。古い文は消していない）
| 前の章 | 前の決まり | 14章では |
|---|---|---|
| 3章 見本の絵・STYLE BASE | `style_確定_2-2.png` と `実物のコマ_人物.png` を渡す。全部にピント・なめらかな肌 | 14-4 の見本・14-5 の A と C。ピントは絵ごと（確かめる絵は全部にピント、ぼけは後から機械で） |
| 3章 書いてはいけない言葉 | そのまま残す | 足す：`faint surface texture`・`realistic face shape`・`flat even light`・`eye-level`・（動画の指示で）`round bokeh highlights` |
| 3章 場所 | 物を8〜10個 | 引きは5〜8個。葉や床の細かい模様は書かない |
| 4章②1・2・3 | 基準の絵を元に「ここだけ変える」。外から写す向きは変えない | 同じカメラのまま中だけ変える絵（前と後・透ける）は、今までどおり EDIT。**カメラが動くクリップの終わりの絵は、14-6 の下絵から**。向きは変えてよい |
| 4章②7 | 中を見せる絵は、明るい地に主役1つ。窓は幅の3〜4割 | 14-13（ガラスの殻。背景はその場のままぼかす） |
| 4章③ | 始めと終わりは、大きさか高さが違う2枚。作る秒数は3秒か4秒 | 終わりの絵は、始めの絵から作る（14-2）。高さか向きを必ず変え、寄りは6倍以上。人が動いて寄るクリップは5秒も使う |
| 4章③ 毎回付ける文・7章 CAMERA の文 | 2つを続けて書く | 14-10 の形（FIXED THINGS・ACTION・CAMERA・LENS・FOCUS・BACKGROUND）。7章のカメラの種類の表と、山の形・型は、そのまま使う |
| 7章「速い動きは、クリップの頭の0.3秒に置く」 | 頭の0.3秒 | 0.3秒までに動きだし、**クリップの長さの3割までに着く**（14-10）。頭の0.3秒で終える形は、前のクリップからつながって、もう動いている時だけ |
| 6章⑪a・⑪入る | 表面が、ふちからぼけて透ける | 人や体の一部・物をまるごと透かす時は 14-13（一度に、3コマで）。物の一部だけは ⑪a のまま |
| 10章 2 | 2枚目からは、1枚目を見本に渡して作る | 場所の見本（14-3 ⑤）を先に作り、14-4 の表で渡す |
| 11-1 | 場所の基準の絵を、向きの数だけ。人は「ここに人を足す」で作る。寄りは、基準の絵を切り出して背景にする | 場所の見本は「渡す見本」。**始めの絵は、人と場所を1枚の絵として描く。** 寄りの背景は、下絵（始めの絵を動かした物）から。切り出して貼らない。場所の物の並びを1つの文に決める事（場所の表）は、そのまま |
| 11-2 | 体の向きが大きく変わる動きは、1本でやらせない | 立つ⇄すわる⇄寝る・物をまたぐは、今までどおり切る。**同じ所に立ったまま、上半身が大きく動く動き**（のけぞる・かがむ・手を顔へ・ふり向く）は、14-10 の ACTION の形で、1本でやらせる。足は同じ所。手は、始めの絵でその形に近くしておく |
| 11-3 | 人にも、小さい動きを1つ | 人の出る場面の半分以上で、体の形が変わる動き。動かせない場面だけ、小さい動き＋大きいカメラ |
| 12-1 | 守る数5つ | そのまま。14-17 の7つを足す。絵の枚数の数え方：場所の見本・下絵・数の図・ぼかす前の絵は数えない |
| 12-3「1つの場所につき、カメラの向きを3つ用意する」 | 場所の基準の絵を3つの向きで | 場所の見本は2〜3枚作る（渡す見本）。**クリップの終わりの向きは、始めの絵から下絵で出す**ので、向きの数は3つに限らない。終わりの絵に、始めと同じ向きの見本を渡さない。「同じ動きを2場面続けない」「始めと終わりで大きさか向きを変える」は、そのまま |
| 12-2 | 前の終わりの絵＝次の始めの絵 | そのまま。加えて、つながりの組の中の絵は、全部、組の最初の絵から作る（14-3 ⑦）。次の始めの絵にする時、下絵の元は、ぼかす前の絵 |

## 15. 物のバグを出さない・カメラを本物に寄せる（**ここは、ほかの全部の章より先**。この章で作った見本：`（作業フォルダ：アプリには同梱していない見本）`（`コマ割り.md`・`out/frames.jpg`。**その台本の言葉が入っている。表の形と、バグの消し方の型だけ見る**）。この章を足す前の決まりの控え：`ec-ad-ops/references/_archive/動画ルール_20261010_ふくらはぎ4本の時点/`）

### 15-0. 作る順（絵コンテのページは、言われた時だけ。言われなければ、この順で一発で作る）
**作る長さ：指定が無ければ、台本の最後まで。**（短く作るのは、運営者 が「最初の◯秒だけ」と言った時だけ。どの映像の型でも同じ）
1. **台本を受け取る**（文言は1字も変えない）。声を録り、言葉ごとの時刻を出す（4章①・11-5。話し手が2人以上なら13章）
2. **`コマ割り.md` を書く**（絵より先）。列：#／秒／声の言葉／場所／始めの絵→終わりの絵／ゆっくりの流れの向き／速い動き（種類・どの語の切れ目・何秒に着く）／前の場面とのつなぎ（カメラでつなぐ・切る）／エフェクト／効果音／**人のほかに写る物（全部）**
   - 1場面＝声の1〜2句。**言葉が言っている物を、その時に見せる**（言っていない物を見せない）。困り事の言葉の所で、その場所に赤い光＋音。**「その場所」は、絵に写っている物の名前1つで書く（16-1。「痛い所」「◯◯の所」と書かない）**
   - 「人のほかに写る物」の欄に書けない物は、絵に入れない（15-1）。だれも触らない物の動きは、ここで音だけにするか、切ると決める
3. **数える**（外れたら、表を直してから絵に進む）：速い動き 10秒に1〜2回・同じ種類が続かない・速い場面が2つ続かない／カメラでつなぐ所 30秒で4か所以上／止めの場面 0／強い語・エフェクトの上に速い動きが無い／場所も時間も変わらないのに切っている所 0
4. **絵**（14-4・14-5 の見本と文。Codex）。1つの場所の最初の絵で人物と物を決め、あとは、その絵から作る。**15-2 で確かめてから**、クリップへ
5. **クリップ**（14-10 の形＋15-3 の文）。新しい型の動きは、3秒で試す
6. **15-4 で、物のバグを数える**。1つでもあるクリップは使わない
7. **組む**（字幕・効果音・曲。曲は小さく1曲を通す＝11-4 と sound-rules.md）。エフェクトの出る時刻を、声の言葉に合わせる（7章の末「編集での合わせ方」）。**編集で重ねる円・光・輪は、16章の順（組んだ後のコマで測る → 確かめの絵を見る → `pointer_check.py --gate` が通る → 書き出す）**
8. **完成品を1秒6コマで全部並べて、目で見る**（`out/frames.jpg`）。15-4 をもう1度・字幕が台本と同じか・絵に文字が無いか・同じ人か
9. **報告**：15-7 の形

### 15-1. 物のバグは、3つの元から出る（元を消す。出てから直さない）
| 出たバグ | 元 | 決まり |
|---|---|---|
| だれも触っていない物が、勝手に動く・たおれる・向きが変わる | **始めの絵と終わりの絵で、その物の位置・形が違う**（別々に描いた／終わりの絵で「動いた後」を描いた）。動画の道具は、訳を作れないまま、2枚の間をうめる | **人とカメラのほかは、始めと終わりで1画素も変えない。** 終わりの絵は、始めの絵の EDIT で作り、`Change ONLY:` に書くのは、人の体の形・顔・エフェクトだけ。物を動かしたい時は、**だれが・どの手で・何秒に触るか**を ACTION に書ける時だけ。書けない動き（ドアが閉まる・物がたおれる・物が落ちる）は、絵にしない＝**音だけにする**か、**動いた後の絵に切る** |
| 体に付いている物（かばん・ひも・めがね・持ち物）が、体をすりぬける・落ちる・消える | 体が動くと、付いている物を、道具が体と別に動かす | **台本の言葉に出てこない持ち物・身に着ける物は、絵に入れない**（かばん・上着・ぼうし・首から下げる物）。要る時は、①体の動きが小さい場面だけに出す ②動画の指示に ATTACHED の文（15-3）を入れる ③はずす・置く動きは見せず、次の場面を「もう置いてある絵」から始める |
| 手・うで・足が増える。持ち主の分からない手が出る | 手が画面のはしから入る／手の持ち主のうでが写っていない／始めの絵に無い手を、途中で出させた | **手が何かに触る場面は、始めの絵で、もう触っている**（11-2）。その手は、**ひじより上まで、同じ人の体につながって写る**構図にする。手だけの寄りは、手首から先だけを写さず、うでが画面のはしまで続く向きを1つに決めて、始めと終わりで同じにする。動画の指示に HANDS の文（15-3）を入れる。途中で、新しい手を画面に入れない |

| 同じ物が2つになる（手の中の物と、置いてある物） | 始めの絵と終わりの絵で、その物の居場所が違う | その物は、動画の中で1つだけ。居場所は、始めの絵で、もう終わりの所にある（手で持って、もう半分入っている、など） |
| 物から、それを持つ人へ速く引く時、体より先に、うでだけが画面に入る | 始めの絵（物の寄り）に、持ち主の手・うでが写っていない | 本人のうでが、体につながって入るなら、バグに数えない。ただし、始めの絵（物の寄り）に、**もう、その手と手首が写っている**構図を先に試す。だめなら、切ってつなぐ |

**小道具を減らす**：人の手足が届く所に置く、動かない小さい物（靴・コップ・リモコン・クッション）は、**台本の言葉が指す物だけ**。飾りで置かない。置いた物は、15-3 の FIXED の文に、名前で全部書く。

### 15-2. 絵を作る時に、もう確かめる（クリップを打つ前）
始めの絵と終わりの絵を並べて、次を1つずつ見る。1つでも外れたら、絵を直す（クリップは打たない）。
1. 人のほかの物：数・位置・向き・形が、2枚で同じか
2. 手の数：画面の中の手は、何本か。全部、持ち主の体につながっているか。2枚で同じ本数か
3. 身に着けている物・持っている物：2枚で同じ所に付いているか。台本に無い物を着けていないか
4. 人の位置：足・こし（座っている時）が、2枚で同じ所か（歩く場面のほか）

### 15-3. 動画の指示に、毎回足す文（14-10 の文の、FIXED THINGS の後ろ）
```
PHYSICS: [人のほかの物を、名前で全部] do not move at all: nobody touches them, so they stay exactly where they are, in the same pose, from the first frame to the last. Nothing falls, tips over, rolls, slides, opens or closes by itself. HANDS: [the person] has exactly two hands and two arms; the [left] hand [どこにある], the [right] hand [どこにある]. No other hand, arm, finger or person ever enters the frame. Solid things never pass through each other.
```
身に着けている物・持っている物がある時に足す：
```
ATTACHED: the [物] stays [on her left shoulder / in his right hand] the whole time, attached at the same point; it moves only together with the body, never slips off, never passes through the body, never floats.
```
人が物に触って動かす時だけ（PHYSICS の「do not move」から、その物を外して）：
```
CONTACT: at about [1.2] s [her right hand] takes hold of [物]; the [物] moves only while the hand is holding it, and stops the moment the hand lets go.
```

### 15-4. クリップができたら、物のバグを数える（1秒6コマで見る。**1つでもあったら、そのクリップは使わない**）
見る物：①触っていない物が動いた ②物が体や物をすりぬけた ③手・うで・足・指の数が変わった ④物が増えた・消えた・別の物になった ⑤人が、足を動かさずにすべった。
- **作り直しの回数が切れても、バグのあるクリップを出さない。** 直す順：(a) 絵を 15-2 で見直す → (b) その物を絵から外す・構図を寄せて画面の外に出す → (c) 動きを小さくする（体の形の変化を、1つにする）→ (d) 動きの前後で切る（2枚の止めに近いクリップにする）
- 報告に、クリップごとの①〜⑤の数（0である事）を書く。「弱い場面」に、物のバグを残したまま書いて出さない

### 15-5. カメラ（7章の実物の数に寄せる。ただし「動きすぎて、情報が入ってこない」と言われた形にしない）
実物は「いつも流れている・速い動きは短く、言葉の切れ目にだけ・大事な言葉の間は、ゆっくり」。前に「動きすぎ」と言われた版は、大事な言葉の間にも大きく動かしていた。前に「見やすい」と言われた版は、止めが多く、切ってつないでいた。**両方を取る形**：
1. **完全に止まったカメラの場面を作らない。** どの場面も、ゆっくり流れる（寄る・引く・横へ。3秒で画面の5〜12%）。同じ場面で、寄って→引いて、をくり返さない。流れの向きは、次の場面と変える
2. **速い動きは、言葉の切れ目・つなぎの語の上だけ。0.2〜0.5秒で着く。** 強い語の0.1〜0.2秒前に着いて、その後はゆっくり流れるだけ（7章「山の形」）。**強い語・エフェクトの間に、大きく動かさない**
3. **速い動きの数：10秒に1〜2回**（30秒で4〜6回）。種類を変える（速く寄る／速く引く／回りこむ／下がる・上がる／中へ入る／追う）。同じ種類を続けない。続けて2場面、速い動きを入れない
4. **同じ場所・同じ主役の間は、切らずに、速いカメラでつなぐ**（人の全身 → その人の体の一部、外 → 中、物 → それを持つ人）。切るのは、場所が変わる・時間が飛ぶ・中から外へ戻る時（12-2）。**30秒で、カメラでつなぐ所を4か所以上**
5. **書き出しの1コマ目は、寄りの絵で、もう動いている**
6. **カメラの高さ・向きを散らす**：目の高さ・水平の絵は、全体の半分まで（14-17）。低い所から見上げる・上から見下ろす・ななめを混ぜる。手持ちの広角で、主役に近い
7. **物の多い場所では、大きく動かさない**（物がゆがむ）。速く大きい動きは、①無地の背景の説明の場面 ②14章の固定のやり方で終わりの絵を作った場面 ③物を3つまでに減らした構図、でだけ使う。それ以外の場面は、1 のゆっくりの流れだけにする
8. **ゆっくりの流れ（1.2倍まで）の終わりの絵は、始めの絵の切り出しだけでよい**（描き直さないので、物が1画素も変わらない。人の形を変える時だけ、切り出しを EDIT）。平らなかべ・無地の場面は、もっと大きい寄りでも、切り出しを下絵にして仕上げさせれば、位置が合った。**カメラの高さ・向きが変わる動きは、14-6 の下絵から**
9. **終わりの絵に、エフェクト（光・透ける）を入れると、秒の指示より早く出る**（クリップの頭の0.6秒で光った）。声の言葉に合わせたいエフェクトは、①「出る前」のクリップと「出た後」のクリップに分ける ②光・輪・線は、編集の道具で重ねる、のどちらかにする。**②の位置は、16章で測って確かめる（止め絵の上で座標を読まない）**
10. **人の場面で「速く寄って着く」は、14-10 の文を入れても、ゆっくりの寄りにならされる事がある**（3回続けて、ならされた）。2回試してだめなら、逃げ道：**編集で0.2秒だけ速く寄せ、寄った先を、次のクリップの始めの絵の位置に合わせてつなぐ**。これは速い動きに数える（編集のズームの「1割まで」には数えない。ただし、速い動きの回数まで）
11. **カメラでつなぐ時、前のクリップは、終わりのコマまで使う**（途中で切ると、つなぎ目でとぶ）。だから、前のクリップの動きの秒は、**クリップの後ろに合わせて**書く（場面の長さより長いクリップは、頭を切って、後ろを残す）
12. **速い動きを入れない場面の決め方**：物が多い場所・人が物に触っている最中・強い語が続く所。迷ったら、入れない（ゆっくりの流れだけにする）

### 15-6. 前の決まりとぶつかる所（15章が勝つ）
| 前 | 15章では |
|---|---|
| 絵コンテの共通の決まり「カメラを動かす場面は、3分の1まで」 | 「**速く大きく**動かす場面」が3分の1まで。残りも、止めずに、ゆっくり流す |
| 絵コンテ「動きの前と後を見せたい場面は、2枚」 | 2枚で変えてよいのは、人の体の形・顔・エフェクトだけ（15-1） |
| 12-5・各依頼の「1場面の作り直しは◯回まで」 | 回数が切れたら、15-4 の (b)〜(d) で形を変える。バグのまま出さない |
| 12-1「切る所は、場面の数の3割まで」 | **場所か時間が変わる所・中から外へ戻る所は、切ってよい（数に入れない）。それ以外で切った所が 0** である事を守る。場所の多い台本では、切る所が5割になってよい |
| 12-1「1場面の平均 2.8〜3.2秒」 | 2.2〜3.2秒（声の1〜2句＝1場面を先に守る） |
| 12-1「絵の枚数は、場面の数の1.8倍以上」 | 1.5倍以上。切り出しで作った終わりの絵も、1枚に数える。**始めと終わりが同じ絵のクリップを作らない**、は、そのまま |
| 12-1「編集で足した寄り・引きは、1割まで」 | そのまま。15-5 の 10 の「0.2秒の速い寄り」は、別に数える |
| 14-17 `flow_med`・`slow_frac`・`fast_bursts`・`obj_p90_med` | **目安として測って、報告に書くだけ。合わせに行かない**（承認された版は `flow_med` 3.8・`fast_bursts` 2.4 で、線に届いていない）。15-5 の 2・7 を先に守る。`still_max_s` 0.5秒まで、は守る |
| 14-8・14-11 の機械の確かめ | カメラの高さ・向きが変わるクリップ（14-6 の下絵を使った物）にだけ当てる。切り出しで作ったゆっくりの流れには、当てなくてよい（15-2 と 15-4 の目で見る確かめは、全部に当てる） |

### 15-7. 報告の形（これだけ書く）
完成品の場所・長さ・場面数／カメラ：速い動きの回数と種類（場面の番号で）・カメラでつなぐ所の数・止めの場面の数・止まりの最長／物のバグ：15-4 の①〜⑤の数（残っていたら、どの場面の何か）・判断の分かれた所／**指す円：16-6 の数（◯個・3コマとも はい ◯個・直した回数・やめた円・完成品でも見たか）**／弱いと思う場面／使ったクレジット／決まりで合わなかった所／確かめていない事（**再生して見たか・音を耳で聞いたか**を必ず書く）／**声の終わり◯秒・尺◯秒（尺＝声の終わり＋0.5秒以上。2026-10-12）**。

## 16. 指す円・光・輪を、指す物の真上に置く（**ここは、ほかの全部の章より先**。この章を足す前の控え：同じ場所の `v1-zackdfilms-video.md.bak-20261012pointer`）

編集で重ねる物（円・輪・光・丸・矢印・線・ラベルの先。音と一緒に「ここ」と指す物）の全部に当てる。どの商品・どの体の部分・どの物でも同じ。例は ◯◯ で書く。

### 16-0. 何が起きていたか（1本を、コマで確かめた）
円 20個のうち、3コマとも指す物の上にあったのは 6個。3コマとも外れていたのが 8個、途中で外れたのが 6個（体の別の所・後ろの家具・かべ・顔の上に出ていた）。元は5つ：
1. **位置を決める手順が、決まりに無かった。**「その場所に赤い光」「光・輪・線は、編集の道具で重ねる」とだけ書いてあった
2. **座標を、クリップを作る前の止め絵（始めの絵・終わりの絵）の上で読んでいた。** 円が出る時刻の、できた動画のコマでは測っていない。数は 0.5・0.45 のような切りのいい数で、同じ数が何回も出ていた
3. **円を重ねた絵を、1回も見ていなかった。** 作業フォルダに、確かめの絵が無い。検品は 1秒6コマの小さい並びだけ
4. **物が動くのに、円が止まっていた／逆へ動かしていた。** カメラが寄る場面で、円が、体の上から顔の上へ外れた
5. **指す物が、言葉で1つに決まっていなかった・絵に写っていなかった。**「◯◯の所」と書き、服の下で見えない物・体のかげの物を指そうとした

ほかに：円の座標を書いた後に、場面の切り出し（寄り・引き）を変えていた／円の終わりが、場面の切れ目と同じ時刻だった（最後の1コマが次の場面にかかった）。

### 16-1. コマ割りの表で、「何を指すか」を1つに決める（絵より先）
エフェクトの列に、次の4つを書く。書けない円は、置かない。
- **指す物**：体や物の部分の言葉で、1つ。**その絵に写っていて、指でさせる物。**「痛い所」「◯◯の所」「◯◯のあたり」と書かない。
  - 悪い例：「◯◯の痛い所に赤い光」。良い例：「服の上から見える、◯◯の下のふちの線（手のすぐ上）」「◯◯の右のはしの金具」
  - 指したい物が、服や体のかげで見えない時：①見える物に言いかえる（その上の服のしわ・ふくらみ・手が当たっている所）②見える絵に変える（向き・寄り・透ける）のどちらかを、ここで決める。見えないまま、円を置かない
- **その物が、その場面の絵のどこに写るか**（始めの絵で、もう写っている事。途中で画面の外に出ない・手や物でかくれない構図）
- **動くか**：カメラ・体・物の動きで、円が出ている間に、その物が画面の上を動くか（16-4 のどれにするかも書く）
- **出る秒と消える秒**（声の言葉に合わせる＝7章の末）。**消える秒は、場面の終わりの 0.1秒前まで**

### 16-2. 位置は、できた動画のコマで測る（止め絵・コマ割りの数・体の部分の名前から決めない）
1. 測る絵は、**編集の後の1本**（切り出し・寄り引き・左右の反転・速さの変更・つなぎを、全部すませた、円を重ねる前の動画。例 `tmp/silent.mp4`）。クリップ1本・始めの絵・終わりの絵・絵コンテでは測らない（座標が変わる）
2. 円が出る時刻の **最初・真ん中・最後** の3コマを抜く。目もりつきで見る：`$PY $T/gridview.py コマ.png out.jpg`（寄って読む時は、わくと倍率を付ける）
3. 3コマそれぞれで、**指す物の真ん中**の位置を読む（x・y は 0〜1。左上が 0,0）。自分の目で読むか、絵を見られるモデルに「◯◯の真ん中の座標」を聞く。**どちらの答えも、そのまま信じない。16-3 の絵で確かめるまでは、仮の数**
4. 円の大きさは、指す物の大きさから決める（小さい点を指す時：半径は幅の 4〜8%。指す物より大きくして、となりの別の物まで入れない）
5. `fx.json` の行に、**指す物の名前を文字で入れる**（行の最後に `"◯◯の下のふちの線"`）。名前の無い行は、確かめを通らない

### 16-3. 確かめの絵を必ず作って、目で見る（通るまで、動画を書き出さない）
```
$PY $T/pointer_check.py tmp/silent.mp4 --fx fx.json --out work/pointer      # 絵を出す（1つの円につき1枚＝最初・真ん中・最後）
# work/pointer/p00.jpg … を、1枚ずつ Read で見る → work/pointer/判定.json に はい／いいえ を書く
$PY $T/pointer_check.py --gate work/pointer/判定.json --fx fx.json          # 全部「はい」でなければ 1 で終わる。build の前に必ず打つ
```
- 絵の十字＝円の真ん中、輪＝円の大きさ。上が全体、下が円のまわりを大きくした絵
- **問いは1つ：「十字は、指す物の上にあるか」。3コマそれぞれに、はい／いいえ で答える。**「だいたい合っている」「近い」は、いいえ。となりの部分（◯◯の上ではなく下・体ではなく後ろの物）に乗っていたら、いいえ。指す物が写っていない・かくれているコマも、いいえ
- 答えは `判定.json` の `最初`・`真ん中`・`最後` に書き、`見た事` に、十字の下に何が写っていたかを一言書く（「◯◯の下のふちの上」）。**見ないで「はい」と書かない**
- **1つでも いいえ なら、座標を直して、絵を出し直して、もう1回見る。** 座標を変えた行は、道具が前の答えを消す。3回直しても通らない円は、16-4 で形を変えるか、置かない
- 切り出し・寄り引き・反転・場面の長さ・クリップの差しかえを、**後から1つでも変えたら、その場面の円は、測り直して、絵を出し直す**（前の はい は使えない）
- 完成品（円を重ねた後）でも、同じ3コマを 1枚ずつ見る。`$PY $T/pointer_check.py out/<完成>.mp4 --fx fx.json --out work/pointer_final --no-track`

### 16-4. 指す物が動く時（円が出ている間に、画面の上を動く）
`pointer_check.py` が出す「物と円のはなれ」が、半径の 0.5倍より大きい行は、動く物として扱う（数は目安。色の平らな所では追えない事がある。決めるのは 16-3 の目）。上から順に選ぶ：
1. **動きの止まる時刻だけに出す**（先に試す）。カメラが着いた後・体が止まった後の 0.4〜1.0秒に、円を縮める。6章「カメラが着いて、ゆっくり流れている時に出す」と同じ
2. **追わせる**。ゆっくり一方向に動く時だけ。最初と最後のコマで測った位置を、行の始め（x0,y0）と終わり（x1,y1）に入れる。**向きを勘で入れない**（寄る時、物は画面の真ん中から外へ動く）。真ん中のコマで外れたら、円を2つに分ける
3. **止め絵にしてから出す**。速く動く・向きが変わる・手でかくれる時。その時刻のコマを止めて（または、止め絵の切り出しをゆっくり動かして）、その上に出す。止まりは 0.5秒まで（15-5）
4. どれでも通らない時は、**円をやめて、絵の中のエフェクト**（6章。始めの絵か終わりの絵に描く）にするか、**音だけ**にする

### 16-5. 切り出し・寄り引き・反転をした後の座標で置く
- 座標は、いつも **完成の画面（1080×1920）の上の 0〜1**。元の絵・クリップの上の座標を、そのまま使わない
- 編集で絵を変える物（切り出し・ゆっくりの寄り引き・0.2秒の速い寄り・左右の反転・止め絵の動かし）は、**全部すませてから**測る。順は「場面を組む → 測る → 確かめる → 円を重ねて書き出す」
- 同じ絵を別の場面で使い回す時も、場面ごとに測る（切り出しが違えば、位置が違う）

### 16-6. 検品の表と、報告（15-4・15-7 に足す）
- 検品の表に行を足す：**「指す円：◯個。3コマとも はい ◯個／直した回数 ◯回／やめた・形を変えた円 ◯個（どの場面・何に変えたか）／完成品でも見たか」**。はい でない円が1つでもある動画は、出さない
- 報告に書く：上の数・`work/pointer/` の場所・円ごとの「指す物の名前」と「十字の下に見えた物」（`判定.json` の中身）・動く物をどう扱ったか（16-4 の何番）。**絵を見ていない円は、「見ていない」と書く**
- 確かめていない事に書く：再生して、音と一緒に見たか（確かめの絵は3コマだけ。コマの間は見ていない）

### 16-7. 前の決まりとぶつかる所（16章が勝つ）
| 前 | 16章では |
|---|---|
| 15-0 の 2「困り事の言葉の所で、その場所に赤い光＋音」 | 「その場所」を、16-1 の形（写っている物の名前1つ）で書く |
| 15-5 の 9「光・輪・線は、編集の道具で重ねる」 | 重ねる前に、16-2〜16-5。重ねた後に、16-3 の末 |
| 15-0 の 7・8（組む・1秒6コマで見る） | 7 の中で `--gate` を通してから書き出す。8 の 1秒6コマの並びは、円の位置の確かめの代わりにならない（小さくて読めない） |
| 9章「エフェクトが物にくっついているか」 | 編集で重ねる物は、16-3 の絵で見る |

## 17. 映像の直し（2026-10-15 仮ハーネスで試し、2026-10-16 本物へ入れた。ほかの章とぶつかる所は、この章が先）
正本は `zackdfilms/映像の分析_20261015/作り方の直し.md`（数の元は同じフォルダの `分析.md`・`音の一覧.md`）。要点：
1. 大きく速いカメラは、Kling に頼まず編集で作る：Kling には一定の速さで大きく（主役3倍以上／向き45度以上）動かせ、編集で 0.2〜2.4秒を混ぜて約7倍速（0.3秒の山）→ 残りを 0.5倍で流す（直しの 1-1）。人が動く場面とエフェクトの出る区間には使わない
2. 切れ目は、同じ向きの速い振り＋方向ぼかしでかくす（1-2）
3. Kling の指示は直しの 2-2 の型。寄りで終わるクリップに `deep focus` を書かない
4. 寄りの絵は 100mm マクロの文（3-1）。寄り・マクロを6割以上、面すれすれを3割以上。14-9 の背景ぼかしを飛ばさない
5. 24コマを30コマに水増ししない（完成品を 24コマで書き出す）
6. 効果音：速い動きに必ず低いシュッ、着いた所に低いドン、高いキラは10秒に1つまで（4章）
7. BGM：1本に1曲、声より18〜22dB下。自社の W-MOOD-27 を既定。ZackD と同じ曲（Epidemic Sound）は使えない
8. 色：黒を下げ、黄みを戻し、ざらつきを弱める（6章）
9. 目ざす数は直しの 0章（測る道具 `zackdfilms/映像の分析_20261015/tools/zd_measure.py`・`agg.py`）

## 18. 847 の質感で作る手順（正本。2026-10-16 本物へ入れた）
**ほかの章（3・14・15・17）と人物の描き方がぶつかる所は、この章が先。** カメラの動き・編集の速さの山・効果音・BGM・字幕は、17章と `zackdfilms/映像の分析_20261015/作り方の直し.md` のまま。
置き場所：`zackdfilms/質感847/`（`参考/`＝渡す本物のコマ・`指示の見本/`＝実際に通った指示の全文・`見本/`＝847 の始めと終わりの絵と10秒の動画・`tools/`＝道具）。見本の動画：`zackdfilms/質感847/見本/847_B_10秒.mp4`。

### 18-1. 一番大事な事
- **質感は、言葉ではなく、渡す本物のコマで決まる。** 本物の ZackD の画を切り抜いて、1枚ずつ役目を書いて渡す（「Image 2 = この肌と顔の作りに合わせる。この顔は写さない」）。言葉だけ・本物のコマ1枚まるごとだけでは、写真の顔かピクサーの顔に振れた（2026-10-15〜16 の試し）
- **細かさの言葉を書かない**（毛穴・そばかす・ほくろ・しわ）。Codex は写真らしさと読んで、写真の顔に戻る
- 画像は Codex だけ（`tools/gen.sh`。1枚15分で強制終了・同時に3本まで）。参考画像は5枚まで（6枚は断られた）
- 人物は、うちのオリジナル。本物のコマの人・服・部屋・ロゴは写さない（質感だけ借りる）。本物のコマを土台にして人だけ替える作り方は、ZackD の作品の流用になるので使わない

### 18-2. 作る順（1コマずつ。5段。前の段の絵を次の段の Image 1 にする）
| 段 | すること | 渡す物（順番どおり） | 指示の見本 |
|---|---|---|---|
| 0 | **人物の見本を1枚作る**（商品ごと・相手ごとに1回）。普通の体つきの日本人・服は1色・長袖なら「手首までの長袖」と書く | `参考/3_人物/` の2〜3枚 | `見本/人物の見本の例_Y4.png` |
| 1 | **土台の絵**：構図・水色の部屋・場面を作る | 構図の本物1枚（`参考/1_構図と質感/<場面>/1_構図_*`）＋質感の切り抜き2〜3枚（顔の肌・服・壁）＋（2コマ目から）前のコマ | `指示の見本/1_土台_顔の寄り.txt` |
| 2 | **ぼけとブレ**：寄りは目だけにピント、手前も奥もとける | 段1の絵＋`参考/2_ブレとぼけ/` の1〜2枚＋人物の切り抜き1枚 | `2_ブレとぼけ_顔の寄り.txt` |
| 3 | **人物の描き直し**：顔・肌・髪・服を ZackD の既製の 3D 人物に | 段2の絵＋段0の人物の見本＋`参考/3_人物/` の T10・T07・T13 | `3_人物_断面の画.txt` |
| 4 | **影**：上からの大きな白い1灯・首とあごの下と襟の内側を暗く・前髪の影・目のくぼみ・接地の小さな影・部屋の明るさは変えない | 段3の絵＋`参考/4_影/` S01・S03＋人物の見本＋T10 | `4_影.txt` |
| 5 | **質感B（847）**：ひと昔前のゲーム画面（Unreal Engine 4 のころ）で描き直す | 段4の絵＋T10＋T19（終わりの絵は、＋同じ場面の始めの絵を Image 4） | `5_質感B_始めの絵.txt`・`5_質感B_終わりの絵.txt` |

段5の言い方（そのまま使う）：`RE-RENDER Image 1 as a real-time game engine frame (Unreal Engine 4 era, not 5): mid-poly stock character, low-resolution skin texture that looks slightly smeared, simple skin shader with a dull sheen, hair as a solid mass of hair cards with soft alpha edges, cloth as one flat color with a few broad baked folds, slightly plastic look overall, real-time lighting with soft shadow edges and screen-space ambient occlusion in creases, mild bloom, video compression softness. … Keep the framing, the camera angle and every object of Image 1 at exactly the same place. No motion blur, no streaks. Match the rendering of Images 2-3 exactly; do not copy their people. No text.`

- 段1〜4 は、2026-10-16 にこの順で作って 847 が出た。**段を飛ばして早くする近道は、まだ試していない**（試す時は、仮ハーネスの別の試しとして）
- 1コマできるたびに原寸で見る：指・手の数・顔の崩れ・物の位置・服（袖の長さ）・前のコマとのずれ。直す時は、その段だけやり直す

### 18-3. 動画にする始めと終わりの絵
- **始めと終わりの絵には、ぼけだけを描く。ブレは描かない。** 絵にブレがあると、Kling がそれを光る筋として最後まで残す（2026-10-16）。ブレは編集で足す（17章の 1）
- 終わりの絵は、始めの絵の「ここだけ変える」の編集で作る：人のポーズと顔だけを変え、部屋・物・カメラは画素のまま（`指示の見本/5_質感B_終わりの絵.txt`）。同じ場面の始めの絵を Image 4 に渡すと、人と部屋がそろう
- 人は動かす：びくっとする・腰をつかむ・もたれる・足を開く。1場面で姿勢を2〜3回変える（ZackD の人は止まらない）

### 18-4. 動画と編集
- 動画：Higgsfield `kling_o3_flf`・pro・音なし・3〜5秒（`tools/clip.sh`。打つ前に `higgsfield generate cost`・同時に3本まで・作り直しは1本に1回まで）。指示は `指示の見本/6_動画_*.txt` の形（動かない物の名前・起きる順の動き・手の数・カメラ・ピント）
- Kling は 9:16 と頼んでも 2:3（1176×1764）で返す時がある → 編集で左右を切る（`tools/crop.py`）
- 編集：17章のまま（速さの山とコマを混ぜたブレ・振りのつなぎ・24コマで書き出す・速い動きに低いシュッ・BGM は自社の W-MOOD-27 を声の約20dB下・字幕は白の太字に黒いふち・高さ約78%）。組み立ての見本：`tools/render.py`・`tools/plan_847_B.json`（パスは作業フォルダに合わせて直す）
- 847 は、最後に色の仕上げ（17章の 8）をかけていない。この見た目を変えないため、かけない
- 検品：6コマ/秒で全クリップを見る（物が勝手に動く・すり抜け・手が増える・足がすべる・顔が変わる）・つなぎ目は24コマ/秒で見る・声は whisper で台本と照らす

### 18-5. まだ残っている事（847 の時点）
- 動画にすると、Kling が自分の描き方に少し寄せる（止め絵より差が小さくなる）
- 痛みの光る印（断面の黄色のふちなど）は、段5で消えることがある → 編集か、段5の指示で「残す」と書く
- お尻を真ん中に写さないため、腰へ寄る画が上半身寄りになる時がある

### 18-6. 通しで作った時の直し（2026-10-16 夜、針マット_14_通し_02 で 847 の手順のまま3分の動画を最後まで作って分かった事。2026-10-20 に入れた）
記録の全文：`zackdfilms/質感847/通し/作り方の記録_針マット_14.md`。通しで回した道具：`zackdfilms/質感847/通し/tools/`（下の表）。指示の文の実物：`通し/指示の例/`。
**使い方**：作業フォルダ（例 `（作業フォルダ：アプリには同梱していない見本）`）に `tools/` を写して使う（道具は「tools の1つ上」を作業フォルダとして読む：`指示/`・`work/gen/`・`クリップ/847/`・`声/`）。音の棚は `（作業フォルダ：アプリには同梱していない見本）` を読む。

| 道具 | する事 |
|---|---|
| `mk_vo.py`・`tighten.py`・`align.py`・`timing.py` | 声を全文1回で録る → 間を詰めて1.12倍 → 文字の時刻 → 句ごとの時刻 |
| `shots.py` | コマ割りの正（場面・始めと終わりの絵・カメラ・指す物） |
| `pipe.py` | 絵の段0〜5 を場面ごとに自動で回す（同時3本。できた絵は飛ばすので、止まっても同じコマンドで再開） |
| `pairs.py`・`wait_pairs.sh`・`sheet.py` | 始めと終わりの絵を並べて見る |
| `clips.py`・`clip.sh`・`clipcheck.py`・`clipsheet.sh` | Kling の動画（3〜5秒）と、6コマ/秒の検品シート |
| `plan.py`・`render2.py`・`compose.py`・`overlays.py`・`crop.py` | 編集の表 → 速さの山とブレ・24コマで組む → 効果音と曲 → 札 |
| `cmp_whisper.py`・`web.py`・`build.py` | 書き起こしで台本と照合・確かめのページ |

**決まりに足す事（通しで外れた所。どれも、そのまま守る）**
1. **商品の写真を商品フォルダに1枚置く**（`00_入口.md` の仕入れ先・同型の写真）。写真に付属品（袋・巾着）が写っていたら、「本体だけ」「付属品だけ」に切り分けて渡す（まぎれこむ）。場面の指示に「袋を置かない」と書く
2. 段2の Image の順は、通った見本（`指示の見本/2_*.txt`）の順に合わせる（本物の構図が Image 1、自分の段1の絵が最後）。表の「前の段の絵を Image 1」より見本が先
3. 段2の見本の文の「motion blur」は抜き、`NO MOTION BLUR` を足す（18-3 のとおり、絵にブレは描かない）
4. **段3に年齢と顔の形を書く**（「50代の丸い・ふくよかな顔・ほおのたるみ。若くしない・きれいにしない」）。**段5に、承認された 847 の絵（`見本/S1_始め.png`）を Image 4 として渡す**（「顔と色の明るさだけ合わせる・部屋は写さない」）。顔の寄りは `S3_始め.png` を段3の Image 2 に渡す方がよい
5. 体の断面は「真横・前が画面の左・背中が右・後ろからは見ない」と書く（書かないと後ろ姿で出る）
6. 人のいない場面（断面・マクロ・物）の段5の Image 2-3：断面は `参考/1_構図と質感/D_体の中の断面/2_質感_赤い組織.png`・`3_質感_骨と脂肪.png`、物と部屋は `B/2_質感_水色の部屋の人.png` 系を渡す
7. 終わりの絵は、段5の後の始めの絵を Image 1 にして「人の形と顔だけ変える」編集を1回（Image 2-3＝T10・T19）。全部を5段でやると絵の上限に入らない
8. **量の見込み（3分の動画）**：場面約60・人の場面の始めの絵だけで Codex 約150回（1枚に5回・約7分）・合計 約280枚・Higgsfield 約240 クレジット（約50本）・約3時間。同じ場所の2コマ目からは、段1に「同じ場所の前のコマの段1の絵」を渡すと並べて作れる。段3・4 は差が小さい場面がある（飛ばす近道は試していない）
9. 絵に文字・ロゴ・数字を入れない（時計・カレンダーは字の無い物にし、時刻は編集の札で重ねる）
10. Kling の指示の見本は人の場面しか無い。断面・マクロ・物だけの場面は、人の文（顔を保つ・服）を外した形（`clips.py` の中）
11. 物の多い部屋で「tracks sideways（横に追う）」を頼まない（部屋が別の部屋に変わる）。カメラをほぼ止めて1歩だけ歩かせる。外の道は変わらない（15-5 の 7 に足す）
12. Kling の寄りは、終わりの絵の切り出し 1.2倍までに守る（1.3〜1.5倍は届かない事がある）
13. 断面の場面の背景ぼけの見本は `参考/2_ブレとぼけ/` に無い（シアンの無地では効かない）
14. **0.4秒より短い効果音は、統合の大きさ（ebur128 の I）が −70 になって +56dB かかる**。−16 LUFS として置く（`compose.py` は直してある。`build.py` には同じ穴がある）
15. 1文が5秒を超える文は、5秒のクリップを 0.85〜0.9倍で流す。0.9〜1.2秒の短い文は、3秒のクリップの後ろだけを使う
16. Codex は同時3本まで。作り直しは、走っている `pipe.py` に任せる（外から打つと4本になる）
17. 音：BGM は W-MOOD-27 を1曲通し、声より約20 LU 下。フックは4dB下・原因の名前の前は6dB下・商品から2dB上・締めは3dB下（`sound-rules.md` 4章）。24コマで書き出し、色の仕上げはかけない
