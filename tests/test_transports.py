"""
Unit tests for FastMCP Forge SSE Transport.
"""
import json
import pytest
from fastmcp_forge.server import FastMCP
from fastmcp_forge.transports.sse import SSETransportHandler

@pytest.fixture
def mcp_app():
    app = FastMCP(name="sse-test-server", version="1.0.0")

    @app.tool()
    def add(a: int, b: int) -> int:
        return a + b

    return app

def test_sse_connect_and_post_unauthenticated(mcp_app):
    # Public mode (no key required)
    handler = SSETransportHandler(mcp_app)

    # 1. Connect SSE
    conn_resp = handler.handle_sse_connect(headers={}, client_ip="192.168.1.10")
    assert conn_resp["status_code"] == 200
    assert "session_id" in conn_resp
    assert "event: endpoint" in conn_resp["sse_event"]
    assert conn_resp["content_type"] == "text/event-stream"
    session_id = conn_resp["session_id"]

    # 2. Post JSON-RPC request to session
    req_json = {
        "jsonrpc": "2.0",
        "id": 100,
        "method": "tools/call",
        "params": {"name": "add", "arguments": {"a": 7, "b": 3}}
    }
    post_resp = handler.handle_post_message(
        session_id=session_id,
        request_json=req_json,
        headers={},
        client_ip="192.168.1.10"
    )
    assert post_resp["status_code"] == 200
    body = json.loads(post_resp["body"])
    assert body["id"] == 100
    assert body["result"]["content"][0]["text"] == "10"

def test_sse_with_authentication(mcp_app):
    handler = SSETransportHandler(mcp_app, api_key="secret-token-777")

    # Connect without auth -> 401
    unauth_conn = handler.handle_sse_connect(headers={})
    assert unauth_conn["status_code"] == 401

    # Connect with valid auth -> 200
    auth_conn = handler.handle_sse_connect(headers={"X-Api-Key": "secret-token-777"})
    assert auth_conn["status_code"] == 200
    session_id = auth_conn["session_id"]

    # Post message without auth -> 401
    bad_post = handler.handle_post_message(session_id, {}, headers={})
    assert bad_post["status_code"] == 401

    # Post message with valid auth -> 200
    good_post = handler.handle_post_message(
        session_id,
        {"jsonrpc": "2.0", "id": 1, "method": "ping"},
        headers={"X-Api-Key": "secret-token-777"}
    )
    assert good_post["status_code"] == 200
