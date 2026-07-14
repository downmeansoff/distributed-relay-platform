"""Заглушка единого API платформы.

В реальном сервисе здесь общий контракт для веб-интерфейса, мобильных приложений
и Telegram-бота. Тут оставлены только health-эндпоинт и минимальный роут, чтобы
стенд поднимался и проходил smoke-проверки в CI.
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

APP_ENV = os.getenv("APP_ENV", "local")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"status": "ok", "env": APP_ENV})
        elif self.path == "/api/v1/nodes":
            # В реальности — актуальное состояние relay-узлов из БД/мониторинга.
            self._json(200, {"nodes": [], "note": "sanitized demo"})
        else:
            self._json(404, {"error": "not found"})

    def _json(self, code, payload):
        import json
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # тише в логах
        pass


def main(host="0.0.0.0", port=8000):
    HTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    main()
