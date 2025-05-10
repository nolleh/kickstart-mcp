from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP, Context
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn
import httpx
from typing import Any

# Constants for the National Weather Service API
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[str]:
    try:
        ## This is just example. actual code,
        ## Using yield with time consuming resource, like db connection
        yield server.name
    finally:
        pass


# Create FastMCP instance with SSE support
mcp = FastMCP(
    "Weather Service",
    dependencies=["httpx", "starlette", "uvicorn"],
    lifespan=server_lifespan,
)

async def run_server(transport: str = "stdio", port: int = 9009) -> None:
    """Run the MCP server with the specified transport."""
    if transport == "sse":
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.requests import Request
        from starlette.routing import Mount, Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request: Request) -> None:
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await server.run(
                    streams[0], streams[1], server.create_initialization_options()
                )

        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
            ],
        )

        import uvicorn

        # Set up uvicorn config
        config = uvicorn.Config(starlette_app, host="0.0.0.0", port=port)  # noqa: S104
        app = uvicorn.Server(config)
        # Use server.serve() instead of run() to stay in the same event loop
        await app.serve()
    else:
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, server.create_initialization_options()
            )

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error making request: {e}")
            return None


def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

async def run_sse(port: int = 9009) -> None:
    starlette_app = Starlette(routes=[Mount("/", app=mcp.sse_app())])
    config = uvicorn.Config(starlette_app, host="0.0.0.0", port=port)  # noqa: S104
    app = uvicorn.Server(config)
    # Use server.serve() instead of run() to stay in the same event loop
    await app.serve()

@mcp.tool()
async def get_alerts(state: str, ctx: Context) -> str:
    """Get weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY)
        ctx: FastMCP context for progress reporting and logging
    """
    ctx.info(f"Fetching alerts for state: {state}")
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return f"Unable to fetch alerts or no alerts found for {state}."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n--\n".join(alerts)

@mcp.tool()
async def get_forecast(latitude: float, longitude: float, ctx: Context) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
        ctx: FastMCP context for progress reporting and logging
    """
    ctx.info(f"Fetching forecast for location: {latitude}, {longitude}")

    # First get the Forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return "Unable to fetch forecast data for this location."

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return "Unable to fetch detailed forecast."

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []

    for period in periods[:5]:  # Only show next 5 periods
        forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
        """
        forecasts.append(forecast)
    return "\n--\n".join(forecasts)
def main():
    """Run the FastMCP server"""
    import asyncio
    import argparse

    parser = argparse.ArgumentParser(description="Run the FastMCP Weather Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport type to use",
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port to use for SSE transport"
    )
    args = parser.parse_args()
    if args.transport == "sse":
        asyncio.run(run_sse(port=args.port))
    else:
        mcp.run()

if __name__ == "__main__":
    main()
