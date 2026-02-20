# ローカルでの起動と GitHub Pages での公開

※アプリの操作（ファイル選択→実行→ダウンロード）はライブデモでそのまま試せます。以下は開発・検証用の起動・公開手順です。

## ローカルで試す

```bash
python -m http.server 8000
# ブラウザで http://localhost:8000/index.html
```

## GitHub Pagesで公開する

1. ルートに `index.html`（ブラウザ完結版）を配置済み。`app_github_pages.js` をアップロード
2. GitHub Pages を有効化
3. `https://<username>.github.io/yokutsukau_pointcloud/` でアクセス

**⚠️ 注意**: 必ずルート（`/` または `index.html`）を開いてください。`/variants/index.html` はサーバー版用のため、GitHub Pages では API がなく `Failed to fetch` になります。
