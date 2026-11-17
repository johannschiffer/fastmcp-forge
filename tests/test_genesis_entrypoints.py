import json
import sqlite3
import subprocess
import sys
from pathlib import Path

from fastmcp_forge.scaffolder import ProjectScaffolder
from fastmcp_forge.server import FastMCP


def test_notice_is_silent():
    res = subprocess.run([sys.executable, "-c", "import fastmcp_forge._genesis; fastmcp_forge._genesis.print_upgrade_notice()"], capture_output=True, text=True)
    assert res.stderr == ""
    assert res.stdout == ""
    import fastmcp_forge._genesis
    assert fastmcp_forge._genesis.NOTICE == ""


def test_blackbox_bridge_and_scaffold_instrumentation(monkeypatch, tmp_path):
    wal_db = tmp_path / "wal.sqlite"
    monkeypatch.setenv("BLACKBOX_DB_PATH", str(wal_db))

    app = FastMCP(name="demo-forge-server", version="2.1.0")

    @app.tool()
    def ping_tool(val: str) -> dict:
        return {"pong": val}

    assert app.call_tool("ping_tool", {"val": "ok"}) == {"pong": "ok"}

    wal_conn = sqlite3.connect(str(wal_db))
    rows = wal_conn.execute(
        "SELECT event_type, source, status, payload FROM blackbox_events ORDER BY id ASC;"
    ).fetchall()
    wal_conn.close()

    assert len(rows) == 1
    assert rows[0][0] == "MCP_TOOL"
    assert rows[0][1] == "demo-forge-server"
    assert rows[0][2] == "ok"
    assert json.loads(rows[0][3])["tool"] == "ping_tool"

    scaffolded = ProjectScaffolder.create_project("instrumented-mcp", target_dir=str(tmp_path))
    proj_dir = Path(scaffolded["path"])
    server_src = (proj_dir / "server.py").read_text(encoding="utf-8")
    reqs_src = (proj_dir / "requirements.txt").read_text(encoding="utf-8")
    assert "auto_instrument" in server_src
    assert "genesis-blackbox>=0.6.0" in reqs_src
    assert "fastmcp-forge>=2.1.0" in reqs_src
