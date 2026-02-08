以下を **そのままLLM（実装担当）に投げる指示書**として使ってください。

---

## 追加機能 指示書（平面直角→該当COPC→LAZ丸ごとDL）

目的：`yokutsukau_pointcloud` に機能追加し、ユーザーが **平面直角座標（X,Y）と系番号** を入力すると、3DDB API で該当する **COPC（= .laz）** を特定し、**切り抜き無しで丸ごとLAZをダウンロード**できるようにする。表示機能の有無は問わないが、DLが主目的。

要件：

1. UI追加：入力欄「系（1〜19 もしくは EPSG:667x）」「X(Easting, m)」「Y(Northing, m)」とボタン「COPC検索」「LAZダウンロード」。系は必須。初期値は東京想定で「9系（EPSG:6677）」を選択状態にする。入力値バリデーション（数値・未入力・系未選択）を実装。
2. 座標変換：ブラウザ側で `proj4js` を使用し、平面直角→経緯度（JGD2011 lon/lat）へ変換。`always_xy` 相当で x=Easting, y=Northing を徹底。最低限「9系」だけ定義して動作させ、可能なら1〜19系を同様に登録。変換先は JGD2011（EPSG:6668）。
3. COPC検索：3DDB API を `GET /api/v1/services/ALL/features?area=POINT(lon lat)&limit=50` で呼ぶ（ベースURLは現行のデモ `https://gsrt.digiarc.aist.go.jp/3ddb_demo` をデフォルト、設定で差し替え可能にする）。レスポンスGeoJSONの `features[].properties.external_link_type=="copc"` かつ `external_link` を抽出し候補配列にする。
4. 候補選択：候補が0なら「該当COPCなし」を表示。複数ならUIに候補リスト（title/reg_id/外部URL）を表示し、デフォルトは先頭を選択。改善として可能なら「入力点とfeature geometry の距離最小」を選択（geometryがPolygon/Point混在に備えて安全に）。
5. ダウンロード：選択した `external_link` を **そのまま .laz として保存**する。巨大ファイル対策として `fetch→blob` は原則避け、`<a href="URL" download="xxx.laz">` でブラウザの標準ダウンロードを起動する（CORS回避・メモリ節約）。ファイル名は `reg_id` や `title` から安全な文字列にして `3ddb_{reg_id}.laz` を基本とする。
6. エラー処理：API失敗、変換失敗、CORS/ネットワーク、ダウンロード失敗（ユーザーがブロックした等）を捕捉し、UIに短いメッセージ表示。コンソールにも詳細ログ。
7. 実装は既存構成（Vite/静的）を崩さず、追加JS/TSを最小に。新規関数：`convertXYToLonLat(epsg,x,y)`、`searchCopc(lon,lat)`、`triggerDownload(url,filename)` を分離してテストしやすくする。

完了条件：系+X+Y入力→検索→候補表示→ボタンでCOPC(.laz)が丸ごとダウンロード開始されること。切り抜き・再圧縮は実装しない。
