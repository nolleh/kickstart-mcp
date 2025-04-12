from ..tutorial_base import TutorialBase
import os


class TestServer01(TutorialBase):
    def __init__(self):
        super().__init__(
            name="TestServer01",
            description="Learn how to test the weather server using MCP Inspector",
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
            self.prompter.box_with_key("test_server01.title")
            self.prompter.instruct_with_key("test_server01.intro1")
            self.prompter.instruct_with_key("test_server01.intro2")

            self.prompter.instruct_with_key("test_server01.follow")

            self.prompter.snippet("""$ npx @model_context_protocol/inspector""")
            self.prompter.snippet(
                """
Starting MCP inspector...
Proxy server listening on port 3000

🔍 MCP Inspector is up and running at http://localhost:5173 🚀"""
            )

            self.prompter.instruct_with_key("test_server01.access")
            self.prompter.instruct_with_key("test_server01.enter")
            self.prompter.instruct_with_key("test_server01.connect")

            self.prompter.instruct_with_key("test_server01.after_test")

            self.prompter.instruct_with_key("test_server01.press_key")
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
