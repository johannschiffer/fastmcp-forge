from fastmcp_forge.server import FastMCP

app = FastMCP("demo-weather-mcp")

@app.tool()
def get_weather(city: str) -> str:
    """Get real-time weather information for a specified city."""
    return f"The weather in {city} is clear and 21°C."

if __name__ == "__main__":
    app.run()
