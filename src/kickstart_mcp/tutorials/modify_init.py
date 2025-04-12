from ..tutorial_base import TutorialBase
import subprocess

class ModifyInit(TutorialBase):
    def __init__(self):
        super().__init__(
            name="ModifyInit",
            description="Learn how to modify the __init__.py file to add a main function"
        )
        self.target_file = "mcp-weather/src/mcp_weather/__init__.py"

    def run(self) -> bool:
        """Run the tutorial"""
        self.prompter.clear()
        self.prompter.box_with_key("modify_init.title")
        self.prompter.instruct_with_key("modify_init.intro1")
        self.prompter.instruct_with_key("modify_init.intro2")
        self.prompter.instruct_with_key("modify_init.intro3")

        code_snippet = '''def main():
    print("hello, world")

if __name__ == "__main__":
    main()'''
        self.prompter.snippet(code_snippet)

        if not self.verify_file_exists(self.target_file):
            self.prompter.warn_with_key("modify_init.warning")
            return False

        if not self.handle_editor_options(self.target_file):
            return False

        return self.check()

    def check(self) -> bool:
        """Check if the __init__.py file has been modified correctly"""
        try:
            # Run the module and capture output
            result = subprocess.run(
                ["hatch", "run", "mcp-weather"],
                cwd="mcp-weather",
                check=True,
                text=True,
                capture_output=True
            )

            # Check if the output matches "hello, world" (ignoring whitespace)
            output = result.stdout.strip()
            expected = "hello, world"

            # Compare strings ignoring whitespace
            return output == expected

        except subprocess.CalledProcessError as e:
            return False
