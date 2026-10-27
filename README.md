# FastMCP Forge (Lite Edition)

[![Early Access $9](https://img.shields.io/badge/Early%20Access-%249%20Promo-orange.svg)](https://johanld.gumroad.com/l/genesis-enterprise-suite/EARLYACCESS)
> Enterprise Suite Pro: $9 Early Access (Regular $19) con código EARLYACCESS: https://johanld.gumroad.com/l/genesis-enterprise-suite/EARLYACCESS

> ### ⚡ Enterprise Infrastructure & Tooling
> | Component | Pricing | Delivery / Direct Access |
> |---|---|---|
> | **Starter Kit** | **Free ($0+)** | 25+ `.cursorrules`, `CLAUDE.md` stack rules & MCP config templates. [Download Free](https://johanld.gumroad.com/l/genesis-starter-kit) |
> | **Enterprise Suite Pro** | **$9 Early Access** ~~$19~~ | 6 Pro MCP Servers, Zero-Downtime DB migrations, Residential Proxies, Docker Compose Stack & Commercial License. [Get Early Access ($9)](https://johanld.gumroad.com/l/genesis-enterprise-suite/EARLYACCESS) |
> | **Config Generator** | **Free Web Tool** | Interactive visual config generator for Claude Desktop & Cursor. [Open Generator](https://johannschiffer.github.io/) |


<a href="https://glama.ai/mcp/servers/@johannschiffer/fastmcp-forge">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@johannschiffer/fastmcp-forge/badge" alt="fastmcp-forge MCP server" />
</a>



[![Release](https://img.shields.io/github/v/release/johannschiffer/fastmcp-forge?include_prereleases&color=blue)](https://github.com/johannschiffer/fastmcp-forge/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://python.org)
[![MCP Compliant](https://img.shields.io/badge/MCP-2024--11--05-purple.svg)](https://modelcontextprotocol.io)


> ### ⚡ Enterprise Infrastructure & Tooling
> | Package | Access | Features |
> |---|---|---|
> | **Starter Kit** | **Free ($0+)** | 25+ `.cursorrules`, `CLAUDE.md` stack rules & MCP config templates. [Download Free](https://johanld.gumroad.com/l/genesis-starter-kit) |
> | **Enterprise Suite Pro** | **$19 USD** | 6 Pro MCP Servers, Zero-Downtime DB migrations, Residential Proxies, Docker Compose Stack & Commercial License. [Get Pro License](https://johanld.gumroad.com/l/genesis-enterprise-suite/EARLYACCESS) |
> | **Config Generator** | **Free Web Tool** | Interactive visual config generator for Claude Desktop & Cursor. [Open Generator](https://johannschiffer.github.io/) |

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

## 💎 Need Enterprise Remote Deployment? Upgrade to FastMCP Forge Pro

Deploying MCP servers as remote team microservices, behind authentication proxies, or in production clouds?

| Feature | Lite (Open Source) | Enterprise Suite ($9 Early Access) |
|---|:---:|:---:|
| **@tool Schema Introspection** | ✅ | ✅ |
| **JSON-RPC 2.0 stdio Transport** | ✅ | ✅ |
| **CLI Project Scaffolding** | ✅ | ✅ |
| **Dual Transport: stdio + Remote SSE HTTP** | ❌ | ✅ |
| **Security & Auth Middleware** *(API Keys & Bearer Tokens)* | ❌ | ✅ |
| **Token Bucket Rate Limiter** | ❌ | ✅ |
| **Structured JSON Logs with Correlation IDs** | ❌ | ✅ |
| **Multi-Stage Docker & Compose** | ❌ | ✅ |
| **Full Pytest Suite & Enterprise Architecture Blueprint** | ❌ | ✅ |

👉 **[Get the Genesis Enterprise Suite ($9 Early Access)](https://johanld.gumroad.com/l/genesis-enterprise-suite/EARLYACCESS)**

---


## Solución Enterprise (Genesis Suite)

Para despliegues en producción y cargas intensivas con bypass de rate limits, soporte multi-tenant y configuraciones Docker precompiladas:

- **Bypass de Rate Limits & IP Rotation:** Scaffolder para servidores MCP de nivel empresarial con soporte SSE, stdio y middleware de autenticación.
- **Soporte Multi-Tenant & RBAC:** Control de accesos granular, gestión de secretos y auditoría criptográfica.
- **Docker Compose Stacks:** Contenedores precompilados y configuraciones listas para producción con orquestación autónoma.

👉 **[Genesis Enterprise Suite ($9 Early Access)](https://johanld.gumroad.com/l/genesis-enterprise-suite/EARLYACCESS)**  
📦 **[Genesis AI Engineering Starter Kit ($0+)](https://johanld.gumroad.com/l/genesis-starter-kit)**


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

[Live config builder](https://johannschiffer.github.io) | [Starter Kit, free](https://johanld.gumroad.com/l/genesis-starter-kit) | [Enterprise Suite, $9 Early Access](https://johanld.gumroad.com/l/genesis-enterprise-suite/EARLYACCESS)

## Recommended Infrastructure & Sponsorship

- **Sponsorship & Corporate Support**: Support continued maintenance and priority feature requests via [GitHub Sponsors](https://github.com/sponsors/johannschiffer).
- **Verified Cloud & Network Infrastructure**:
  - **High-Performance VPS & Nodes**: [Hetzner Cloud](https://www.hetzner.com/cloud) & [DigitalOcean](https://m.do.co/c/johannschiffer)
  - **Reliable Proxy Pool & IP Rotation**: [Webshare](https://www.webshare.io/) & [Bright Data](https://brightdata.com/)
  - **Documentation & Setup Guides**: [johannschiffer.github.io](https://johannschiffer.github.io/)