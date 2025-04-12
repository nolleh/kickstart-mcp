from typing import Optional
from ..tutorial_base import TutorialBase
from ..utils import Prompt
from pathlib import Path
from ..config import Config
import platform
from colorama import Fore, Style
import subprocess
from ..i18n import i18n

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
        self.prompter.box_with_key("hello_mcp.step1.title")
        self.prompter.instruct_with_key("hello_mcp.step1.welcome")
        self.prompter.instruct_with_key("hello_mcp.step1.intro")
        self.prompter.instruct_with_key("hello_mcp.step1.location")

        self.prompter.snippet(
            f"""# For {self.os_type}:
{self.target_file}"""
        )
        self.prompter.instruct_with_key("hello_mcp.step1.structure")
        self.prompter.snippet(
            """{
    "mcpServers": {}
}"""
        )

    def step2(self):
        self.prompter.clear()
        self.prompter.box_with_key("hello_mcp.step2.title")
        self.prompter.instruct_with_key("hello_mcp.step2.intro")
        self.prompter.instruct_with_key("hello_mcp.step2.update")
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
        self.prompter.intense_instruct_with_key("hello_mcp.step2.reminder")
        self.prompter.instruct_with_key("hello_mcp.step2.explanation")

    def step3(self):
        self.prompter.clear()
        self.prompter.box_with_key("hello_mcp.step3.title")
        self.prompter.instruct_with_key("hello_mcp.step3.intro")
        self.prompter.instruct_with_key("hello_mcp.step3.instruction")
        self.prompter.snippet(
            """node --version"""
        )
        self.prompter.instruct_with_key("hello_mcp.step3.restart")
        self.prompter.instruct_with_key("hello_mcp.step3.completion")

    def run(self) -> bool:
        """Run the tutorial"""
        self.prompter.clear()
        self.prompter.box_with_key("hello_mcp.title")

        # Introduction to MCP
        self.prompter.instruct_with_key("hello_mcp.intro1")
        self.prompter.instruct_with_key("hello_mcp.intro2")
        self.prompter.instruct_with_key("hello_mcp.intro3")
        self.prompter.instruct_with_key("hello_mcp.feature1")
        self.prompter.instruct_with_key("hello_mcp.feature2")
        self.prompter.instruct_with_key("hello_mcp.feature3")

        self.prompter.instruct_with_key("hello_mcp.more_info")
        self.prompter.instruct("docs/tutorials/description/hello_mcp.md")

        self.prompter.instruct_with_key("hello_mcp.choose_host")
        self.prompter.instruct_with_key("hello_mcp.available_options")
        print(Fore.YELLOW + Style.BRIGHT + i18n.get("hello_mcp.option1"))
        print(Fore.YELLOW + Style.BRIGHT + i18n.get("hello_mcp.option2"))
        print(Fore.YELLOW + Style.BRIGHT + i18n.get("hello_mcp.option3"))

        choice = input(Fore.GREEN + i18n.get("hello_mcp.enter_choice") + " ").strip()

        if choice == '1':
            self.target_file = self.config.claude_config_map[self.os_type]
            self.prompter.instruct_with_key("hello_mcp.choice1")
        elif choice == '2':
            self.target_file = self.config.cursor_config_map[self.os_type]
            self.prompter.instruct_with_key("hello_mcp.choice2")
        elif choice == '3':
            self.target_file = self.config.custom_config_map[self.os_type]
            self.prompter.instruct_with_key("hello_mcp.choice3")
        else:
            print(Fore.RED + i18n.get("hello_mcp.invalid_choice"))
            return False

        while self.current_step <= self.total_steps:
            if not self.check():
                if not self.run_step(self.current_step):
                    return False
            else:
                self.prompter.intense_instruct(
                    i18n.get("hello_mcp.step_complete", str(self.current_step))
                )
                self.current_step += 1
            self.prompter.instruct_with_key("hello_mcp.press_continue")
            self.prompter.get_key()

        return True
