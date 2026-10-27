"""
Token Bucket Rate Limiter Middleware (FastMCP Forge Pro).
Protects remote SSE/HTTP MCP endpoints from runaway AI agent tool invocation loops.
"""
import time
from typing import Dict, Any

class RateLimiter:
    def __init__(self, rate_per_sec: float = 10.0, burst: int = 20):
        self.rate_per_sec = rate_per_sec
        self.burst = burst
        self.buckets: Dict[str, Dict[str, float]] = {}

    def _get_bucket(self, key: str) -> Dict[str, float]:
        if key not in self.buckets:
            self.buckets[key] = {
                "tokens": float(self.burst),
                "last_update": time.time()
            }
        return self.buckets[key]

    def allow_request(self, client_key: str) -> bool:
        now = time.time()
        bucket = self._get_bucket(client_key)
        elapsed = now - bucket["last_update"]
        bucket["last_update"] = now

        # Replenish tokens based on elapsed time
        bucket["tokens"] = min(float(self.burst), bucket["tokens"] + elapsed * self.rate_per_sec)

        if bucket["tokens"] >= 1.0:
            bucket["tokens"] -= 1.0
            return True
        return False
