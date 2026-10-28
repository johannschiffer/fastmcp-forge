"""
Remote SSE (Server-Sent Events) Transport.
Implements the Model Context Protocol HTTP/SSE remote transport standard
with integrated authentication, bounded session tracking, and rate limiting.
"""
import json
import time
import uuid
from typing import Any, Dict, Optional

from ..middleware.auth import AuthMiddleware
from ..middleware.rate_limiter import RateLimiter


class SSETransportHandler:
    def __init__(
        self,
        mcp_server,
        api_key: Optional[str] = None,
        bearer_token: Optional[str] = None,
        max_sessions: int = 10000,
        session_ttl_sec: float = 3600.0,
    ):
        self.server = mcp_server
        self.auth = AuthMiddleware(api_key=api_key, bearer_token=bearer_token)
        self.limiter = RateLimiter(rate_per_sec=10.0, burst=20)
        self.max_sessions = max(1, int(max_sessions))
        self.session_ttl_sec = float(session_ttl_sec)
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def _prune_sessions(self, now: float) -> None:
        expired = [
            sid
            for sid, meta in self.sessions.items()
            if (now - meta.get("last_seen", meta.get("created_at", now))) > self.session_ttl_sec
        ]
        for sid in expired:
            self.sessions.pop(sid, None)
        while len(self.sessions) >= self.max_sessions:
            oldest_sid = next(iter(self.sessions))
            self.sessions.pop(oldest_sid, None)

    def handle_sse_connect(self, headers: Dict[str, str], client_ip: str = "127.0.0.1") -> Dict[str, Any]:
        """Handles GET /sse connection initiation."""
        is_auth, reason = self.auth.verify_headers(headers)
        if not is_auth:
            return {
                "status_code": 401,
                "body": json.dumps({"error": reason}),
                "content_type": "application/json",
            }

        if not self.limiter.allow_request(client_ip):
            return {
                "status_code": 429,
                "body": json.dumps({"error": "Rate limit exceeded"}),
                "content_type": "application/json",
            }

        now = time.time()
        self._prune_sessions(now)
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {"created_at": now, "last_seen": now, "ip": client_ip}

        endpoint_url = f"/messages?session_id={session_id}"
        sse_event = f"event: endpoint\ndata: {endpoint_url}\n\n"

        return {
            "status_code": 200,
            "session_id": session_id,
            "sse_event": sse_event,
            "content_type": "text/event-stream",
        }

    def handle_post_message(
        self,
        session_id: str,
        request_json: Dict[str, Any],
        headers: Dict[str, str],
        client_ip: str = "127.0.0.1",
    ) -> Dict[str, Any]:
        """Handles POST /messages?session_id=... JSON-RPC payload."""
        is_auth, reason = self.auth.verify_headers(headers)
        if not is_auth:
            return {
                "status_code": 401,
                "body": json.dumps({"error": reason}),
                "content_type": "application/json",
            }

        if not self.limiter.allow_request(client_ip):
            return {
                "status_code": 429,
                "body": json.dumps({"error": "Rate limit exceeded"}),
                "content_type": "application/json",
            }

        now = time.time()
        session = self.sessions.get(session_id)
        if session is None or (now - session.get("last_seen", session.get("created_at", now))) > self.session_ttl_sec:
            self.sessions.pop(session_id, None)
            return {
                "status_code": 404,
                "body": json.dumps({"error": "Unknown or expired session_id"}),
                "content_type": "application/json",
            }
        session["last_seen"] = now

        response = self.server.handle_request(request_json)
        return {
            "status_code": 200,
            "body": json.dumps(response, ensure_ascii=False) if response else "",
            "content_type": "application/json",
        }
