"""
Token Bucket Rate Limiter Middleware.
Protects remote SSE/HTTP MCP endpoints from runaway AI agent tool invocation loops.
"""
import time
from typing import Dict


class RateLimiter:
    def __init__(self, rate_per_sec: float = 10.0, burst: int = 20, max_buckets: int = 10000):
        if rate_per_sec <= 0:
            raise ValueError("rate_per_sec must be positive")
        if burst < 1:
            raise ValueError("burst must be at least 1")
        self.rate_per_sec = float(rate_per_sec)
        self.burst = int(burst)
        self.max_buckets = max(1, int(max_buckets))
        self.buckets: Dict[str, Dict[str, float]] = {}

    def _get_bucket(self, key: str, now: float) -> Dict[str, float]:
        if key not in self.buckets:
            if len(self.buckets) >= self.max_buckets:
                oldest_key = next(iter(self.buckets))
                self.buckets.pop(oldest_key, None)
            self.buckets[key] = {
                "tokens": float(self.burst),
                "last_update": now,
            }
        return self.buckets[key]

    def allow_request(self, client_key: str) -> bool:
        now = time.monotonic()
        bucket = self._get_bucket(client_key, now)
        elapsed = max(0.0, now - bucket["last_update"])
        bucket["last_update"] = now

        bucket["tokens"] = min(float(self.burst), bucket["tokens"] + elapsed * self.rate_per_sec)

        if bucket["tokens"] >= 1.0:
            bucket["tokens"] -= 1.0
            return True
        return False
