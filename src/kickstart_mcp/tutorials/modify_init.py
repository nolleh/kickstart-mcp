from ..tutorial_base import TutorialBase
import os
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
        if not self.verify_file_exists(self.target_file):
            return False

        self.prompter.clear()
        self.prompter.box("Modify __init__.py")
        self.prompter.instruct("\nIn this tutorial, you'll learn how to modify the __init__.py file.")
        self.prompter.instruct("You'll need to add a main function that prints 'hello, world'.")
        self.prompter.instruct("\nAdd the following code to the file:")
        self.prompter.instruct("def main():")
        self.prompter.instruct("    print(\"hello, world\")")
        self.prompter.instruct("if __name__ == \"__main__\":")
        self.prompter.instruct("    main()")
        
        if not self.handle_editor_options(self.target_file):
            return False

        # Test the command
        self.prompter.instruct("\nLet's test if the command works:")
        try:
            result = subprocess.run(
                ["python", "-m", "mcp_weather"],
                cwd="mcp-weather",
                check=True,
                text=True,
                capture_output=True
            )
            self.prompter.instruct(result.stdout)
        except subprocess.CalledProcessError as e:
            self.prompter.error(f"Error running the command: {e.stderr}")
        return self.check()

    def check(self) -> bool:
        """Check if the __init__.py file has been modified correctly"""
        try:
            # Run the module and capture output
            result = subprocess.run(
                ["python", "-m", "mcp_weather"],
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
            
        except subprocess.CalledProcessError:
            return False 
