# -*- coding: utf-8 -*-
"""Serves the Magrabi best-sellers page and pulls the live sales report."""
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

HOST = "127.0.0.1"
PORT = 18923
REPORT_URL = (
    "https://appsc.magrabi.com/MagrabiPOS-Reports/ReportInfo?r="
    "6f6f3a410c666d7d6f7adc796845844752484fff5225676bd2f65f4270e02856"
    "ed53a7b71dc05d46ac5d2bf3a5d9946fa32fba8575cec528c6d6a19d0e16e5e9"
    "8d3ccf1fb2cd1ddd5da565ab4c9e3ca17b4d9aafab33bfc94e858dbec3ceabda"
    "97234b179bbef1140be4da12aa06a6bded089f7f6a8620aa&__format=xls"
)


class Handler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self):
        if self.path.split("?", 1)[0] == "/sales-report.xls":
            self.proxy_report()
            return
        super().do_GET()

    def proxy_report(self):
        try:
            req = urllib.request.Request(REPORT_URL, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=120) as response:
                data = response.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/vnd.ms-excel")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except Exception as exc:
            body = str(exc).encode("utf-8", "replace")
            self.send_response(502)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)


if __name__ == "__main__":
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()
