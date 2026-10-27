"""
FastMCP Server Engine (Enterprise Pro Edition).
Implements official Model Context Protocol (2024-11-05) supporting both
local stdio and remote HTTP/SSE transports, with decorator registry and auto-schemas.
"""

import sys
import json
import inspect
import logging
from typing import Callable, Dict, Any, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [FastMCP-Pro] %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("FastMCPProServer")

class FastMCP:
    def __init__(self, name: str = "fastmcp-server", version: str = "1.0.0", description: str = ""):
        self.name = name
        self.version = version
        self.description = description
        self.tools: Dict[str, Dict[str, Any]] = {}

    def tool(self, name: Optional[str] = None, description: Optional[str] = None):
        """Decorator to register a Python function as an MCP tool."""
        def decorator(func: Callable):
            tool_name = name or func.__name__
            tool_desc = description or (func.__doc__.strip() if func.__doc__ else f"Tool {tool_name}")

            sig = inspect.signature(func)
            properties = {}
            required = []

            type_map = {
                str: "string",
                int: "integer",
                float: "number",
                bool: "boolean",
                list: "array",
                dict: "object"
            }

            for param_name, param in sig.parameters.items():
                if param_name in ("self", "cls"):
                    continue

                schema_type = type_map.get(param.annotation, "string") if param.annotation != inspect.Parameter.empty else "string"
                properties[param_name] = {
                    "type": schema_type,
                    "description": f"Parameter {param_name}"
                }
                if param.default == inspect.Parameter.empty:
                    required.append(param_name)

            self.tools[tool_name] = {
                "name": tool_name,
                "description": tool_desc,
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                },
                "func": func
            }
            return func
        return decorator

    def get_tools_definition(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t["name"],
                "description": t["description"],
                "inputSchema": t["inputSchema"]
            }
            for t in self.tools.values()
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        if name not in self.tools:
            raise KeyError(f"Tool not found: '{name}'")
        func = self.tools[name]["func"]
        return func(**arguments)

    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if req_id is None:
            if method == "notifications/initialized":
                logger.info("Client initialization handshake confirmed.")
            return None

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": self.name,
                        "version": self.version
                    }
                }
            }

        elif method == "ping":
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": self.get_tools_definition()}
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            try:
                result = self.call_tool(tool_name, tool_args)
                formatted_text = result if isinstance(result, str) else json.dumps(result, indent=2, ensure_ascii=False)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": formatted_text}],
                        "isError": False
                    }
                }
            except KeyError as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": str(e)}
                }
            except TypeError as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": f"Invalid params: {str(e)}"}
                }
            except Exception as e:
                logger.error(f"Error calling tool {tool_name}: {e}")
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }
        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }

    def run_stdio(self):
        """Standard IO event loop reading JSON-RPC lines from stdin."""
        logger.info(f"Starting {self.name} v{self.version} stdio listener...")
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                request = json.loads(line)
                response = self.handle_request(request)
                if response is not None:
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse error: {e}")
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"}
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()
            except Exception as e:
                logger.error(f"Unexpected stdio exception: {e}")

    def create_sse_transport(self, api_key: Optional[str] = None, bearer_token: Optional[str] = None):
        """Creates an authenticated SSE transport handler for remote HTTP deployments."""
        from .transports.sse import SSETransportHandler
        return SSETransportHandler(self, api_key=api_key, bearer_token=bearer_token)
