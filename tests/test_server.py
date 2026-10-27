"""
Unit tests for FastMCP Server Engine.
Verifies tool decorator, schema inference, JSON-RPC 2.0 protocol dispatch, and error codes.
"""
import pytest
from fastmcp_forge.server import FastMCP

def test_fastmcp_tool_registration():
    app = FastMCP(name="test-server", version="1.0.0")

    @app.tool(name="multiply", description="Multiply two numbers")
    def multiply_nums(x: float, y: float) -> float:
        return x * y

    tools = app.get_tools_definition()
    assert len(tools) == 1
    tool = tools[0]
    assert tool["name"] == "multiply"
    assert tool["description"] == "Multiply two numbers"
    assert tool["inputSchema"]["type"] == "object"
    assert "x" in tool["inputSchema"]["properties"]
    assert "y" in tool["inputSchema"]["properties"]
    assert "x" in tool["inputSchema"]["required"]
    assert "y" in tool["inputSchema"]["required"]

def test_fastmcp_tool_execution():
    app = FastMCP()

    @app.tool()
    def greet(name: str, shout: bool = False) -> str:
        msg = f"Hello, {name}!"
        return msg.upper() if shout else msg

    res = app.call_tool("greet", {"name": "Alice"})
    assert res == "Hello, Alice!"

    res_shout = app.call_tool("greet", {"name": "Bob", "shout": True})
    assert res_shout == "HELLO, BOB!"

def test_fastmcp_jsonrpc_initialize():
    app = FastMCP(name="demo-mcp", version="2.1.0")
    req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05"}
    }
    resp = app.handle_request(req)
    assert resp["jsonrpc"] == "2.0"
    assert resp["id"] == 1
    assert resp["result"]["protocolVersion"] == "2024-11-05"
    assert resp["result"]["serverInfo"]["name"] == "demo-mcp"
    assert resp["result"]["serverInfo"]["version"] == "2.1.0"

def test_fastmcp_jsonrpc_ping():
    app = FastMCP()
    req = {"jsonrpc": "2.0", "id": 2, "method": "ping"}
    resp = app.handle_request(req)
    assert resp["jsonrpc"] == "2.0"
    assert resp["id"] == 2
    assert resp["result"] == {}

def test_fastmcp_jsonrpc_tools_list_and_call():
    app = FastMCP()

    @app.tool()
    def echo(text: str) -> str:
        return f"echo: {text}"

    # tools/list
    list_req = {"jsonrpc": "2.0", "id": 3, "method": "tools/list"}
    list_resp = app.handle_request(list_req)
    assert list_resp["id"] == 3
    assert len(list_resp["result"]["tools"]) == 1
    assert list_resp["result"]["tools"][0]["name"] == "echo"

    # tools/call success
    call_req = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {"name": "echo", "arguments": {"text": "hello mcp"}}
    }
    call_resp = app.handle_request(call_req)
    assert call_resp["id"] == 4
    assert call_resp["result"]["isError"] is False
    assert call_resp["result"]["content"][0]["text"] == "echo: hello mcp"

def test_fastmcp_jsonrpc_errors():
    app = FastMCP()

    @app.tool()
    def fail_op(a: int):
        if a < 0:
            raise ValueError("Negative value forbidden")
        return a

    # Tool not found: -32601
    nf_req = {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "unknown_tool"}}
    nf_resp = app.handle_request(nf_req)
    assert nf_resp["error"]["code"] == -32601

    # Method not found: -32601
    bad_meth = {"jsonrpc": "2.0", "id": 6, "method": "invalid/method"}
    bad_resp = app.handle_request(bad_meth)
    assert bad_resp["error"]["code"] == -32601

    # Tool error: -32000
    err_req = {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": "fail_op", "arguments": {"a": -5}}}
    err_resp = app.handle_request(err_req)
    assert err_resp["error"]["code"] == -32000
    assert "Negative value forbidden" in err_resp["error"]["message"]

def test_fastmcp_notification_handling():
    app = FastMCP()
    notif = {"jsonrpc": "2.0", "method": "notifications/initialized"}
    resp = app.handle_request(notif)
    assert resp is None
