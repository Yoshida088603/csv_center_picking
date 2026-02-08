# potree-copc-viewer 参照分析

参照リポジトリ: [Yoshida088603/potree-copc-viewer](https://github.com/Yoshida088603/potree-copc-viewer)  
公開URL: **https://Yoshida088603.github.io/potree-copc-viewer/**

## 概要

- Potree をベースにした COPC（.copc.laz）専用ビューア
- クエリパラメータ `r` で「reg_id または COPC の URL」を受け取り、その COPC を表示
- 複数指定可（カンマ・改行区切り）→ 複数点群を同時表示

## 起動時の流れ（index.html）

1. **入力**: `getQueryParam('r')` で `?r=...` を取得
2. **パス解決**:
   - `id` が `https?://` で始まる → **その URL をそのまま** COPC のパスとして使用
   - 否则 → `https://gsrt.digiarc.aist.go.jp/3ddb-pds/copc/${id}.copc.laz` を生成（reg_id 想定）
3. **読み込み**: `Potree.loadPointCloud(path, name, callback)` を各 ID/URL に対して実行
4. **表示**: `viewer.scene.addPointCloud(e.pointcloud)` でシーンに追加

## 読み込みまわり（src）

| ファイル | 役割 |
|----------|------|
| `Potree.js` | `path.includes('.copc.laz')` のとき `CopcLoader.load(path, callback)` を呼ぶ |
| `loader/EptLoader.js` | `CopcLoader.load(file, callback)` — `window.Copc` の `Getter.http(url)` で HTTP 範囲取得し、`Copc.create(getter)` で COPC を開く |
| `libs/copc/index.js` | COPC フォーマット用ライブラリ（Getter.http, Copc.create など） |

## yokutsukau_pointcloud との連携方針

- **「Potreeで表示」** = 選択した候補の COPC URL を potree-copc-viewer の `?r=` に渡して**別タブで開く**
- 候補の `external_link` が **.copc.laz または .laz の URL** なら、その URL をエンコードして  
  `https://Yoshida088603.github.io/potree-copc-viewer/?r=${encodeURIComponent(url)}` で開く
- **ZIP のみの候補**（`isZip: true`）の場合は、COPC 直リンクがないため「Potreeで表示は COPC 形式のみ対応」などと案内するか、3DDB の reg_id から  
  `https://gsrt.digiarc.aist.go.jp/3ddb-pds/copc/{reg_id}.copc.laz` を試す（同一ホストなら開ける可能性あり）

## 実装で使う情報

- Potree で開く URL の形:  
  `https://Yoshida088603.github.io/potree-copc-viewer/?r=<COPCのURLまたはreg_id>`
- 複数開く場合: `?r=url1,url2` のようにカンマ区切りで渡せる（index.html の `ids.forEach` で分割して読み込み）
