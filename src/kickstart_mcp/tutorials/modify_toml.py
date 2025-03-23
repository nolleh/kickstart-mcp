from ..utils import Prompt
import os
import tomli
import tomli_w
import subprocess
import platform

class ModifyToml:
    def __init__(self, name):
        self.name = name
        self.project_dir = "mcp-weather"
        self.editor = self._get_default_editor()

    def _get_default_editor(self):
        """Get the default editor based on environment variables or system preferences"""
        # Check environment variables first
        editor = os.environ.get('EDITOR') or os.environ.get('VISUAL')
        if editor:
            return editor

        # Check common editors based on OS
        if platform.system() == 'Darwin':  # macOS
            if os.path.exists('/usr/local/bin/code'):  # VS Code
                return 'code'
            elif os.path.exists('/usr/local/bin/subl'):  # Sublime Text
                return 'subl'
        elif platform.system() == 'Linux':
            if os.path.exists('/usr/bin/code'):  # VS Code
                return 'code'
            elif os.path.exists('/usr/bin/subl'):  # Sublime Text
                return 'subl'
        elif platform.system() == 'Windows':
            if os.path.exists('C:\\Program Files\\Microsoft VS Code\\Code.exe'):
                return 'code'
            elif os.path.exists('C:\\Program Files\\Sublime Text\\subl.exe'):
                return 'subl'
        
        # Fallback to nano
        return 'nano'

    def _open_in_editor(self, file_path):
        """Open the file in the selected editor"""
        try:
            if self.editor in ['code', 'subl']:
                # VS Code and Sublime Text are non-blocking
                subprocess.Popen([self.editor, file_path])
            else:
                # Other editors (like nano, vim) are blocking
                subprocess.run([self.editor, file_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error opening editor: {e}")
            return False
        return True

    def main(self):
        prompter = Prompt()
        prompter.box("2. Let's modify pyproject.toml")

        # Check if project exists
        if not os.path.exists(self.project_dir):
            prompter.error("Project directory not found. Please complete the previous tutorial first.")
            return

        toml_path = os.path.join(self.project_dir, "pyproject.toml")
        if not os.path.exists(toml_path):
            prompter.error("pyproject.toml not found. Please complete the previous tutorial first.")
            return

        # Read current toml content
        with open(toml_path, "rb") as f:
            toml_data = tomli.load(f)

        prompter.instruct("Now we need to add a script entry to your pyproject.toml file.")
        prompter.instruct("Add the following under [project]:")
        prompter.intense_instruct("[project.scripts]")
        prompter.intense_instruct("mcp-weather = mcp_weather:main")

        while True:
            # Show current content
            prompter.instruct("\nCurrent pyproject.toml content:")
            # with open(toml_path, "r") as f:
            #     prompter.instruct(f.read())

            # Get user input
            prompter.instruct("\nWould you like to:")
            prompter.instruct("1. Edit the file")
            prompter.instruct("2. Check if changes are correct")
            prompter.instruct("3. Change editor")
            prompter.instruct("4. Exit")
            
            choice = prompter.read("Enter your choice (1-4): ")

            if choice == "1":
                prompter.instruct(f"Opening file in {self.editor}...")
                if self._open_in_editor(toml_path):
                    prompter.instruct("File opened in editor. Make your changes and save the file.")
                    prompter.instruct("After saving, you can check if your changes are correct.")
                else:
                    prompter.error("Failed to open the file in editor. Please try again.")
                
            elif choice == "2":
                # Read the current state
                with open(toml_path, "rb") as f:
                    current_data = tomli.load(f)
                
                # Check if the script entry exists
                if "project" in current_data and "scripts" in current_data["project"]:
                    scripts = current_data["project"]["scripts"]
                    if "mcp-weather" in scripts and scripts["mcp-weather"] == "mcp_weather:main":
                        prompter.success("Correct! You've successfully added the script entry.")
                        # Test the command
                        prompter.instruct("\nLet's test if the command works:")
                        os.system("cd mcp-weather && hatch run mcp-weather --help")
                        break
                    else:
                        prompter.error("The script entry is not correct. Please try again.")
                else:
                    prompter.error("The [project.scripts] section is missing. Please try again.")
            
            elif choice == "3":
                prompter.instruct("Available editors:")
                prompter.instruct("1. VS Code (code)")
                prompter.instruct("2. Sublime Text (subl)")
                prompter.instruct("3. Nano (nano)")
                prompter.instruct("4. Vim (vim)")
                
                editor_choice = prompter.read("Enter your choice (1-4): ")
                editor_map = {
                    "1": "code",
                    "2": "subl",
                    "3": "nano",
                    "4": "vim"
                }
                
                if editor_choice in editor_map:
                    self.editor = editor_map[editor_choice]
                    prompter.success(f"Editor changed to {self.editor}")
                else:
                    prompter.error("Invalid choice. Keeping current editor.")
            
            elif choice == "4":
                prompter.instruct("Exiting tutorial. You can come back later to complete it.")
                break
            
            else:
                prompter.error("Invalid choice. Please try again.") 
