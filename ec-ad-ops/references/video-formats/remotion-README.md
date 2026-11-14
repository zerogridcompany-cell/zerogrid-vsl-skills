# VSL 最初の10秒：Remotion の土台

縦 1080×1920・30fps・300コマ（10秒）。10人が同時に別々のフォルダで作っても衝突しないように、**各自が自分の entry で書き出す**。

## 3行で

```bash
cd （作業フォルダ：アプリには同梱していない見本）
cp -R src/_template src/f3          # 自分の番号で。entry.ts と index.tsx の "fX" を "f3" に書き換える
npx remotion render src/f3/entry.ts f3 ../out/f3_pixar.mp4 && scripts/check.sh ../out/f3_pixar.mp4
```

`scripts/check.sh` は ffprobe の確認（1080×1920・30fps・10.0秒・300コマ・音声あり・音量）と、0.5秒ごとの20コマを並べた `../out/f3_sheet.jpg` を作る。作ったら必ず Read で開いて、誤字・はみ出し・絵の破綻・黒い画面を見る。

## 決まり（衝突しないために）

- 触ってよいのは `src/f<番号>/` と `（作業フォルダ：アプリには同梱していない見本）` だけ。
- `src/common/`・`src/Root.tsx`・`src/index.ts`・`public/`・`sounds/`・`package.json`・`remotion.config.ts` は書き換えない。`npm install` もしない。足りない部品は自分のフォルダに作る（common の部品を写して直してよい）。
- 書き出しは必ず `src/f<番号>/entry.ts` を指定する。`src/index.ts`（全部入り）で書き出すと、他の人の作りかけで止まる。
- Composition の id は `f<番号>`（entry.ts の `makeRoot("f3", Main)`）。大きさ・コマ数は `makeRoot` が 1080×1920・30fps・300コマに固定する。
- `index.tsx` は `export default` で部品を1つ出す（Studio の全部入り Root がそれを読む）。

## 置き場所

| 物 | 置く場所 | コードでの書き方 |
|---|---|---|
| 生成した絵・動画・声 | `../assets/f3/scene1.mp4` | `"a/f3/scene1.mp4"`（`public/a` が `assets/` へのリンク） |
| 音ボックスの効果音・BGM | 写してある（`sounds/`） | `<Sfx name="pop" />`・`<Bgm name="bgmLofi" />` |
| 自分で作った音（seed_audio など） | `../assets/f3/kachinko.wav` | `<Sfx src="a/f3/kachinko.wav" />` |
| 書き出した動画 | `../out/f3_<短い英名>.mp4` | — |

- `public/` の中に**ファイル単位のリンク（ln -s）を置かない**。Remotion の配信が 404 を返す（フォルダのリンクは読める）。素材は `assets/f<番号>/` に実体を置く。
- ファイル名は半角英数にする（日本語のファイル名は文字の正規化で読めないことがある）。
- 動画は h264 の mp4、絵は png / jpg / webp、声は mp3 / wav / m4a。

## 部品（`import { … } from "../common"`）

座標はすべて 1080×1920 の px。秒は動画の頭からの秒。

### 字幕

```tsx
<Captions
  cues={[
    { at: 0.4, text: "床拭きが終わらない" },
    { at: 1.4, text: "一番の原因は", em: true },        // 句全体を黄色＋1.12倍
    { at: 5.0, text: "犬は*鼻*で" },                    // * * の中だけ黄色
    { at: 8.2, text: "においが残ります", em: "red", to: 9.0 },
  ]}
/>
```

- 句を1つずつ差し替える。白字・黒ふち・影。出る時に少し大きく出て縮む。次の句が出るまで出し続ける（`to` で先に消せる）。
- 既定：`y={0.665}`（文字の中心の高さ。見本の実測）、`size={96}`、`font="maru"`。
- 長い句は幅に収まるように自動で小さくなる。**1句は全角11字まで**が目安（12字で約76pxまで縮む）。改行はしない。
- `<KaraokeCaption words={[{ text: "毎朝", at: 0.2 }, …]} from={0} to={2.5} />`：1行を出したまま、話している語だけ黄色にする。
- `<OutlineText text="…" size={60} />`：ふち付きの文字だけを好きな場所に置く時。

### フォント

- `font="maru"`（既定）：M PLUS Rounded 1c ExtraBold。見本の丸ゴシックに近い。`public/fonts/` に置いてある（SIL OFL）。
- `font="kaku"`：この Mac のヒラギノ角ゴシック W8。
- どちらも読み込みが終わるまで書き出しを待つ（`common/fonts.ts`）。自分で部品を作る時は `fontFamily: FONT.maru`、`fontWeight: 800`。

### ラベル

```tsx
<Label text="毎朝 床を拭く方へ" at={0.1} to={5} x={370} y={150} />                                   // 黄色・左上の大ラベル
<Label text="毎日敷いてるコレ" at={2.5} to={5} x={770} y={790} variant="white" size={50} rotate={6} />  // 白・物の横の小ラベル
<Label text="床が目印に" at={8.7} x={540} y={900} variant="redFrame" size={96} rotate={-5} big={2.2} /> // 札：大きく出て縮む
```

- `x`,`y` はラベルの**中心**。`variant`：`yellow`／`white`／`blueFrame`（白地・青枠）／`redFrame`（白地・赤枠）／`black`。
- 出る時に `big` 倍（既定 1.45）で出て約0.2秒で縮む。`noPop` で動きなし。
- 画面の外にはみ出す時は自動で内側に寄せ、字を小さくする。

### 印

```tsx
<RedX at={0} x={540} y={570} size={520} />
<Arrow at={5.6} from={[820, 250]} toPoint={[640, 430]} curve={-60} />   // 色は color で。黒ふち付き
<Circle at={6.5} x={540} y={570} rx={300} ry={130} />                   // 手で囲んだような丸
<Check at={9.4} x={860} y={380} size={190} />
```

### 絵・動画

```tsx
<Clip src="a/f3/scene1.mp4" />                                   // 全面。音は消す。trim で頭を飛ばす
<Clip src="a/f6/talk.mp4" sound volume={1} position="50% 30%" /> // 人物が話す動画は sound を付ける
<KenBurns src="a/f9/panel1.png" dur={3.3} fromScale={1} toScale={1.1} toPos={[0.03, 0]} />
<Still src="a/f1/dog.png" x={140} y={200} width={800} height={700} />   // 切り抜き PNG を置く
```

- どれも `x` `y` `width` `height` で枠を決められる（省くと全面）。枠からはみ出た分は切れる。
- `Clip` は場面より動画が短いと最後のコマで止まる。5秒の動画を10秒に使う時は場面を分けるか `playbackRate={0.5}`。
- `KenBurns` は **Scene の中に置く**（場面の頭から動き始める）。`dur` はその場面の長さ。

### 地・枠・その他

- `<GridBg />`：見本の水色の格子（上は平らな格子の壁、下は奥行きのある床）。`horizon={0.5}` が床の始まる高さ、`horizon={null}` で全面が平らな格子。`colors` で色替え。
- `<Scene from={0} to={5}>…</Scene>`：場面。切り替えは一瞬（見本と同じ）。
- `<ProgressBar />`：下端の黄色い線。
- `<Split top={…} bottom={…} ratio={0.5} />`：上下2分割。
- `<HeadlineBar text="…" y={960} />`：出しっぱなしの見出し帯（既定は赤地に白字。`bg` `color` `width` `radius` `border` で白い札にもなる）。
- `<Flash />`：場面の頭を一瞬白く光らせる（Scene の中に置く）。
- `sec(秒)`：秒→コマ。`popScale(コマ)`：ラベルと同じ「大きく出て縮む」倍率。`COLORS`・`W`・`H`・`FPS`・`DURATION`。

### 音

```tsx
<Voice src="a/f3/voice.mp3" />                       // ナレーション・話し声
<Bgm name="bgmWarmExplain" volume={0.1} dips={[[4.5, 5.0]]} />
<Sfx at={0} name="don" volume={0.6} />
<Sfx at={5.0} name="whoosh" volume={0.4} />
```

- `Sfx`：`at` 秒に鳴らす。`trim`（音の頭を飛ばす）・`dur`（長さの上限）。`<SfxTrack items={[…]} />` でまとめて置ける。
- `Bgm`：頭と終わりを自動でなだらかにする。`trim` で曲の途中から。`dips` の区間だけ下げる。
- 音量の目安：声 1.0／BGM 0.08〜0.15／効果音 0.3〜0.6（冒頭の `don` だけ 0.6〜0.8）。音ボックスの音は単独用の音量なので、そのままの 1.0 では大きすぎる。見本は全体で −13 LUFS（`check.sh` が出す）。
- 音ボックスは README に「聴感は未確認」とある。機械の検査しか通っていない音。

音の名前（`src/common/sounds.gen.ts`。元の日本語名も入っている）：

| 用途 | 名前（秒） |
|---|---|
| 冒頭・見せ場 | `don` 低いドンという着地(1.5)／`boom` 重い衝撃音ドン(1.4) |
| ラベル・札 | `pop` 短いバブルのポップ(0.5)／`ding` 澄んだベルのディン(1.2)／`click`(0.5)／`check` ピコン(0.6)／`pop3` 三つのポップ(3.5) |
| 場面の切り替え | `whoosh` 短く軽いシュッ(0.5)／`whooshLand`(0.8)／`swipeSoft`(1.0)／`swipeLight`(2.1)／`cardWhoosh`(0.6)／`reverseCymbal`(1.0) |
| フック | `riserSoft`(1.65)／`riserRumble` 低いうなりから上がる(1.9。運営者 が採用したライザーは `riserSoft` とこの2つ)（フックには必ずライザーを入れ、決めの一言で終わらせる）／`spill` 液体が床に落ちて広がる(2.5)／`tear` 紙シーツが破れる(2.0) |
| 気づき | `discover` 温かい発見音(1.1)／`sparkle` きらきら(1.8)／`chime` 正解の二音(1.0) |
| 生活音 | `wipe` 布で床を拭く(2.7)／`wring` 雑巾を絞る／`wetStep` 濡れた床を踏む／`sniff` 犬がくんくん／`whine` くぅん／`barkHappy` うれしい一声／`slippers`／`drip`／`bagRustle` シーツの袋／`scissors`／`door`／`spray` |
| 否定 | `buzzer` 不正解のブザー／`scratch` レコードのスクラッチ（軽い口調の型だけ） |
| 緊張 | `heartbeat`(3.0)／`clock` 秒針(3.0)／`cageDoor` |
| 金額 | `coin`／`coinDrop`／`register` |
| BGM | `bgmWarmExplain` 軽く温かい説明用(20)／`bgmLofi` 温かいlo-fi(45)／`bgmComical` 軽くコミカル(45)／`bgmTense` 緊張感(44)／`bgmSadPiano` 悲しいピアノ(45)／`bgmCta` 明るく軽い(45)／`bgmDarkPad` 暗いパッドと心拍の緊張(60。困りごと・原因の既定)／`bgmTenseCreep` 半音で動く低音と秒針の緊張(60。スマホでは小さい)／`bgmCrisis` せり上がる危機感(45)／`bgmRelief` ほっとするピアノとパッド(45)／`bgmCalmEp` エレピと丸い低音の安心(45)。**曲は段の中身に合わせる**：困りごと・原因・放置した先に `bgmWarmExplain`・`bgmComical`・`bgmCta`・`bgmLofi` を敷かない。置く前に `python3 ec-ad-ops/scripts/bgm_check.py "<段>=<曲の日本語名>" …` を通す（2026-10-06 運営者 指定） |

「アルコット参考のBGM」と「参考由来」の棚は権利が未確認なので入れていない。無い音（カチンコ・歌など）は Higgsfield の seed_audio で作って `assets/f<番号>/` に置く。

## Scene と秒の注意（いちばん間違えやすい）

`Scene`（Sequence）の中では時間が場面の頭から 0 になる。**`Captions`・`Label`・`Sfx`・`Bgm`・`Voice`・印は Scene の外（いちばん上の層）に置いて、全体の秒で書く**のが安全。場面と一緒に消したいラベルは `to` を場面の終わりに合わせる。Scene の中に入れるのは絵（`GridBg`・`Clip`・`KenBurns`・`Still`・`Flash`）と、場面の頭からの秒で書いた印。

重なりの順は書いた順（後に書いたものが上）。絵 → 印・ラベル → 字幕 → ProgressBar → 音 の順に書く。

## 見本（H-OHI-008a_v2）の実測

- 字幕：文字の中心が高さ 66.5%（1277px）。約100pxの丸ゴシック、白字・黒ふち・影。強調の句は黄色で少し大きい。formats.md の1番は「高さ40%あたり」と書いているが、動画のコマを測ると 66.5% だった（既定値は実測に合わせた）。
- 絵は上から 60% ほどまで。字幕の下（70%〜）は床の格子だけで空けてある。
- 上の黄色ラベル：中心 (540, 200) 前後（落ち着いた後の幅は約800px）、傾き −3度、字 約78px。小ラベル：傾き +6度、字 約50px。
- 床の始まりは高さ 50% 前後。下端に黄色い線。
- 見本の動きに寄せた所：ラベルと札は大きく出て約0.2秒で縮む／字幕は句ごとに一瞬で差し替え／場面の切り替えは一瞬。

## 確かめる・見る

```bash
npx tsc --noEmit                                         # 型の間違いを先に見つける（数秒）
npx remotion still src/f3/entry.ts f3 /tmp/x.png --frame=75   # 2.5秒のコマを1枚だけ出す（配置の確認が速い）
npx remotion render src/f3/entry.ts f3 ../out/f3_pixar.mp4    # 10秒で約15〜40秒
scripts/check.sh ../out/f3_pixar.mp4                     # ffprobe＋コマ並べ（../out/f3_sheet.jpg）
```

- 並列は `remotion.config.ts` で 3 に抑えてある（10人が同時に書き出すため）。上書きも有効。
- 映像はちょうど 10.000秒・300コマ。全体の長さは AAC の区切りで 10.005秒と出る（check.sh は 9.99〜10.03 を可にしている）。
- Studio で見たい時：`npx remotion studio src/f3/entry.ts --port=31<番号2桁>`（ポートを人ごとに変える）。全部入りは `src/index.ts`。
- `src/demo/`：絵を使わない見本（`../out/_demo.mp4`）。`src/_mediatest/`：`a/…` の動画・静止画が読めるかの確認用。どちらも書き方の例になる。
- 音ボックスに音が増えたら `node scripts/link-sounds.mjs`（表に1行足して実行。`sounds/` に写し、`sounds.gen.ts` を作り直す）。これは土台の持ち主だけが行う。

## 料金の確認（運営者 の確認待ち）

Remotion は個人と従業員3人以下の会社は無料、4人以上の会社は有料のライセンスが要る。
