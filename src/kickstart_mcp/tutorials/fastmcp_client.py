from typing import Optional
from ..tutorial_base import TutorialBase
from ..utils import Prompt
from pathlib import Path


class FastMcpClient(TutorialBase):
    def __init__(self):
        super().__init__(
            name="FastMcpClient",
            description="Learn how to build an MCP client that connects to any MCP server and interacts with LLMs and tools.",
        )
        self.target_file = "mcp-client/src/mcp_client/client.py"
        self.current_step = 1
        self.total_steps = 5

    def check(self) -> bool:
        """Check if a specific step is completed"""
        if self.current_step == 1:
            # Check for pyproject.toml with correct dependencies
            pyproject_path = Path("mcp-client/pyproject.toml")
            if not pyproject_path.exists():
                return False
            content = pyproject_path.read_text()
            return (
                "mcp" in content and "anthropic" in content and "python-dotenv" in content
            )
        elif self.current_step == 2:
            # Check for client.py with basic structure and connect_to_server
            if not self.verify_file_exists(self.target_file):
                return False
            content = Path(self.target_file).read_text()
            return (
                "class MCPClient" in content and "connect_to_server" in content
            )
        elif self.current_step == 3:
            # Check for process_query implementation
            if not self.verify_file_exists(self.target_file):
                return False
            content = Path(self.target_file).read_text()
            return (
                "process_query" in content and "anthropic.messages.create" in content
            )
        elif self.current_step == 4:
            # Check for chat loop and main entry point
            if not self.verify_file_exists(self.target_file):
                return False
            content = Path(self.target_file).read_text()
            return (
                "async def chat_loop(self):" in content and "async def cleanup(self):" in content
            )
        elif self.current_step == 5:
            target = "mcp-client/src/mcp_client/__init__.py"
            if not self.verify_file_exists(target):
                return False
            content = Path(target).read_text()
            return (
                "def main" in content and "async def run()" in content
            )

        return False

    def run_step(self, step_id: int) -> bool:
        if step_id == 1:
            self.step1()
        elif step_id == 2:
            self.step2()
        elif step_id == 3:
            self.step3()
        elif step_id == 4:
            self.step4()
        elif step_id == 5:
            self.step5()
        if not self.handle_editor_options(self.target_file if step_id > 1 else "mcp-client/pyproject.toml"):
            return False
        return True

    def step1(self):
        self.prompter.clear()
        self.prompter.box_with_key("fastmcp_client.step1.title")
        self.prompter.instruct_with_key("fastmcp_client.step1.intro1")
        self.prompter.instruct_with_key("fastmcp_client.step1.intro2")
        self.prompter.snippet(
            """# In your terminal:
$ hatch new mcp-client
## Or use uv init and configure project by your self
$ cd mcp-client

# Add dependencies
$ uv add mcp anthropic python-dotenv
"""
        )
        self.prompter.instruct_with_key("fastmcp_client.step1.intro3")

    def step2(self):
        self.prompter.clear()
        self.prompter.box_with_key("fastmcp_client.step2.title")
        self.prompter.instruct_with_key("fastmcp_client.step2.intro1")
        self.prompter.instruct_with_key("fastmcp_client.step2.intro2")
        self.prompter.snippet(
            """import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from anthropic import Anthropic
from dotenv import load_dotenv
import sys

load_dotenv()  # Load environment variables from .env

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_server(self, server_script_path: str):
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError('Server script must be a .py or .js file')
        command = 'python' if is_python else 'node'

        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        await self.session.initialize()

        response = await self.session.list_tools()
        tools = response.tools
        print('Connected to server with tools:', [tool.name for tool in tools])"""
        )
        self.prompter.instruct_with_key("fastmcp_client.step2.intro3")

    def step3(self):
        self.prompter.clear()
        self.prompter.box_with_key("fastmcp_client.step3.title")
        self.prompter.instruct_with_key("fastmcp_client.step3.intro1")
        self.prompter.snippet(
            """
    async def process_query(self, query: str) -> str:
        messages = [
            {"role": "user", "content": query}
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )

        final_text = []
        assistant_message_content = []
        for content in response.content:
            if content.type == 'text':
                final_text.append(content.text)
                assistant_message_content.append(content)
            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input
                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")
                assistant_message_content.append(content)
                messages.append({"role": "assistant", "content": assistant_message_content})
                messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": content.id, "content": result.content}]})
                response = self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    messages=messages,
                    tools=available_tools
                )
                final_text.append(response.content[0].text)
        return "\n".join(final_text)"""
        )
        self.prompter.instruct_with_key("fastmcp_client.step3.intro2")

    def step4(self):
        self.prompter.clear()
        self.prompter.box_with_key("fastmcp_client.step4.title")
        self.prompter.instruct_with_key("fastmcp_client.step4.intro1")
        self.prompter.snippet(
            """
    async def chat_loop(self):
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == 'quit':
                    break
                response = await self.process_query(query)
                print("\n" + response)
            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        await self.exit_stack.aclose()
    """
        )

    def step5(self):
        self.prompter.clear()
        self.prompter.box_with_key("fastmcp_client.step5.title")
        self.prompter.instruct_with_key("fastmcp_client.step5.intro1")
        self.prompter.snippet(
            """
from .client import MCPClient
import asyncio
import sys
async def run():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

def main():
    asyncio.run(run())

if __name__ == "__main__":
    main()"""
        )
        self.prompter.instruct_with_key("fastmcp_client.step5.intro2")
        self.prompter.instruct_with_key("fastmcp_client.step5.intro3")
        self.prompter.instruct_with_key("fastmcp_client.step5.intro4")

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
