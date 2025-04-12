import subprocess
from ..utils import Prompt
import subprocess
import os
from ..i18n import i18n

class MakingProject:
    def __init__(self):
        pass

    def run(self) -> bool:
        prompter = Prompt()
        prompter.box_with_key("make_project.title")

        prompter.instruct_with_key("make_project.instruction")
        prompter.instruct_with_key("make_project.command")

        while True:
            command = prompter.read(i18n.get("make_project.prompt"))
            if command == "hatch new mcp-weather":
                break
            prompter.warn(i18n.get("make_project.invalid_command"))

        try:
            if self.check():
                return True
            subprocess.run(["hatch", "new", "mcp-weather"])
        except:
            return False
        return self.check()

    def check(self) -> bool:
        return os.path.isdir("mcp-weather")
