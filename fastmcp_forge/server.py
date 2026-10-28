"""
FastMCP Server Engine.
Implements Model Context Protocol (2024-11-05) over local stdio and HTTP/SSE
transports with decorator tool registration and JSON Schema type inference.
"""

import inspect
import json
import logging
import sys
import types
from typing import Any, Callable, Dict, List, Optional, Union, get_args, get_origin

from . import __version__

logger = logging.getLogger("FastMCPServer")


def _infer_schema_type(annotation: Any) -> str:
    """Map Python type annotations (including Optional and PEP 585 generics) to JSON Schema types."""
    if annotation is inspect.Parameter.empty or annotation is None or annotation is Any:
        return "string"

    origin = get_origin(annotation)
    if origin in (Union, getattr(types, "UnionType", Union)):
        non_none = [arg for arg in get_args(annotation) if arg is not type(None)]
        if len(non_none) == 1:
            return _infer_schema_type(non_none[0])
        return "string"

    if origin in (list, tuple, set, frozenset):
        return "array"
    if origin is dict:
        return "object"

    if annotation is bool:
        return "boolean"
    if annotation is int:
        return "integer"
    if annotation is float:
        return "number"
    if annotation is str:
        return "string"
    if annotation in (list, tuple, set, frozenset):
        return "array"
    if annotation is dict:
        return "object"

    return "string"


class FastMCP:
    def __init__(self, name: str = "fastmcp-server", version: str = __version__, description: str = ""):
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
            try:
                resolved_hints = inspect.get_annotations(func, eval_str=True)
            except Exception:
                resolved_hints = {}

            properties: Dict[str, Any] = {}
            required: List[str] = []

            for param_name, param in sig.parameters.items():
                if param_name in ("self", "cls"):
                    continue
                if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                    continue

                annotation = resolved_hints.get(param_name, param.annotation)
                schema_type = _infer_schema_type(annotation)
                properties[param_name] = {
                    "type": schema_type,
                    "description": f"Parameter {param_name}",
                }
                if param.default is inspect.Parameter.empty:
                    required.append(param_name)

            self.tools[tool_name] = {
                "name": tool_name,
                "description": tool_desc,
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
                "func": func,
            }
            return func
        return decorator

    def get_tools_definition(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": t["name"],
                "description": t["description"],
                "inputSchema": t["inputSchema"],
            }
            for t in self.tools.values()
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        if not name or name not in self.tools:
            raise KeyError(f"Tool not found: '{name}'")
        func = self.tools[name]["func"]
        return func(**arguments)

    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not isinstance(request, dict):
            return {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32600, "message": "Invalid Request: expected JSON object"},
            }

        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params")
        if params is None:
            params = {}
        elif not isinstance(params, dict):
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": "Invalid params: expected JSON object"},
            }

        if req_id is None and "id" not in request:
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
                        "version": self.version,
                    },
                },
            }

        if method == "ping":
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}

        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": self.get_tools_definition()},
            }

        if method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments")
            if tool_args is None:
                tool_args = {}
            elif not isinstance(tool_args, dict):
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": "Invalid params: 'arguments' must be an object"},
                }

            try:
                result = self.call_tool(tool_name, tool_args)
                formatted_text = (
                    result if isinstance(result, str) else json.dumps(result, indent=2, ensure_ascii=False)
                )
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [{"type": "text", "text": formatted_text}],
                        "isError": False,
                    },
                }
            except KeyError as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": str(e)},
                }
            except TypeError as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32602, "message": f"Invalid params: {str(e)}"},
                }
            except Exception as e:
                logger.error("Error calling tool %s: %s", tool_name, e)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)},
                }

        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Method not found: {method}"},
        }

    def run(self, transport: str = "stdio") -> None:
        """Run the FastMCP server using the selected transport."""
        if transport != "stdio":
            raise ValueError(f"Unsupported direct run transport '{transport}'. Use create_sse_transport() for SSE.")
        self.run_stdio()

    def run_stdio(self) -> None:
        """Standard IO event loop reading JSON-RPC lines from stdin."""
        if not logging.getLogger().handlers and not logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s [%(levelname)s] [FastMCP] %(message)s",
                stream=sys.stderr,
            )
        logger.info("Starting %s v%s stdio listener...", self.name, self.version)
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
                logger.error("JSON parse error: %s", e)
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": "Parse error"},
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()
            except Exception as e:
                logger.error("Unexpected stdio exception: %s", e)

    def create_sse_transport(self, api_key: Optional[str] = None, bearer_token: Optional[str] = None):
        """Creates an authenticated SSE transport handler for remote HTTP deployments."""
        from .transports.sse import SSETransportHandler
        return SSETransportHandler(self, api_key=api_key, bearer_token=bearer_token)
