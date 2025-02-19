import json
import time
import http.server
import socketserver
import os

# 設定
PORT = 8000
BASE_DIR = "data"  # JSONファイルが格納されているディレクトリ
DELAY_FILE = "delay.txt"  # 遅延秒数を指定するファイル

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self): 
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def do_DELETE(self):
        self.handle_request()

    def handle_request(self):
        # 遅延時間の取得
        delay = 0
        try:
            with open(DELAY_FILE, "r", encoding="utf-8") as f:
                delay = float(f.read().strip())  # 数値を読み取る
        except (FileNotFoundError, ValueError):
            pass  # ファイルがない場合や異常な値なら遅延なし

        # 現在の日時を出力
        print(time.strftime("[%Y/%m/%d %H:%M:%S]", time.localtime()) + f" Request received: {self.path} (delay: {delay} sec)")
        time.sleep(delay)  # 遅延を適用

        # リクエストされたパスに対応するJSONファイルの取得と送信
        json_file_path = os.path.join(BASE_DIR, self.path.lstrip("/") + ".json")
        try:
            with open(json_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"JSON file not found")

    def log_message(self, format, *args):
        # カスタムログフォーマット
        log_message = f"[{time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())}] {self.address_string()} {format % args}"
        print(log_message)

# `ThreadingTCPServer` を使用して並列処理を可能にする
class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# サーバー起動
with ThreadingTCPServer(("0.0.0.0", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT} with threading")
    httpd.serve_forever()