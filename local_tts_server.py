"""
本地 TTS 测试服务器 — 多线程版
用法：python local_tts_server.py
然后浏览器打开 http://127.0.0.1:8080/pronunciation-phonics.html
"""
import http.server
import urllib.request
import urllib.parse
import urllib.error
import os
import socketserver

PORT = 8080
DIR = os.path.dirname(os.path.abspath(__file__))


class TTSHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIR, **kwargs)

    def do_GET(self):
        # /tts.php?q=xxx -> 代理到百度 TTS
        if self.path.startswith("/tts.php"):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            text = params.get("q", [""])[0].strip()

            if not text:
                self.send_error(400, "missing q")
                return

            text = text[:300]
            url = (
                "https://fanyi.baidu.com/gettts?lan=uk&text="
                + urllib.parse.quote(text)
                + "&spd=3&source=web"
            )

            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Referer": "https://fanyi.baidu.com/",
                    "Accept": "audio/mpeg,audio/*",
                },
            )

            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    audio = resp.read()
                if not audio or len(audio) < 100:
                    self.send_error(502, "empty")
                    return
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.send_header("Content-Length", str(len(audio)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Cache-Control", "public, max-age=86400")
                self.end_headers()
                self.wfile.write(audio)
            except Exception as e:
                # 用 ASCII 避免 latin-1 编码报错
                msg = str(e)[:80].encode("ascii", "replace").decode("ascii")
                self.send_error(502, msg)
            return

        # 其他请求 -> 静态文件
        super().do_GET()


if __name__ == "__main__":
    # 多线程服务器，支持浏览器并发请求
    server = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), TTSHandler)
    server.allow_reuse_address = True
    print(f"本地 TTS 测试服务器已启动 (多线程)")
    print(f"打开浏览器: http://127.0.0.1:{PORT}/pronunciation-phonics.html")
    print(f"按 Ctrl+C 停止")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
