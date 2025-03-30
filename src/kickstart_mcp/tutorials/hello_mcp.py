from typing import Optional
from ..tutorial_base import TutorialBase
from ..utils import Prompt
from pathlib import Path
from ..config import Config
import platform
from colorama import Fore, Style
import subprocess

class HelloMcp(TutorialBase):
    def __init__(self):
        super().__init__(
            name="HelloMcp",
            description="Learn how to set up and use Model Context Protocol (MCP) with different hosts",
        )
        self.config = Config()
        self.os_type = platform.system()
        self.current_step = 1
        self.total_steps = 3

    def check(self) -> bool:
        """Check if a specific step is completed"""
        if self.current_step == 1:
            return self.verify_file_exists(self.target_file)
        elif self.current_step == 2:
            content = Path(self.target_file).read_text()
            return "mcpServers" in content
        elif self.current_step == 3:
            try:
                subprocess.run(["node", "--version"], capture_output=True, check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
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
        self.prompter.box("Step 1: Create MCP Configuration File")
        self.prompter.instruct(
            "\nWelcome to the HelloMcp tutorial! We'll help you set up Model Context Protocol (MCP) with your preferred host."
        )
        self.prompter.instruct(
            "\nFirst, let's create a basic MCP configuration file. This file will be used to configure MCP for your chosen host."
        )
        self.prompter.instruct(
            "\nThe configuration file will be created at the following location based on your operating system:"
        )

        self.prompter.snippet(
            f"""# For {self.os_type}:
{self.target_file}"""
        )
        self.prompter.instruct(
            "\nLet's create a basic configuration file structure:"
        )
        self.prompter.snippet(
            """{
    "mcpServers": {}
}"""
        )

    def step2(self):
        self.prompter.clear()
        self.prompter.box("Step 2: Configure MCP Servers")
        self.prompter.instruct(
            "\nNow that we have our basic configuration file, let's add the filesystem server to enable file operations."
        )
        self.prompter.instruct(
            "\nUpdate your configuration file with the following content:"
        )
        self.prompter.snippet(
            """{
    "mcpServers": {
        "filesystem": {
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "/Users/username/Desktop",
                "/Users/username/Downloads"
            ]
        }
    }
}"""
        )
        self.prompter.intense_instruct(
            "Remember to replace 'username' with your actual username"
        )
        self.prompter.instruct(
            "\nThis configuration enables the filesystem server, which allows MCP to interact with your files."
        )

    def step3(self):
        self.prompter.clear()
        self.prompter.box("Step 3: Install Required Dependencies")
        self.prompter.instruct(
            "\nTo use the filesystem server, we need to install Node.js and the required npm package."
        )
        self.prompter.instruct(
            "\nFirst, ensure you have Node.js installed. Then run:"
        )
        self.prompter.snippet(
            """node --version"""
        )
        self.prompter.instruct(
            "\nAfter installation, restart your application to apply the changes."
        )
        self.prompter.instruct(
            "\nYou should now see the hammer icon (🔨) in the bottom right corner of the input box."
        )

    def run(self) -> bool:
        """Run the tutorial"""
        self.prompter.clear()
        self.prompter.box("Welcome to HelloMcp Tutorial")
        
        # Introduction to MCP
        self.prompter.instruct(
            "\nModel Context Protocol (MCP) is an open protocol that standardizes how applications provide context to LLMs."
        )
        self.prompter.instruct(
            "Think of MCP like a USB-C port for AI applications - it provides a standardized way to connect AI models to different data sources and tools."
        )
        self.prompter.instruct(
            "\nMCP helps you build agents and complex workflows on top of LLMs by providing:"
        )
        self.prompter.instruct("• Pre-built integrations that your LLM can directly plug into")
        self.prompter.instruct("• Flexibility to switch between LLM providers and vendors")
        self.prompter.instruct("• Best practices for securing your data within your infrastructure")
        
        self.prompter.instruct(
            "\nFor more detailed information about MCP, please check the tutorial description at:"
        )
        self.prompter.instruct("docs/tutorials/description/hello_mcp.md")
        
        self.prompter.instruct(
            "\nNow, let's choose your MCP host. The host is the application that will use MCP to interact with various tools and data sources."
        )
        self.prompter.instruct(
            "\nAvailable options:"
        )
        print(Fore.YELLOW + Style.BRIGHT + "➤ 1. Claude Desktop - Anthropic's AI assistant with MCP support")
        print(Fore.YELLOW + Style.BRIGHT + "➤ 2. Cursor - AI-powered code editor with MCP integration")
        print(Fore.YELLOW + Style.BRIGHT + "➤ 3. Custom - Set up MCP for your own application")
        
        choice = input(Fore.GREEN + "\nEnter the number of your choice: ").strip()
        
        if choice == '1':
            self.target_file = self.config.claude_config_map[self.os_type]
            self.prompter.instruct("\nGreat choice! We'll set up MCP for Claude Desktop.")
        elif choice == '2':
            self.target_file = self.config.cursor_config_map[self.os_type]
            self.prompter.instruct("\nExcellent! We'll configure MCP for Cursor.")
        elif choice == '3':
            self.target_file = self.config.custom_config_map[self.os_type]
            self.prompter.instruct("\nPerfect! We'll set up a custom MCP configuration.")
        else:
            print(Fore.RED + "Invalid choice. Please select 1, 2, or 3.")
            return False

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
