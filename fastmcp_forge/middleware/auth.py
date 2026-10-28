"""
Authentication & Authorization Middleware.
Validates API keys and Bearer tokens for incoming MCP HTTP / SSE connections
using constant-time digest comparison.
"""
import hmac
from typing import Dict, Optional


class AuthMiddleware:
    def __init__(self, api_key: Optional[str] = None, bearer_token: Optional[str] = None):
        self.api_key = api_key
        self.bearer_token = bearer_token

    def is_enabled(self) -> bool:
        return bool(self.api_key or self.bearer_token)

    def verify_headers(self, headers: Dict[str, str]) -> tuple[bool, str]:
        """
        Validates headers for X-API-Key or Authorization Bearer token.
        Returns (is_authorized: bool, reason: str).
        """
        if not self.is_enabled():
            return True, "Authentication disabled (public mode)"

        lower_headers = {str(k).lower(): str(v) for k, v in (headers or {}).items()}

        if self.api_key:
            req_key = lower_headers.get("x-api-key")
            if req_key and hmac.compare_digest(req_key.encode("utf-8"), self.api_key.encode("utf-8")):
                return True, "API Key authenticated"

        if self.bearer_token:
            auth_header = lower_headers.get("authorization", "")
            parts = auth_header.split(None, 1)
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1].strip()
                if hmac.compare_digest(token.encode("utf-8"), self.bearer_token.encode("utf-8")):
                    return True, "Bearer token authenticated"

        return False, "Unauthorized: Invalid or missing credentials in X-API-Key or Authorization header"
