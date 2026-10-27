"""
Authentication & Authorization Middleware.
Validates API keys and Bearer tokens for incoming MCP HTTP / SSE connections.
"""
from typing import Dict, Any, Optional

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

        # Normalize headers to lowercase keys
        lower_headers = {k.lower(): v for k, v in headers.items()}

        # 1. Check API Key
        if self.api_key:
            req_key = lower_headers.get("x-api-key")
            if req_key and req_key == self.api_key:
                return True, "API Key authenticated"

        # 2. Check Bearer Token
        if self.bearer_token:
            auth_header = lower_headers.get("authorization", "")
            if auth_header.startswith("Bearer "):
                token = auth_header[7:].strip()
                if token == self.bearer_token:
                    return True, "Bearer token authenticated"

        return False, "Unauthorized: Invalid or missing credentials in X-API-Key or Authorization header"
