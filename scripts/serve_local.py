#!/usr/bin/env python3
"""静的ファイル用ローカルサーバー（テスト用）。"""
import http.server
import sys

PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

if __name__ == "__main__":
    import os
    # プロジェクトルートで起動する想定（このスクリプトは scripts/ にある）
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    with http.server.HTTPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving at http://127.0.0.1:{PORT}/", flush=True)
        print(f"  index.html -> http://127.0.0.1:{PORT}/index.html", flush=True)
        sys.stdout.flush()
        sys.stderr.flush()
        httpd.serve_forever()
