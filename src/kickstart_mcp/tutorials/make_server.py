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
            self.prompter.warn("Did you made the mcp-weather project?. \nDo previous tutorial first")
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
        self.prompter.box("Step 1: Create Server Instance")
        self.prompter.instruct("\nIn this step, you'll create a server instance with a lifespan manager.")
        self.prompter.instruct("\nLet's break down what each part does:")
        self.prompter.instruct("\n1. @asynccontextmanager decorator:")
        self.prompter.instruct("   - This decorator helps manage the server's lifecycle")
        self.prompter.instruct("   - It ensures proper setup and cleanup of server resources")
        self.prompter.instruct("   - Similar to a context manager (with statement) but for async code")
        
        self.prompter.instruct("\n2. server_lifespan function:")
        self.prompter.instruct("   - Manages the server's lifecycle events")
        self.prompter.instruct("   - yield server.name: Provides context (in here, server.name) during its active lifetime")
        self.prompter.intense_instruct("   - This context can be retrieved by accessing server.request_context")
        self.prompter.instruct("   - The finally block: Place for cleanup code when server shuts down")
        
        self.prompter.instruct("\n3. Server instance creation:")
        self.prompter.instruct("   - Creates a new mcp.server named 'weather'")
        self.prompter.instruct("   - Attaches the lifespan manager to handle lifecycle events")
        
        
        self.prompter.instruct("\nAdd the following code to the file:")
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
        self.prompter.instruct("You also need to add dependency in project.toml file")

    def step2(self):
        self.prompter.clear()
        self.prompter.box("Step 2: Add Run Function and Main")
        self.prompter.instruct("\nIn this step, you'll add the run function and main entry point.")
        self.prompter.instruct("\nMCP servers can be implemented in two ways:")
        self.prompter.instruct("1. Local server via standard input/output (stdio)")
        self.prompter.instruct("   - Direct communication through stdin/stdout")
        self.prompter.instruct("   - Many MCP Servers are distributed with package that runnable with npx, uv")
        self.prompter.instruct("   - So, MCP Host often directly run mcp server in local environment")
        
        self.prompter.instruct("\n2. HTTP server via Server-Sent Events (SSE)")
        self.prompter.instruct("   - Web-based communication using SSE")
        self.prompter.instruct("   - More complex but allows remote connections")
        self.prompter.intense_instruct("   - Some MCP Host doesn't support this type of connection.")

        self.prompter.instruct("\nIn this tutorial, we'll implement a stdio server for simplicity.")
        self.prompter.instruct("The run function will set up the communication channel using stdio_server.")
        
        self.prompter.instruct("\nAdd the following code to the file:")
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
        self.prompter.instruct("You also need to add dependency in project.toml file")

    def step3(self):
        self.prompter.clear()
        self.prompter.box("Step 3: Add Tools")
        self.prompter.instruct("\nTools are one of the core features of Model Context Protocol (MCP).")
        self.prompter.instruct("They enable AI models to interact with external systems and perform actual tasks.")
        
        self.prompter.instruct("\nKey points about Tools:")
        self.prompter.instruct("1. Model-centric control:")
        self.prompter.instruct("   - Designed for model-centric control")
        self.prompter.instruct("   - AI models can understand context and automatically find and call tools")
        
        self.prompter.instruct("\n2. Safety and reliability:")
        self.prompter.instruct("   - User approval is always required for actual tool execution")
        self.prompter.instruct("   - Ensures safe and controlled interaction with external systems")
        
        self.prompter.instruct("\n3. Input Schema:")
        self.prompter.instruct("   - Defines the structure of input parameters for each tool")
        self.prompter.instruct("   - Uses JSON Schema format to specify:")
        self.prompter.instruct("     * Parameter types")
        self.prompter.instruct("     * Parameter descriptions")
        self.prompter.instruct("     * Required parameters")

        self.prompter.instruct("\nTools structure")
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
        
        self.prompter.instruct("\nAdd the following code to the file:")
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
        self.prompter.box("Step 4: Implement Tool Handler")
        self.prompter.instruct("\nNow we'll implement the tool handler using ModelContextProtocol's call_tool.")
        self.prompter.instruct("The tool handler is called based on the tool information received through list_tools.")
        
        self.prompter.instruct("\nTool Call Request Format:")
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
        
        self.prompter.instruct("\nTool Call Response Format:")
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
        
        self.prompter.instruct("\nAdd the following code to the file:")
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
