#!/usr/bin/env python3
"""
静的ファイル配信 + 3DDB API 用 CORS プロキシ（ローカル開発で CORS エラーを避けるため）
使い方: プロジェクトルートで python scripts/serve_with_3ddb_proxy.py
        ブラウザで http://localhost:8000/index.html を開き、
        「3DDB COPC取得」で「プロキシ経由で検索」にチェックを入れて検索
"""
import http.server
import urllib.request
import urllib.error
import sys
import os

PORT = 8000
ALLOWED_HOSTS = ('gsvrg.ipri.aist.go.jp', 'grt.ipri.aist.go.jp')


class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/api/3ddb_proxy?'):
            self._handle_proxy()
            return
        super().do_GET()

    def _handle_proxy(self):
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        target = qs.get('url', [None])[0]
        if not target:
            self.send_error(400, 'Missing url parameter')
            return
        if not any(h in target for h in ALLOWED_HOSTS):
            self.send_error(403, 'Proxy only allows 3DDB API hosts')
            return
        try:
            req = urllib.request.Request(target, headers={'User-Agent': 'yokutsukau_pointcloud/1'})
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read()
                content_type = resp.headers.get('Content-Type', 'application/json')
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Proxy error: {e.code}'.encode())
            return
        except Exception as e:
            self.send_error(502, f'Proxy error: {e}')
            return
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    print(f"""
========================================
静的ファイル + 3DDB API プロキシ
========================================
http://localhost:{PORT}/

  index.html を開き、「3DDB COPC取得」で
  「プロキシ経由で検索」にチェックを入れると
  CORS エラーを避けて検索できます。

終了: Ctrl+C
========================================
""", flush=True)
    with http.server.HTTPServer(("", PORT), ProxyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n終了しました")


if __name__ == '__main__':
    main()
