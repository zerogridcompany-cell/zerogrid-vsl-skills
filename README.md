# Zero Grid VSL スキル

Zero Grid アプリが VSL（動画広告）を作るときに使っているスキルを、アプリの同梱版（`zerogrid-app/resources`）から抜き出したもの。抜き出した日：2026-11-14。

**最初に [はじめに_つなぐ物.md](はじめに_つなぐ物.md) を読んで、ElevenLabs（声）・Codex（絵）・Higgsfield（動画化）の3つをつないでください。** 手順書に出てくるアプリの道具の名前を、このリポジトリのどの道具に読み替えるかも、そこに書いてあります。

台本を「寄せなし」（どの映像の型にも寄せない）で書く時は、`vsl-script/references/台本の決まり.md` だけで書きます（0c章に運び・長さ・書き直しの決め）。

| フォルダ | 中身 |
|---|---|
| `vsl-script/` | VSL の台本を、認知段階に合わせて書く |
| `zackd-ad/` | 動画の型 v1（3D 図解）を台本から完パケまで作る |
| `ec-ad-ops/references/video-formats/` | 動画の型ごとの作り方（ZackDFilms・skeleton・clay-story・authority-live など）と道具 |
| `ec-ad-ops/references/` | 動画の型の一覧・VSL の種類・商品理解の基盤 |
| `ec-ad-ops/templates/` | VSL の依頼書・権威 VSL のひな形 |
| `_rules/` | 音声と VSL の品質基準 |
| `_アプリでの動画の作り方.md` | アプリの中で上の手順を回す方法 |
| `_アプリでの読み方.md` | 社内の道や呼び名を置き換えた前提 |
| `はじめに_つなぐ物.md` | 声・絵・動画化のサービスのつなぎ方と、アプリの道具の読み替え |
| `音の棚/` | 自社で作った効果音と BGM（一覧は `sounds.json`） |

アプリ専用に直した版（`app-skills`）がある道具は、その版で上書きしてある。
