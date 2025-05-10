from typing import Optional
from ..tutorial_base import TutorialBase
from ..utils import Prompt
from pathlib import Path


class FastMcpWeather(TutorialBase):
    def __init__(self):
        super().__init__(
            name="FastMcpWeather",
            description="Learn how to implement weather functionality using FastMCP and National Weather Service API",
        )
        self.target_file = "mcp-weather/src/mcp_weather/__init__.py"
        self.current_step = 1
        self.total_steps = 2

    def check(self) -> bool:
        """Check if a specific step is completed"""
        if not self.verify_file_exists(self.target_file):
            self.prompter.warn(
                "Did you complete the previous MakeServer tutorial first?"
            )
            return False

        content = Path(self.target_file).read_text()
        if self.current_step == 1:
            return (
                "from mcp.server.fastmcp import FastMCP" in content
                and "NWS_API_BASE" in content
            )
        elif self.current_step == 2:
            return (
                "get_alerts" in content
                and "get_forecast" in content
                and not "@server.list_tools" in content
                and not "@server.call_tool" in content
            )
        return False

    def run_step(self, step_id: int) -> bool:
        if step_id == 1:
            self.step1()
        elif step_id == 2:
            self.step2()
        if not self.handle_editor_options(self.target_file):
            return False
        return True

    def step1(self):
        self.prompter.clear()
        self.prompter.box_with_key("fastmcp_weather.step1.title")
        self.prompter.instruct_with_key("fastmcp_weather.step1.intro1")
        self.prompter.instruct_with_key("fastmcp_weather.step1.intro2")
        self.prompter.instruct_with_key("fastmcp_weather.step1.intro3")
        self.prompter.instruct_with_key("fastmcp_weather.step1.benefits.title")
        self.prompter.instruct_with_key("fastmcp_weather.step1.benefits.1")
        self.prompter.instruct_with_key("fastmcp_weather.step1.benefits.2")
        self.prompter.instruct_with_key("fastmcp_weather.step1.benefits.3")
        self.prompter.instruct_with_key("fastmcp_weather.step1.benefits.4")
        self.prompter.instruct_with_key("fastmcp_weather.step1.intro4")

        self.prompter.instruct_with_key("fastmcp_weather.step1.dependencies")
        self.prompter.snippet(
            """[project]
dependencies = [
    "mcp[cli]",
    "httpx",
    "starlette>=0.27.0",
    "uvicorn>=0.24.0"
]"""
        )

        self.prompter.instruct_with_key("fastmcp_weather.step1.setup")
        self.prompter.snippet(
            """from mcp.server.fastmcp import FastMCP, Context
from starlette.applications import Starlette
from starlette.routing import Mount
import uvicorn
import httpx
from typing import Any

# Constants for the National Weather Service API
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

# Create FastMCP instance with SSE support
mcp = FastMCP(
    "Weather Service",
    dependencies=["httpx", "starlette", "uvicorn"],
    lifespan=server_lifespan,
)"""
        )

        self.prompter.intense_instruct_with_key("fastmcp_weather.step1.lifespan")
        self.prompter.snippet(
            """
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[str]:
    try:
        ## This is just example. actual code,
        ## Using yield with time consuming resource, like db connection
        yield server.name
    finally:
        pass"""
        )

        self.prompter.instruct_with_key("fastmcp_weather.step1.existing")
        self.prompter.snippet(
            '''
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
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
"""'''
        )

    def step2(self):
        self.prompter.clear()
        self.prompter.box_with_key("fastmcp_weather.step2.title")
        self.prompter.instruct_with_key("fastmcp_weather.step2.intro1")
        self.prompter.instruct_with_key("fastmcp_weather.step2.intro2")

        self.prompter.instruct_with_key("fastmcp_weather.step2.tools")
        self.prompter.instruct_with_key("fastmcp_weather.step2.modify")
        self.prompter.instruct_with_key("fastmcp_weather.step2.automatic")
        self.prompter.snippet(
            '''@mcp.tool()
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
    return "\\n--\\n".join(alerts)

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
    return "\\n--\\n".join(forecasts)'''
        )

        self.prompter.instruct_with_key("fastmcp_weather.step2.main")
        self.prompter.snippet(
            '''
async def run_sse(port: int = 9009) -> None:
    starlette_app = Starlette(routes=[Mount("/", app=mcp.sse_app())])
    config = uvicorn.Config(starlette_app, host="0.0.0.0", port=port)  # noqa: S104
    app = uvicorn.Server(config)
    # Use server.serve() instead of run() to stay in the same event loop
    await app.serve()

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
    main()'''
        )

    def run(self) -> bool:
        """Run the tutorial"""
        while self.current_step <= self.total_steps:
            if not self.check():
                if not self.run_step(self.current_step):
                    return False
            else:
                self.prompter.intense_instruct(
                    f"You've completed step {self.current_step}!"
                )
                self.current_step += 1
            self.prompter.instruct("➤ Press any key to continue")
            self.prompter.get_key()

        return True
