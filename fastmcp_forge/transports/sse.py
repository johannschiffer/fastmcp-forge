"""
Remote SSE (Server-Sent Events) Transport (FastMCP Forge Pro).
Implements the Model Context Protocol HTTP/SSE remote transport standard
with integrated authentication and rate limiting.
"""
import uuid
import json
from typing import Dict, Any, Optional
from ..middleware.auth import AuthMiddleware
from ..middleware.rate_limiter import RateLimiter

class SSETransportHandler:
    def __init__(self, mcp_server, api_key: Optional[str] = None, bearer_token: Optional[str] = None):
        self.server = mcp_server
        self.auth = AuthMiddleware(api_key=api_key, bearer_token=bearer_token)
        self.limiter = RateLimiter(rate_per_sec=10.0, burst=20)
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def handle_sse_connect(self, headers: Dict[str, str], client_ip: str = "127.0.0.1") -> Dict[str, Any]:
        """Handles GET /sse connection initiation."""
        # 1. Auth check
        is_auth, reason = self.auth.verify_headers(headers)
        if not is_auth:
            return {"status_code": 401, "body": json.dumps({"error": reason}), "content_type": "application/json"}

        # 2. Rate limit
        if not self.limiter.allow_request(client_ip):
            return {"status_code": 429, "body": json.dumps({"error": "Rate limit exceeded"}), "content_type": "application/json"}

        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {"created_at": None, "ip": client_ip}

        endpoint_url = f"/messages?session_id={session_id}"
        sse_event = f"event: endpoint\ndata: {endpoint_url}\n\n"

        return {
            "status_code": 200,
            "session_id": session_id,
            "sse_event": sse_event,
            "content_type": "text/event-stream"
        }

    def handle_post_message(self, session_id: str, request_json: Dict[str, Any], 
                            headers: Dict[str, str], client_ip: str = "127.0.0.1") -> Dict[str, Any]:
        """Handles POST /messages?session_id=... JSON-RPC payload."""
        # 1. Auth check
        is_auth, reason = self.auth.verify_headers(headers)
        if not is_auth:
            return {"status_code": 401, "body": json.dumps({"error": reason})}

        # 2. Rate limit
        if not self.limiter.allow_request(client_ip):
            return {"status_code": 429, "body": json.dumps({"error": "Rate limit exceeded"})}

        # 3. Process MCP Request
        response = self.server.handle_request(request_json)
        return {
            "status_code": 200,
            "body": json.dumps(response, ensure_ascii=False) if response else "",
            "content_type": "application/json"
        }
