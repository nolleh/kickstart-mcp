import subprocess
from ..utils import Prompt
import subprocess
import os

class MakingProject:
    def __init__(self):
        pass

    def run(self) -> bool:
        prompter = Prompt()
        prompter.box("1. Let's make a project")

        prompter.instruct("Enter below command to create a new project.")
        prompter.instruct("➤ hatch new mcp-weather")
      
        while True:
            command = prompter.read("Enter the command: ")
            if command == "hatch new mcp-weather":
                break
            prompter.warn("Invalid command. Please try again.")

        try:
            if self.check():
                return True
            subprocess.run(["hatch", "new", "mcp-weather"])
        except:
            return False
        return self.check()

    def check(self) -> bool:
        return os.path.isdir("mcp-weather")
        


