# 算楽塾 教材コンテンツ

小学生向けインタラクティブ算数教材（単体で動作する HTML）と、その一覧ページです。

## GitHub Pages で公開する

1. GitHub の本リポジトリ → **Settings** → **Pages**
2. **Source** に `Deploy from a branch` を選択
3. **Branch** に `main` / フォルダは `/ (root)` を選択して **Save**
4. 数分後に `https://<ユーザー名>.github.io/sangaku_jyuku_contents/` で公開されます

`index.html` がトップページ（教材ポータル）になります。
`.nojekyll` は Jekyll による変換を無効化し、ファイルをそのまま配信するためのものです。

## 管理システムへのリンク

`index.html` 末尾の `SYSTEM_URL` に、算数ブロックパズル管理システム
（AWS Amplify Hosting）の URL を設定してください。

```js
const SYSTEM_URL = "https://main.xxxxxxxx.amplifyapp.com";
```

空のままだとポータル上のボタンは「準備中」表示になります。
管理システムは Next.js + Cognito 認証のため GitHub Pages 上では動作せず、
Amplify Hosting 側へのリンクとして扱います。

## 教材一覧

| フォルダ | 教材 | 対象 |
|---------|------|------|
| `tangram/` | タングラム（Level 1〜3） | 小3〜6 |
| `nikichin/` | ニキーチンの積み木 3D（入門 / 5ピース / 7ピース） | 小1〜6 |
| `mahoujin/` | 魔法陣パズル（3×3 / 4×4 / かけ算） | 小2〜5 |
| `pascal_sankaku/` | パスカルの三角形（虫食い / 色ぬり / 道のり）＋ PDF | 小4〜6 |
| `koubaisu/` | 公倍数つなぎ（Level 1〜3） | 小5〜6 |
| `tateyoko/` | たてよこ算（2×2 たし算 / 2×2 かけ算 / 3×3） | 小1〜4 |

各教材は単体の HTML ファイルで完結しています（ニキーチンの 3D 教材のみ
CDN から Three.js を読み込むため、初回表示時にネットワーク接続が必要です）。

## ローカルで確認する

```bash
python3 -m http.server 8000
# http://localhost:8000/ を開く
```
