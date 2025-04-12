from typing import Optional
from ..tutorial_base import TutorialBase
from ..utils import Prompt
from pathlib import Path

class MakeServer(TutorialBase):
    def __init__(self):
        super().__init__(
            name="MakeServer",
            description="Learn how to create a weather server with step-by-step instructions"
        )
        self.target_file = "mcp-weather/src/mcp_weather/__init__.py"
        self.current_step = 1
        self.total_steps = 4  # Updated to include the new call_tool step

    def check(self) -> bool:
        """Check if a specific step is completed"""
        if not self.verify_file_exists(self.target_file):
            self.prompter.warn_with_key("make_server.warning")
            return False

        content = Path(self.target_file).read_text()
        # self.prompter.intense_instruct("read file..")
        # self.prompter.snippet(content)

        if self.current_step == 1:
            # Check if server instance is created
            # content = self.read_target_file()
            return "server = Server" in content and "@asynccontextmanager" in content
        elif self.current_step == 2:
            # Check if run function and main are added
            # content = self.read_target_file()
            return "async def run()" in content and "def main()" in content
        elif self.current_step == 3:
            # Check if tools are added
            # content = self.read_target_file()
            return "@server.list_tools()" in content and "async def list_tools() -> list[Tool]" in content
        elif self.current_step == 4:
            return "@server.call_tool()" in content and "async def get_weather" in content
        return self.current_step > self.total_steps

    def run_step(self, step_id: int) -> bool:
        """Run a specific step of the tutorial"""
        if step_id == 1:
            self.step1()
        elif step_id == 2:
            self.step2()
        elif step_id == 3:
            self.step3()
        elif step_id == 4:
            self.step4()
        if not self.handle_editor_options(self.target_file):
            return False
        return True

    def step1(self):
        self.prompter.clear()
        self.prompter.box_with_key("make_server.step1.title")
        self.prompter.instruct_with_key("make_server.step1.intro1")
        self.prompter.instruct_with_key("make_server.step1.intro2")
        self.prompter.instruct_with_key("make_server.step1.decorator.title")
        self.prompter.instruct_with_key("make_server.step1.decorator.1")
        self.prompter.instruct_with_key("make_server.step1.decorator.2")
        self.prompter.instruct_with_key("make_server.step1.decorator.3")

        self.prompter.instruct_with_key("make_server.step1.lifespan.title")
        self.prompter.instruct_with_key("make_server.step1.lifespan.1")
        self.prompter.instruct_with_key("make_server.step1.lifespan.2")
        self.prompter.intense_instruct_with_key("make_server.step1.lifespan.3")
        self.prompter.instruct_with_key("make_server.step1.lifespan.4")

        self.prompter.instruct_with_key("make_server.step1.instance.title")
        self.prompter.instruct_with_key("make_server.step1.instance.1")
        self.prompter.instruct_with_key("make_server.step1.instance.2")

        self.prompter.instruct_with_key("make_server.step1.add_code")
        self.prompter.snippet(
            '''from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server import Server

@asynccontextmanager
async def server_lifespan(server: Server) -> AsyncIterator[str]:
try:
    ## This is just example. actual code,
    ## Using yield with time consuming resource, like db connection
    yield server.name
finally:
    pass

server = Server("weather", lifespan=server_lifespan)'''
        )
        self.prompter.instruct_with_key("make_server.step1.dependency")

    def step2(self):
        self.prompter.clear()
        self.prompter.box_with_key("make_server.step2.title")
        self.prompter.instruct_with_key("make_server.step2.intro1")
        self.prompter.instruct_with_key("make_server.step2.intro2")
        self.prompter.instruct_with_key("make_server.step2.stdio.title")
        self.prompter.instruct_with_key("make_server.step2.stdio.1")
        self.prompter.instruct_with_key("make_server.step2.stdio.2")
        self.prompter.instruct_with_key("make_server.step2.stdio.3")

        self.prompter.instruct_with_key("make_server.step2.sse.title")
        self.prompter.instruct_with_key("make_server.step2.sse.1")
        self.prompter.instruct_with_key("make_server.step2.sse.2")
        self.prompter.intense_instruct_with_key("make_server.step2.sse.3")

        self.prompter.instruct_with_key("make_server.step2.implement")
        self.prompter.instruct_with_key("make_server.step2.setup")

        self.prompter.instruct_with_key("make_server.step2.add_code")
        self.prompter.snippet(
            '''import mcp.server.stdio
from mcp.server.models import InitializationOptions
from mcp.server.lowlevel.server import NotificationOptions

async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        print("server is running...")
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
import asyncio
asyncio.run(run())'''
        )
        self.prompter.instruct_with_key("make_server.step2.dependency")

    def step3(self):
        self.prompter.clear()
        self.prompter.box_with_key("make_server.step3.title")
        self.prompter.instruct_with_key("make_server.step3.intro1")
        self.prompter.instruct_with_key("make_server.step3.intro2")

        self.prompter.instruct_with_key("make_server.step3.keypoints.title")
        self.prompter.instruct_with_key("make_server.step3.model.title")
        self.prompter.instruct_with_key("make_server.step3.model.1")
        self.prompter.instruct_with_key("make_server.step3.model.2")

        self.prompter.instruct_with_key("make_server.step3.safety.title")
        self.prompter.instruct_with_key("make_server.step3.safety.1")
        self.prompter.instruct_with_key("make_server.step3.safety.2")

        self.prompter.instruct_with_key("make_server.step3.schema.title")
        self.prompter.instruct_with_key("make_server.step3.schema.1")
        self.prompter.instruct_with_key("make_server.step3.schema.2")
        self.prompter.instruct_with_key("make_server.step3.schema.3")
        self.prompter.instruct_with_key("make_server.step3.schema.4")
        self.prompter.instruct_with_key("make_server.step3.schema.5")

        self.prompter.instruct_with_key("make_server.step3.structure")
        self.prompter.snippet(
            '''{
    "name": "tool_name",
    "description": "tool_description",
    "inputSchema": {
    "type": "object",
    "properties": {
      "paramter name": {
        "type": "string",
        "description": "parmeter description"
      }
    },
    "required": ["required_parameter_list"]
    }
}''')

        self.prompter.instruct_with_key("make_server.step3.add_code")
        self.prompter.snippet(
            '''from mcp.types import Tool

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
                )
            ]
        )
    return tools''')

    def step4(self):
        self.prompter.clear()
        self.prompter.box_with_key("make_server.step4.title")
        self.prompter.instruct_with_key("make_server.step4.intro1")
        self.prompter.instruct_with_key("make_server.step4.intro2")

        self.prompter.instruct_with_key("make_server.step4.request_format")
        self.prompter.snippet(
            '''{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "example_tool",
    "arguments": {
      "param": "value"
    }
  }
}'''
        )

        self.prompter.instruct_with_key("make_server.step4.response_format")
        self.prompter.snippet(
            '''{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [{
      "type": "text",
      "text": "Tool execution result"
    }],
    "isError": false
  }
}'''
        )

        self.prompter.instruct_with_key("make_server.step4.add_code")
        self.prompter.snippet(
            '''from mcp.types import Tool, TextContent
from typing import Sequence

@server.call_tool()
async def get_weather(name: str, state: str) -> Sequence[TextContent]:
    return [TextContent(type="text", text=f"Hello {state}")]'''
        )

    def run(self) -> bool:
        """Run the tutorial"""
        while self.current_step <= self.total_steps:
            if not self.check():
                if not self.run_step(self.current_step):
                    return False
            else:
                # if self.check():
                self.prompter.intense_instruct(f"You've done step:{self.current_step}")
                self.current_step += 1
            self.prompter.instruct("➤ 1Press any key")
            self.prompter.get_key()

        return self.check()
