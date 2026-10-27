# fastmcp-forge (v2.0.0)

[![PyPI version](https://img.shields.io/badge/PyPI-v2.0.0-blue.svg)](https://pypi.org/project/fastmcp-forge/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Support on Ko-fi](https://img.shields.io/badge/Support%20on-Ko--fi-ff5e5b.svg)](https://ko-fi.com/johannschiffer)

> **100% Free & Open Source (MIT)**: All features, proxy rotation, migration simulation, Docker stacks, and recipes are completely unlocked. Support open development on [Ko-fi](https://ko-fi.com/johannschiffer).

> ### ⚡ Open Source Ecosystem & Community Tools
> | Resource | Access | Description |
> |---|---|---|
> | **Ruleset Bundle** | **100% Free** | 55+ production rulesets & MCP config templates. [Download Free](https://johannschiffer.github.io/) |
> | **Support & Donate** | **Ko-fi** | Support open-source maintenance. [Support on Ko-fi](https://ko-fi.com/johannschiffer) |

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

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

## Recommended Infrastructure

VPS hosting that work well with FastMCP Forge. Some links are referral links.

- [Hetzner Cloud](https://www.hetzner.com/cloud)
- [DigitalOcean](https://www.digitalocean.com/)

## Genesis MCP Ecosystem

| Module | What it does | Repo |
|---|---|---|
| **CrawlEngine MCP** | Anti-bot web scraping, clean Markdown, proxy rotation and TLS evasion | [GitHub](https://github.com/johannschiffer/crawlengine-mcp) |
| **BrowserBridge MCP** | Deterministic headless browser automation with cryptographic action receipts | [GitHub](https://github.com/johannschiffer/browserbridge-mcp) |
| **PgSafe MCP** | Zero-trust PostgreSQL/SQLite guard, live PII masking, zero-downtime migration checks | [GitHub](https://github.com/johannschiffer/pgsafe-mcp) |
| **OmniBridge MCP** | Multi-channel notification and webhook bus with a persistent SQLite WAL queue | [GitHub](https://github.com/johannschiffer/omnibridge-mcp) |
| **SysFlow MCP** | Safe Linux administration plane: systemd, port audit, isolated execution | [GitHub](https://github.com/johannschiffer/sysflow-mcp) |
| **FastMCP Forge** (this repo) | Production MCP server scaffolder: stdio, SSE and auth middleware | [GitHub](https://github.com/johannschiffer/fastmcp-forge) |

[Live config builder](https://johannschiffer.github.io) | [GitHub Profile](https://github.com/johannschiffer) | [Support on Ko-fi ☕](https://ko-fi.com/johannschiffer)

## Recommended Infrastructure & Sponsorship

- **Sponsorship & Corporate Support**: Support continued maintenance and priority feature requests via [GitHub Sponsors](https://github.com/sponsors/johannschiffer).
- **Verified Cloud & Network Infrastructure**:
  - **High-Performance VPS & Nodes**: [Hetzner Cloud](https://www.hetzner.com/cloud) & [DigitalOcean](https://m.do.co/c/johannschiffer)
  - **Reliable Proxy Pool & IP Rotation**: [Webshare](https://www.webshare.io/) & [Bright Data](https://brightdata.com/)
  - **Documentation & Setup Guides**: [johannschiffer.github.io](https://johannschiffer.github.io/)

---

## Support

[![Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/johannschiffer)

If you find this tool helpful, you can support its maintenance via Ko-fi.
