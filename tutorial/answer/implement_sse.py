from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server import Server
from mcp.types import Tool, TextContent
from typing import Any, Sequence
import httpx

@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[str]:
    try:
        ## This is just example. actual code,
        ## Using yield with time consuming resource, like db connection
        yield server.name
    finally:
        pass


server = Server("weather", lifespan=server_lifespan)


@server.list_tools()
async def list_tools() -> list[Tool]:
    tools = []
    ctx = server.request_context.lifespan_context

    if ctx and "weather":
        tools.extend(
            [
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
                Tool(
                    name="get_forecast",
                    description="Get weather forecast for a location",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "latitude": {
                                "type": "number",
                                "description": "Latitude of the location. ex. 38.8898",
                            },
                            "longitude": {
                                "type": "number",
                                "description": "Longitude of the location. ex. -77.009056",
                            },
                        },
                        "required": ["latitude", "longitude"],
                    },
                ),
            ]
        )
    return tools


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
    # return [TextContent(type="text", text="test~")]
    if name == "get_alerts":
        result = await get_alerts(arguments["state"])
        return [TextContent(type="text", text=result)]
    elif name == "get_forecast":
        result = await get_forecast(arguments["latitude"], arguments["longitude"])
        return [TextContent(type="text", text=result)]
    raise ValueError(f"Unknown tool: {name}")


async def get_alerts(state: str) -> str:
    """Get weather alerts for a US state

    Args:
        state: Two-letter US state code (e.g. CA, NY)
    """

    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return f"url: {url}, Unable to fetch alerts or no alerts found."

    if not data["features"]:
        return "No active alerts for this state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n--\n".join(alerts)


async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """

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

    for period in periods[:5]:  # Only show next 5 period
        forecast = f"""                                                            
{period['name']}:                                                                  
Temperature: {period['temperature']}°{period['temperatureUnit']}                   
Wind: {period['windSpeed']} {period['windDirection']}                              
Forecast: {period['detailedForecast']}                                             
        """
        forecasts.append(forecast)
    return "\n--\n".join(forecasts)


# async def run():
#     async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
#         print("server is running...")
#         await server.run(
#             read_stream,
#             write_stream,
#             InitializationOptions(
#                 server_name="weather",
#                 server_version="0.1.0",
#                 capabilities=server.get_capabilities(
#                     notification_options=NotificationOptions(),
#                     experimental_capabilities={},
#                 ),
#             ),
#         )
#     # Constants for the National Weather Service API                              |


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


NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"


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


def main(
):
    import asyncio
    import argparse
    parser = argparse.ArgumentParser(description="Run the MCP Weather Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio", help="Transport type to use")
    parser.add_argument("--port", type=int, default=8000, help="Port to use for SSE transport")
    args = parser.parse_args()

    asyncio.run(run_server(transport=args.transport, port=args.port))

if __name__ == "__main__":
    main()

