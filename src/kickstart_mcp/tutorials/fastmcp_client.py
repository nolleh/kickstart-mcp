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
        self.total_steps = 3

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
            # Check for client.py with basic structure
            if not self.verify_file_exists(self.target_file):
                return False
            content = Path(self.target_file).read_text()
            return (
                "class MCPClient" in content and "connect_to_server" in content and "process_query" in content
            )
        elif self.current_step == 3:
            # Check for main entry point and chat loop
            if not self.verify_file_exists(self.target_file):
                return False
            content = Path(self.target_file).read_text()
            return (
                "async def chat_loop" in content
            )
        return False

    def run_step(self, step_id: int) -> bool:
        if step_id == 1:
            self.step1()
        elif step_id == 2:
            self.step2()
        elif step_id == 3:
            self.step3()
        if not self.handle_editor_options(self.target_file if step_id > 1 else "mcp-client/pyproject.toml"):
            return False
        return True

    def step1(self):
        self.prompter.clear()
        self.prompter.box("MCP Client Tutorial: Step 1 - Environment Setup")
        self.prompter.instruct(
            "In this step, you'll set up your Python environment and install the required dependencies for building an MCP client. We'll use a modern, isolated environment and follow best practices."
        )
        self.prompter.instruct(
            "1. Create a new project directory and initialize it with a pyproject.toml file.\n2. Confiure virtual enviorment/project configuration with your favorite tools.(in this tutorial, used hatch)\n3. Add the required dependencies: mcp, anthropic, python-dotenv."
        )
        self.prompter.snippet(
            """# In your terminal:
$ hatch new mcp-client
## Or use uv init and configure project by your self
$ cd mcp-client

# Add dependencies
$ uv add mcp anthropic python-dotenv
"""
        )
        self.prompter.instruct(
            "Make sure your pyproject.toml includes these dependencies. This ensures your client can communicate with MCP servers and use the Anthropic API."
        )

    def step2(self):
        self.prompter.clear()
        self.prompter.box("MCP Client Tutorial: Step 2 - Writing the Client Code")
        self.prompter.instruct(
            "Now, let's write the core client code. This client will connect to any MCP server, list available tools, and interact with LLMs (like Claude) to process queries and call tools."
        )
        self.prompter.instruct(
            "1. Create a file named client.py in your mcp-client directory(src/mcp_client/client.py).\n2. Add the following code to set up the basic structure, following best practices for async resource management and environment loading."
        )
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
        print('\nConnected to server with tools:', [tool.name for tool in tools])

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
        return "\n".join(final_text)
"""
        )
        self.prompter.instruct(
            "This code sets up the client, connects to a server, lists tools, and processes queries using Claude and tool calls."
        )

    def step3(self):
        self.prompter.clear()
        self.prompter.box("MCP Client Tutorial: Step 3 - Running and Using the Client")
        self.prompter.instruct(
            "Finally, let's add the interactive chat loop and the main entry point. This will allow you to run your client and interact with any MCP server."
        )
        self.prompter.snippet(
            """    async def chat_loop(self):
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

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())
"""
        )
        self.prompter.instruct(
            "Now you can run your client with: python client.py <path_to_server_script>. Try connecting to your weather server or any other MCP server!"
        )
        self.prompter.instruct(
            "Congratulations! You've built a fully functional MCP client. You can now explore, extend, and integrate with any MCP-compatible server and tools."
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
