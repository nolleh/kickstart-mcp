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
        self.total_steps = 2  # We'll update this as more steps are added

    def check(self) -> bool:
        """Check if a specific step is completed"""
        if not self.verify_file_exists(self.target_file):
            self.prompter.warn("Did you made the mcp-weather project?. \nDo previous tutorial first")
            return False

        content = Path(self.target_file).read_text()
        self.prompter.intense_instruct("read file..")
        self.prompter.snippet(content)

        if self.current_step == 1:
            # Check if server instance is created
            # content = self.read_target_file()
            return "server = Server" in content and "@asynccontextmanager" in content
        elif self.current_step == 2:
            # Check if run function and main are added
            # content = self.read_target_file()
            return "async def run()" in content and "def main()" in content
        return False

    def run_step(self, step_id: int) -> bool:
        """Run a specific step of the tutorial"""
        print("run the tutorial")
        if step_id == 1:
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
from mcp.server.stdio import stdio_server
from mcp.server.stdio.stdio_server import InitializationOptions
from mcp.server.stdio.stdio_server import NotificationOptions

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
            self.handle_editor_options(self.target_file)
        elif step_id == 2:
            self.prompter.clear()
            self.prompter.box("Step 2: Add Run Function and Main")
            self.prompter.instruct("\nIn this step, you'll add the run function and main entry point.")
            self.prompter.instruct("\nAdd the following code to the file:")
            self.prompter.snippet(
                '''async def run():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, 
                         write_stream, InitializationOptions(
                         server_name = "weather",
                         server_version = "0.1.0",
                         capabilities = server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={}
                         )))

def main():
    import asyncio
    asyncio.run(run())'''
            )
            self.handle_editor_options(self.target_file)
        return self.check()

    def run(self) -> bool:
        """Run the tutorial"""
        while self.current_step <= self.total_steps:
            if not self.check():
                if not self.run_step(self.current_step):
                    return False
            else:
                self.prompter.intense_instruct(f"You've done step:{self.current_step}")
                self.prompter.instruct("➤ Press any key") 
                self.prompter.get_key()
                self.current_step += 1

        return self.current_step == self.total_steps
