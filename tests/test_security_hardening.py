"""
Security and protocol hardening tests for fastmcp-forge v2.0.1.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

import pytest

from fastmcp_forge import __version__
from fastmcp_forge.cli import build_forge_mcp_server
from fastmcp_forge.middleware.auth import AuthMiddleware
from fastmcp_forge.middleware.rate_limiter import RateLimiter
from fastmcp_forge.scaffolder import ProjectScaffolder
from fastmcp_forge.server import FastMCP
from fastmcp_forge.transports.sse import SSETransportHandler


def test_future_annotations_and_generic_schema_inference():
    app = FastMCP("typed-mcp")

    @app.tool()
    def summarize(
        tags: List[str],
        metadata: Dict[str, str],
        limit: Optional[int] = None,
        flag: bool = True,
    ) -> dict:
        return {"tags": tags, "metadata": metadata, "limit": limit, "flag": flag}

    schema = app.get_tools_definition()[0]["inputSchema"]
    props = schema["properties"]
    assert props["tags"]["type"] == "array"
    assert props["metadata"]["type"] == "object"
    assert props["limit"]["type"] == "integer"
    assert props["flag"]["type"] == "boolean"
    assert schema["required"] == ["tags", "metadata"]


def test_malformed_jsonrpc_inputs_handled_safely():
    app = FastMCP("safe-mcp")

    @app.tool()
    def ping_tool() -> str:
        return "pong"

    # Non-dict batch/array payload
    resp_list = app.handle_request([1, 2, 3])  # type: ignore[arg-type]
    assert resp_list["error"]["code"] == -32600

    # Null params and null arguments
    resp_null_args = app.handle_request(
        {"jsonrpc": "2.0", "id": 10, "method": "tools/call", "params": {"name": "ping_tool", "arguments": None}}
    )
    assert resp_null_args["result"]["isError"] is False
    assert resp_null_args["result"]["content"][0]["text"] == "pong"


def test_scaffolder_blocks_path_traversal_and_generated_tests_pass(tmp_path):
    with pytest.raises(ValueError):
        ProjectScaffolder.create_project("../escape", target_dir=str(tmp_path))
    with pytest.raises(ValueError):
        ProjectScaffolder.create_project("bad/name", target_dir=str(tmp_path))

    res = ProjectScaffolder.create_project("demo-service", target_dir=str(tmp_path))
    validation = ProjectScaffolder.validate_project(res["path"])
    assert validation["valid"] is True

    repo_root = str(Path(__file__).resolve().parents[1])
    env = {**os.environ, "PYTHONPATH": repo_root}
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=res["path"],
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout


def test_sse_rejects_unknown_session_and_bounds_sessions():
    app = FastMCP("sse-hardened")
    handler = SSETransportHandler(app, max_sessions=3)

    unregistered = handler.handle_post_message(
        session_id="non-existent-session",
        request_json={"jsonrpc": "2.0", "id": 1, "method": "ping"},
        headers={},
    )
    assert unregistered["status_code"] == 404

    sids = [handler.handle_sse_connect(headers={})["session_id"] for _ in range(5)]
    assert len(handler.sessions) <= 3
    assert sids[-1] in handler.sessions


def test_auth_case_insensitive_bearer_and_bounded_rate_limiter():
    auth = AuthMiddleware(bearer_token="top-secret")
    ok, _ = auth.verify_headers({"Authorization": "bearer top-secret"})
    assert ok is True

    limiter = RateLimiter(rate_per_sec=5.0, burst=2, max_buckets=3)
    for idx in range(6):
        limiter.allow_request(f"ip-{idx}")
    assert len(limiter.buckets) <= 3


def test_cli_non_tty_serves_mcp_initialize_and_version():
    repo_root = str(Path(__file__).resolve().parents[1])
    env = {**os.environ, "PYTHONPATH": repo_root}
    ver = subprocess.run(
        [sys.executable, "-m", "fastmcp_forge", "--version"],
        env=env,
        capture_output=True,
        text=True,
    )
    assert ver.returncode == 0
    assert __version__ in ver.stdout

    forge_server = build_forge_mcp_server()
    tools = [t["name"] for t in forge_server.get_tools_definition()]
    assert "scaffold_project" in tools
    assert "validate_project" in tools

    init_line = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"}) + "\n"
    proc = subprocess.run(
        [sys.executable, "-m", "fastmcp_forge"],
        input=init_line,
        env=env,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    payload = json.loads(proc.stdout.strip())
    assert payload["result"]["serverInfo"]["name"] == "fastmcp-forge"
    assert payload["result"]["serverInfo"]["version"] == __version__
