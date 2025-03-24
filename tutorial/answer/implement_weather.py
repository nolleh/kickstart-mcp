# SPDX-FileCopyrightText: 2025-present nolleh <nolleh7707@gmail.com>
#
# SPDX-License-Identifier: MIT

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server import Server
import mcp.server.stdio
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel.server import NotificationOptions
from mcp.types import Tool, TextContent
from typing import Any, Sequence
import httpx

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=5.0)
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
Area: {props.get('areaDesc', 'Unknwon')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instruction provided')}
    """


@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[str]:
    try:
        ## this is just example. actually code,
        ## use yield with consuming resource, like db connection
        yield server.name
    finally:
        pass


server = Server("weather", lifespan=server_lifespan)


@server.call_tool()
async def get_weather(name: str, state: str) -> Sequence[TextContent]:
    return [TextContent(type="text", text=f"Hello {state}")]


@server.call_tool()
async def get_alerts(name: str, arguments: dict) -> Sequence[TextContent]:
    """Get weather alerts for a US state

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """

    url = f"{NWS_API_BASE}/alerts/active/area/{arguments["state"]}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return [
            TextContent(type="text", text=f"url: {url}, Unable to fetch alerts or no alerts found.")
        ]
    if not data["features"]:
        return [TextContent(type="text", text="No active alerts for this state.")]

    alerts = [format_alert(feature) for feature in data["features"]]
    return [TextContent(type="text", text="\n--\n".join(alerts))]


# @server.call_tool()
async def get_forecast(name: str, latitude: float, longitude: float) -> Sequence[TextContent]:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        logitude: Longitude of the location
    """

    # First get the Forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    points_data = await make_nws_request(points_url)

    if not points_data:
        return [
            TextContent(
                type="text", text="Unable to fetch forecast data for this location."
            )
        ]

    # Get the forecast URL from the points response
    forecast_url = points_data["properties"]["forecast"]
    forecast_data = await make_nws_request(forecast_url)

    if not forecast_data:
        return [TextContent(type="text", text="Unable to fetch detailed forecast.")]

    # Format the periods into a readable forecast
    periods = forecast_data["properties"]["periods"]
    forecasts = []

    for period in periods[:5]:  # Only show next 5 period
        forecast = f"""
                {period['name']}:
                Temperature: {period['temperature']}°{period['temperatureUnit']}
                Wind: {period['windSepeed']} {period['windDirection']}
                Forecast: {period['detailedForecast']}
        """
        forecasts.append(forecast)
    return [TextContent(type="text", text="\n--\n".join(forecasts))]


@server.list_tools()
async def list_tools() -> list[Tool]:
    tools = []
    ctx = server.request_context.lifespan_context

    if ctx and "weather":
        tools.extend(
            [
                Tool(
                    name="get_weather",
                    description="Get the weather",
                    inputSchema={
                        "type": "object",
                        "properties": {"state": {"type": "string"}},
                    },
                ),
                Tool(
                    name="get_alerts",
                    description="Get weather alerts for a US state",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "state": {
                                "type": "string",
                                "description": "Two-letter US state code (e.g. CA, NY)",
                            }
                        },
                        "required": ["state"],
                    },
                ),
            ]
        )
    return tools


async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="weather",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


def main():
    print("server is running...")
    import asyncio

    asyncio.run(run())


#
#
if __name__ == "__main__":
    main()
