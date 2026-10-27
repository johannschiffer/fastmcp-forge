# fastmcp-forge (v1.0.0)

[![PyPI version](https://img.shields.io/badge/PyPI-v1.0.0-blue.svg)](https://pypi.org/project/fastmcp-forge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Support on Ko-fi](https://img.shields.io/badge/Support%20on-Ko--fi-ff5e5b.svg)](https://ko-fi.com/johannschiffer)

<a href="https://glama.ai/mcp/servers/@johannschiffer/fastmcp-forge">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@johannschiffer/fastmcp-forge/badge" alt="fastmcp-forge MCP server" />
</a>

[![Release](https://img.shields.io/github/v/release/johannschiffer/fastmcp-forge?include_prereleases&color=blue)](https://github.com/johannschiffer/fastmcp-forge/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://python.org)
[![MCP Compliant](https://img.shields.io/badge/MCP-2024--11--05-purple.svg)](https://modelcontextprotocol.io)

**FastMCP Forge** is an ergonomic framework and CLI scaffolding engine that enables Python developers to build, test, and package compliant **Model Context Protocol (MCP)** servers in seconds.

---

## Run without cloning

Execute directly via `uvx` (PyPI direct or Git source):

```bash
# Direct PyPI invocation:
uvx fastmcp-forge

# Or direct Git invocation (pre-PyPI sync):
uvx --from git+https://github.com/johannschiffer/fastmcp-forge fastmcp-forge
```

Claude Desktop / Cursor config entry:

```json
{
  "mcpServers": {
    "fastmcp-forge": {
      "command": "uvx",
      "args": [
        "fastmcp-forge"
      ]
    }
  }
}
```
*(Alternative for pre-indexation: replace `"args": ["fastmcp-forge"]` with `"args": ["--from", "git+https://github.com/johannschiffer/fastmcp-forge", "fastmcp-forge"]`)*

[![CI](https://github.com/johannschiffer/fastmcp-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/johannschiffer/fastmcp-forge/actions/workflows/ci.yml)

## ⚡ The Problem: MCP Boilerplate Burnout

In 2026, every AI developer is building MCP servers to connect tools to **Claude Desktop**, **Cursor**, **Windsurf**, and **Antigravity**. However, writing raw JSON-RPC 2.0 handlers from scratch requires:
- Manually parsing JSON schemas for tool arguments.
- Handling error codes (-32600, -32601, -32602, -32000).
- Managing `sys.stdin` and `sys.stdout` stream buffers.
- Writing test harnesses to mock agent tool invocations.

**FastMCP Forge** gives you an intuitive `@app.tool` decorator that introspects function signatures, infers types, generates valid schemas, and creates automated test suites instantly.

---

## 🛠️ Code Example: Build an MCP Server in 10 Lines

```python
from fastmcp_forge.server import FastMCP

app = FastMCP(name="math-mcp", version="1.0.0")

@app.tool(description="Multiply two numbers safely")
def multiply(a: float, b: float) -> float:
    return a * b

if __name__ == "__main__":
    app.run_stdio()
```

---

## 🚀 CLI Project Scaffolder

Generate a full production-ready project with tests in 1 second:

```bash
python -m fastmcp_forge.cli new analytics-mcp
```

Output:
```text
[OK] Created new FastMCP project 'analytics-mcp'
Generated files:
  - server.py
  - tests/test_server.py
  - README.md
  - requirements.txt
```

---

## 🖥️ Client Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["server.py"],
      "cwd": "/path/to/my-server"
    }
  }
}
```

---

## Genesis MCP Ecosystem

| Module | Description | Repository |
|---|---|---|
| **CrawlEngine MCP** | Anti-bot web scraping, clean Markdown, proxy rotation, and TLS evasion | [GitHub](https://github.com/johannschiffer/crawlengine-mcp) |
| **BrowserBridge MCP** | Deterministic headless browser automation with cryptographic action receipts | [GitHub](https://github.com/johannschiffer/browserbridge-mcp) |
| **PgSafe MCP** | Zero-trust PostgreSQL/SQLite guard, live PII masking, and schema inspection | [GitHub](https://github.com/johannschiffer/pgsafe-mcp) |
| **OmniBridge MCP** | Multi-channel notification bus with persistent SQLite queue | [GitHub](https://github.com/johannschiffer/omnibridge-mcp) |
| **SysFlow MCP** | Safe Linux administration, systemd automation, and port auditing | [GitHub](https://github.com/johannschiffer/sysflow-mcp) |
| **FastMCP Forge** | Production FastMCP server scaffolder with stdio and SSE middleware | [GitHub](https://github.com/johannschiffer/fastmcp-forge) |

## Support

If you find this project helpful, you can support its ongoing maintenance on [Ko-fi](https://ko-fi.com/johannschiffer).

## License

MIT © 2026 [Johann Schiffer](https://github.com/johannschiffer)
