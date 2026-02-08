# 実装計画: 3DDB COPC の Potree 可視化オプション

## 目的

見つかった COPC 候補について「ダウンロード」に加え、**Potree で可視化する**オプションを追加する。  
[potree-copc-viewer](https://github.com/Yoshida088603/potree-copc-viewer) を別タブで開き、選択した候補の COPC を表示する。

---

## 前提・参照

- 公開ビューアURL: `https://Yoshida088603.github.io/potree-copc-viewer/`
- クエリ `?r=` に「COPC の URL」または「reg_id」を渡すと、その COPC を読み込んで表示する（詳細は `docs/POTREE_COPC_VIEWER_ANALYSIS.md`）

---

## 実装タスク

### 1. UI 追加

| 項目 | 内容 |
|------|------|
| 対象 | COPC 候補リスト表示エリア（`#copcCandidateList` 付近） |
| 追加要素 | 「Potreeで表示」ボタン 1 つ（候補選択後に有効） |
| 配置 | 「LAZダウンロード」ボタンと横並び、または候補リスト直下 |

### 2. クリック時の挙動

| 条件 | 処理 |
|------|------|
| 選択候補が **COPC/LAZ の URL**（`external_link` が .copc.laz / .laz） | その URL を `encodeURIComponent` し、`potreeViewerBase + '?r=' + url` を `window.open(..., '_blank')` で開く |
| 選択候補が **ZIP のみ**（`isZip: true`） | reg_id から `https://gsrt.digiarc.aist.go.jp/3ddb-pds/copc/{reg_id}.copc.laz` を組み立て、同様に `?r=` で開く（同一ホストに COPC がある場合のフォールバック） |
| 未選択・候補なし | ボタンは disabled のまま。クリック不可。 |

### 3. 定数・設定

| 項目 | 内容 |
|------|------|
| Potree ビューアベースURL | 定数で保持（例: `POTREE_COPC_VIEWER_BASE = 'https://Yoshida088603.github.io/potree-copc-viewer/'`） |
| 変更可能性 | 将来的に設定で差し替え可能にしてもよい（今回は定数で十分） |

### 4. エラー・案内

| 状況 | 対応 |
|------|------|
| 候補未選択で押した場合 | 既存と同様「候補を選択してから〜」とメッセージ表示 |
| ZIP のみで 3ddb-pds に COPC が無い場合 | ビューア側で読み込み失敗となる。本アプリでは「Potreeで表示は COPC 形式のデータに対応しています」などの短い説明を UI に表示してもよい |

---

## 変更するファイル

| ファイル | 変更内容 |
|----------|----------|
| `index.html` | 「Potreeで表示」ボタン（`id="copcPotreeBtn"` など）を追加 |
| `app_github_pages.js` | 定数 `POTREE_COPC_VIEWER_BASE`、Potree ボタンの `click` ハンドラ、候補表示時にボタン有効化 |

---

## 完了条件

- 候補を 1 件選択した状態で「Potreeで表示」をクリックすると、potree-copc-viewer が別タブで開き、その COPC が表示されること
- ZIP のみの候補でも、reg_id から 3ddb-pds の COPC URL を組み立てて開くこと（開けない場合はビューア側の表示で十分）
- 候補 0 件または未選択時は「Potreeで表示」が押せないこと

---

## 備考

- 既存の「LAZダウンロード」はそのまま維持する
- 複数候補をまとめて Potree で開く（`?r=url1,url2`）は、今回のスコープ外とする（必要なら後で追加）
