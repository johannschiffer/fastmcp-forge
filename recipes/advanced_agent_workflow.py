"""
End-to-end FastMCP Forge workflow recipe.
Demonstrates decorator registration, JSON Schema inference, direct tool execution,
and authenticated SSE session handling.
"""
import json
import sys
from fastmcp_forge.server import FastMCP

app = FastMCP("demo-weather-mcp", version="2.0.1")


@app.tool()
def get_weather(city: str, units: str = "celsius") -> str:
    """Return sample weather details for a city."""
    temp = "21C" if units == "celsius" else "70F"
    return f"Weather in {city}: clear, {temp}."


def run_demo() -> None:
    sse = app.create_sse_transport(api_key="demo-key")
    conn = sse.handle_sse_connect({"X-API-Key": "demo-key"})
    session_id = conn["session_id"]
    resp = sse.handle_post_message(
        session_id=session_id,
        request_json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": "get_weather", "arguments": {"city": "Madrid"}},
        },
        headers={"X-API-Key": "demo-key"},
    )
    print(json.dumps(json.loads(resp["body"]), indent=2))


if __name__ == "__main__":
    if "--stdio" in sys.argv:
        app.run()
    else:
        run_demo()
