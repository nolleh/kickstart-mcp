from ..utils import Prompt
import os

class MakingProject:
    def __init__(self, name):
        self.name = name

    def main(self):
        prompter = Prompt()
        prompter.box("1. Let's make a project")

        prompter.instruct("➤ hatch new mcp-weather")
      
        while True:
            command = prompter.read("Enter the command: ")
            if command == "hatch new mcp-weather":
                break
            prompter.instruct("Invalid command. Please try again.")

        os.system("hatch new mcp-weather")
        


