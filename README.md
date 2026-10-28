# fastmcp-forge

[![PyPI version](https://img.shields.io/pypi/v/fastmcp-forge.svg)](https://pypi.org/project/fastmcp-forge/)
[![CI](https://github.com/johannschiffer/fastmcp-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/johannschiffer/fastmcp-forge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://python.org)
[![MCP Compliant](https://img.shields.io/badge/MCP-2024--11--05-purple.svg)](https://modelcontextprotocol.io)

<a href="https://glama.ai/mcp/servers/@johannschiffer/fastmcp-forge">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@johannschiffer/fastmcp-forge/badge" alt="fastmcp-forge MCP server" />
</a>

**FastMCP Forge** is a zero-dependency Python framework, CLI project scaffolder, and MCP server for building and testing **Model Context Protocol (2024-11-05)** servers over stdio or authenticated SSE transports.

## Features

- **`@app.tool` Decorator & Schema Inference**: Introspects function signatures (including `Optional[T]`, `list[T]`, `dict[K, V]`, and `from __future__ import annotations`) into JSON Schema definitions.
- **Built-in MCP Server & CLI Scaffolder**: Run `fastmcp-forge new <name>` from the terminal or connect `fastmcp-forge` directly to an MCP client to call `scaffold_project` and `validate_project`.
- **Authenticated SSE Transport Handler**: Constant-time API key and Bearer token verification (`hmac.compare_digest`), bounded session tracking with TTL expiration, and token-bucket rate limiting.

## Quickstart

### 1. Run as an MCP Server (`uvx`)

```json
{
  "mcpServers": {
    "fastmcp-forge": {
      "command": "uvx",
      "args": ["fastmcp-forge", "serve"]
    }
  }
}
```

Note: When invoked over a non-TTY pipe (`uvx fastmcp-forge` with no subcommand), `fastmcp-forge` automatically enters stdio MCP server mode.

### Built-in MCP Tools

| Tool | Description |
|---|---|
| `scaffold_project` | Generate a complete FastMCP server directory (`server.py`, `tests/test_server.py`, `pyproject.toml`, `README.md`, `requirements.txt`). |
| `validate_project` | Parse and verify an existing FastMCP project directory for syntax and structure. |

### 2. CLI Project Scaffolder

```bash
pip install fastmcp-forge
fastmcp-forge new analytics-mcp
fastmcp-forge validate ./analytics-mcp
```

### 3. Build a Custom Server in Python

```python
from fastmcp_forge.server import FastMCP

app = FastMCP(name="math-mcp", version="2.0.1")


@app.tool(description="Multiply two numbers")
def multiply(a: float, b: float) -> float:
    return a * b


if __name__ == "__main__":
    app.run()
```

## Genesis MCP Ecosystem

| Module | Description | Repository |
|---|---|---|
| **CrawlEngine MCP** | HTTP web extraction to clean Markdown, JSON-LD parsing, and proxy rotation | [GitHub](https://github.com/johannschiffer/crawlengine-mcp) |
| **BrowserBridge MCP** | Lightweight HTTP/DOM session automation with SHA-256 action receipts | [GitHub](https://github.com/johannschiffer/browserbridge-mcp) |
| **PgSafe MCP** | Read-only PostgreSQL/SQLite query guard, PII masking, and dry-run mutations | [GitHub](https://github.com/johannschiffer/pgsafe-mcp) |
| **OmniBridge MCP** | Multi-channel notification bus with SQLite retry queue | [GitHub](https://github.com/johannschiffer/omnibridge-mcp) |
| **SysFlow MCP** | Linux systemd inspection, confined log tailing, and port auditing | [GitHub](https://github.com/johannschiffer/sysflow-mcp) |
| **FastMCP Forge** | Zero-dependency FastMCP framework, CLI scaffolder, and SSE middleware | [GitHub](https://github.com/johannschiffer/fastmcp-forge) |

## Support

If you find this project useful, you can support maintenance on [Ko-fi](https://ko-fi.com/johannschiffer).

## License

MIT (c) 2026 [Johann Schiffer](https://github.com/johannschiffer)
