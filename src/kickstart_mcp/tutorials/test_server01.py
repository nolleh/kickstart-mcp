from ..tutorial_base import TutorialBase
import os

class TestServer01(TutorialBase):
    def __init__(self):
        super().__init__(
            name="TestServer01",
            description="Learn how to test the weather server using MCP Inspector"
        )
        self.current_step = 1
        self.total_steps = 1

    def check(self) -> bool:
        """Check if the tutorial is completed"""
        return self.current_step > self.total_steps

    def run_step(self, step_id: int) -> bool:
        """Run the tutorial step"""
        if step_id == 1:
            self.prompter.clear()
            self.prompter.box("Test Weather Server")
            self.prompter.instruct("\nNow let's run and test the mcp-weather server we've created.")
            self.prompter.instruct("Unlike previous tutorials, this one doesn't involve code writing or")
            self.prompter.instruct("verifying code editing completion. Instead, we'll")
            self.prompter.instruct("launch our MCPServer and test it through the inspector.")
            
            self.prompter.instruct("\nPlease follow the instructions to perform the test yourself.")
            
            self.prompter.snippet(
                '''$ npx @model_context_protocol/inspector''')
            self.prompter.snippet('''
Starting MCP inspector...
Proxy server listening on port 3000

🔍 MCP Inspector is up and running at http://localhost:5173 🚀'''
            )
            
            self.prompter.instruct("\nAccess http://localhost:5173 in your browser")
            self.prompter.instruct("Enter: STDIO, uv, --directory path/to/kickstart-mcp/mcp-weather run mcp-weather")
            self.prompter.instruct("Click connect to")
            self.prompter.instruct("list and test the tools.")
            
            self.prompter.instruct("\nAfter performing the test,")
            self.prompter.instruct("please refer to the following document.")
            
            self.prompter.instruct("\n➤ Press any key to open the reference document\n(open with system default application)")
            self.prompter.get_key()
            
            # Open the reference document
            # self.open_reference_document("test_server01.md")
            os.system("open ./tutorial/description/test_server01.md")
            return True
        return False

    def run(self) -> bool:
        """Run the tutorial"""
        while self.current_step <= self.total_steps:
            if not self.run_step(self.current_step):
                return False
            self.current_step += 1
        return True 
