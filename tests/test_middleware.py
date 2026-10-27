"""
Unit tests for FastMCP Forge Middleware (Auth & Rate Limiting).
"""
import time
import pytest
from fastmcp_forge.middleware.auth import AuthMiddleware
from fastmcp_forge.middleware.rate_limiter import RateLimiter

def test_auth_middleware_disabled():
    auth = AuthMiddleware()
    assert not auth.is_enabled()
    is_auth, _ = auth.verify_headers({})
    assert is_auth is True

def test_auth_middleware_api_key():
    auth = AuthMiddleware(api_key="secret-mcp-key-123")
    assert auth.is_enabled()

    # Valid API Key in Header (case insensitive)
    valid_res, _ = auth.verify_headers({"X-Api-Key": "secret-mcp-key-123"})
    assert valid_res is True

    # Invalid API Key
    invalid_res, reason = auth.verify_headers({"X-Api-Key": "wrong-key"})
    assert invalid_res is False
    assert "Unauthorized" in reason

    # Missing API Key
    missing_res, _ = auth.verify_headers({})
    assert missing_res is False

def test_auth_middleware_bearer_token():
    auth = AuthMiddleware(bearer_token="jwt-token-xyz")
    assert auth.is_enabled()

    # Valid Bearer token
    valid_res, _ = auth.verify_headers({"authorization": "Bearer jwt-token-xyz"})
    assert valid_res is True

    # Invalid Bearer token
    invalid_res, _ = auth.verify_headers({"authorization": "Bearer bad-token"})
    assert invalid_res is False

def test_rate_limiter_token_bucket():
    # Rate of 2 tokens per sec, burst capacity 2
    limiter = RateLimiter(rate_per_sec=2.0, burst=2)
    client = "client-1"

    # Consume 2 burst tokens
    assert limiter.allow_request(client) is True
    assert limiter.allow_request(client) is True

    # 3rd request immediately should be rate-limited
    assert limiter.allow_request(client) is False

    # Wait 0.6s -> should replenish ~1 token (0.6 * 2 = 1.2)
    time.sleep(0.6)
    assert limiter.allow_request(client) is True

    # Different client has its own independent bucket
    other_client = "client-2"
    assert limiter.allow_request(other_client) is True
