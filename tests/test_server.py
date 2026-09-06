import json
import threading
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer

from dikwp_sirr.server import Handler


def test_local_api_health_and_analysis():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        conn = HTTPConnection(host, port, timeout=5)
        conn.request("GET", "/health")
        response = conn.getresponse()
        health = json.loads(response.read())
        assert response.status == 200
        assert health["external_action_authority"] == 0
        body = json.dumps({"text": "可能对部分人有帮助，需要结合具体情况。"}, ensure_ascii=False).encode()
        conn.request("POST", "/analyze", body=body, headers={"Content-Type": "application/json", "Content-Length": str(len(body))})
        response = conn.getresponse()
        result = json.loads(response.read())
        assert response.status == 200
        assert result["invariants"]["external_action_authority_zero"]
    finally:
        server.shutdown()
        server.server_close()
