from typing import Optional
from ..tutorial_base import TutorialBase
from ..utils import Prompt
from pathlib import Path

class ImplementSseTransport(TutorialBase):
    def __init__(self):
        super().__init__(
            name="ImplementSseTransport",
            description="Learn how to implement SSE transport for your MCP server"
        )
        self.target_file = "mcp-weather/src/mcp_weather/__init__.py"
        self.current_step = 1
        self.total_steps = 3

    def check(self) -> bool:
        """Check if a specific step is completed"""
        if not self.verify_file_exists(self.target_file):
            self.prompter.warn("Did you complete the previous ImplementWeather tutorial first?")
            return False

        content = Path(self.target_file).read_text()

        if self.current_step == 1:
            return "run_server" in content and "transport: str = \"stdio\"" in content
        elif self.current_step == 2:
            return "SseServerTransport" in content and "starlette.applications" in content
        elif self.current_step == 3:
            return "uvicorn.Config" in content and "server.serve()" in content
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
        self.prompter.box_with_key("implement_sse.step1.title")
        self.prompter.intense_instruct_with_key("implement_sse.step1.intro1")
        self.prompter.intense_instruct_with_key("implement_sse.step1.intro2")

        self.prompter.instruct_with_key("implement_sse.step1.transport_types.title")
        self.prompter.instruct_with_key("implement_sse.step1.transport_types.1")
        self.prompter.instruct_with_key("implement_sse.step1.transport_types.2")
        self.prompter.instruct_with_key("implement_sse.step1.add_function")
        self.prompter.instruct_with_key("implement_sse.step1.add_code")
        self.prompter.snippet(
            '''async def run_server(transport: str = "stdio", port: int = 8000) -> None:
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
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
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
        sse_server = uvicorn.Server(config)
        # Use sse_server.serve() instead of run() to stay in the same event loop
        await sse_server.serve()
    else:
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream, write_stream, app.create_initialization_options()
            )'''
        )

    def step2(self):
        self.prompter.clear()
        self.prompter.box_with_key("implement_sse.step2.title")
        self.prompter.instruct_with_key("implement_sse.step2.intro1")
        self.prompter.instruct_with_key("implement_sse.step2.intro2")
        self.prompter.snippet(
            '''starlette>=0.27.0
uvicorn>=0.24.0'''
        )
        self.prompter.instruct_with_key("implement_sse.step2.intro3")

    def step3(self):
        self.prompter.clear()
        self.prompter.box_with_key("implement_sse.step3.title")
        self.prompter.instruct_with_key("implement_sse.step3.intro1")
        self.prompter.instruct_with_key("implement_sse.step3.intro2")
        self.prompter.snippet(
            '''if __name__ == "__main__":
    import asyncio
    import argparse

    parser = argparse.ArgumentParser(description="Run the MCP Weather Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio", help="Transport type to use")
    parser.add_argument("--port", type=int, default=8000, help="Port to use for SSE transport")
    args = parser.parse_args()

    asyncio.run(run_server(transport=args.transport, port=args.port))'''
        )
        self.prompter.instruct_with_key("implement_sse.step3.intro3")
        self.prompter.instruct_with_key("implement_sse.step3.intro4")
        self.prompter.instruct_with_key("implement_sse.step3.intro5")

    def run(self) -> bool:
        """Run the tutorial"""
        while self.current_step <= self.total_steps:
            if not self.check():
                if not self.run_step(self.current_step):
                    return False
            else:
                self.prompter.intense_instruct_with_key("implement_sse.step_complete", self.current_step)
                self.current_step += 1
            self.prompter.instruct_with_key("implement_sse.press_continue")
            self.prompter.get_key()

        return True
