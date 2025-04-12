from typing import Optional
from ..tutorial_base import TutorialBase
from ..utils import Prompt
from pathlib import Path


class ImplementWeather(TutorialBase):
    def __init__(self):
        super().__init__(
            name="ImplementWeather",
            description="Learn how to implement real weather functionality using National Weather Service API",
        )
        self.target_file = "mcp-weather/src/mcp_weather/__init__.py"
        self.current_step = 1
        self.total_steps = 3

    def check(self) -> bool:
        """Check if a specific step is completed"""
        if not self.verify_file_exists(self.target_file):
            self.prompter.warn_with_key("implement_weather.warning")
            return False

        content = Path(self.target_file).read_text()
        # self.prompter.intense_instruct("read file..")
        # self.prompter.snippet(content)

        if self.current_step == 1:
            return "NWS_API_BASE" in content and "make_nws_request" in content
        elif self.current_step == 2:
            return "get_alerts" in content and "@server.list_tools()" in content
        elif self.current_step == 3:
            return "get_forecast" in content and "latitude: float" in content
        return False

    def run_step(self, step_id: int) -> bool:
        if step_id == 1:
            self.step1()
        elif step_id == 2:
            self.step2()
        elif step_id == 3:
            self.step3()
        if not self.handle_editor_options(self.target_file):
            return False
        return True

    def step1(self):
        self.prompter.clear()
        self.prompter.box_with_key("implement_weather.step1.title")
        self.prompter.intense_instruct_with_key("implement_weather.step1.intro1")
        self.prompter.intense_instruct_with_key("implement_weather.step1.intro2")
        self.prompter.instruct_with_key("implement_weather.step1.intro3")
        self.prompter.instruct_with_key("implement_weather.step1.intro4")

        self.prompter.instruct_with_key("implement_weather.step1.todo.title")
        self.prompter.instruct_with_key("implement_weather.step1.todo.1")
        self.prompter.instruct_with_key("implement_weather.step1.todo.2")
        self.prompter.instruct_with_key("implement_weather.step1.todo.3")
        self.prompter.instruct_with_key("implement_weather.step1.todo.4")

        self.prompter.instruct_with_key("implement_weather.step1.add_code")
        self.prompter.snippet(
            '''from typing import Any, Sequence
import httpx
from mcp.types import Tool, TextContent

# Constants for the National Weather Service API
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

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
        self.prompter.instruct_with_key("implement_weather.step1.dependency")

    def step2(self):
        self.prompter.clear()
        self.prompter.box_with_key("implement_weather.step2.title")
        self.prompter.instruct_with_key("implement_weather.step2.intro1")
        self.prompter.instruct_with_key("implement_weather.step2.intro2")
        self.prompter.intense_instruct_with_key("implement_weather.step2.intro3")
        self.prompter.intense_instruct_with_key("implement_weather.step2.intro4")

        self.prompter.instruct_with_key("implement_weather.step2.replace_list")
        self.prompter.snippet(
            """@server.list_tools()
async def list_tools() -> list[Tool]:
    tools = []
    ctx = server.request_context.lifespan_context

    if ctx and "weather":
        tools.extend([
            Tool(
                name="get_alerts",
                description="Get weather alerts for a US state",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "state": {
                            "type": "string",
                            "description": "Two-letter US state code (e.g. CA, NY)"
                        }
                    },
                    "required": ["state"]
                }
            ),
        ])
    return tools"""
        )

        self.prompter.instruct_with_key("implement_weather.step2.replace_call")
        self.prompter.snippet(
            '''
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
    # return [TextContent(type="text", text="test~")]
    if name == "get_alerts":
        result = await get_alerts(arguments["state"])
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
    return "\\n--\\n".join(alerts)'''
        )

    def step3(self):
        self.prompter.clear()
        self.prompter.box_by_key("implement_weather.step3.title")
        self.prompter.instruct_with_key("implement_weather.step3.intro1")
        self.prompter.instruct_with_key("implement_weather.step3.intro2")

        self.prompter.instruct_with_key("implement_weather.step3.add_list")
        self.prompter.snippet(
            """
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
            """
        )

        self.prompter.instruct_with_key("implement_weather.step3.add_impl")
        self.prompter.snippet(
            '''
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> Sequence[TextContent]:
    ## ....previous steps code
    elif name == "get_forecast":
        result = await get_forecast(arguments["latitude"], arguments["longitude"])
        return [TextContent(type="text", text=result)]
    raise ValueError(f"Unknown tool: {name}")

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
    return "\\n--\\n".join(forecasts)'''
        )

    def run(self) -> bool:
        """Run the tutorial"""
        while self.current_step <= self.total_steps:
            if not self.check():
                if not self.run_step(self.current_step):
                    return False
            else:
                self.prompter.intense_instruct_with_key(
                    "implement_weather.step_complete", self.current_step
                )
                self.current_step += 1
            self.prompter.instruct_with_key("implement_weather.press_continue")
            self.prompter.get_key()

        return True
