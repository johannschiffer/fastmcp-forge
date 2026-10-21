# FastMCP Forge (Lite Edition)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-brightgreen.svg)](https://python.org)
[![MCP Compliant](https://img.shields.io/badge/MCP-2024--11--05-purple.svg)](https://modelcontextprotocol.io)

**FastMCP Forge** is an ergonomic framework and CLI scaffolding engine that enables Python developers to build, test, and package compliant **Model Context Protocol (MCP)** servers in seconds.

---

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

| Feature | Lite (Open Source) | Pro ($14.99 USD) |
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

👉 **[Get FastMCP Forge Pro on Gumroad ($14.99)](https://johanld.gumroad.com/l/fastmcp-forge-pro)**

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
