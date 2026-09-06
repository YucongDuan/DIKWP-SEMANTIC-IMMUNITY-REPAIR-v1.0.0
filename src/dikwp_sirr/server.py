from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from .analyzer import analyze
from .models import SemanticCase

MAX_BODY = 1_000_000


class Handler(BaseHTTPRequestHandler):
    server_version = "DIKWP-SIRR/1.0.0"

    def _send(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            self._send(200, {"status": "ok", "version": "1.0.0", "external_action_authority": 0})
        else:
            self._send(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/analyze":
            self._send(404, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY:
                self._send(413, {"error": "invalid_or_oversized_body"})
                return
            data = json.loads(self.rfile.read(length).decode("utf-8"))
            case = SemanticCase.from_dict(data)
            if not case.text.strip():
                self._send(400, {"error": "text_required"})
                return
            self._send(200, analyze(case).to_dict())
        except (ValueError, TypeError, json.JSONDecodeError) as exc:
            self._send(400, {"error": "invalid_request", "detail": str(exc)})

    def log_message(self, format: str, *args: object) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8765) -> None:
    if host not in {"127.0.0.1", "localhost", "::1"}:
        raise ValueError("Reference server only binds to a loopback address")
    server = ThreadingHTTPServer((host, port), Handler)
    print(json.dumps({"status": "listening", "host": host, "port": port, "external_action_authority": 0}))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
