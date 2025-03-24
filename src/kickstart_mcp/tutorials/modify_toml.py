from ..tutorial_base import TutorialBase
import os
import tomli
import tomli_w
import subprocess
import platform
from colorama import Fore, Style
from typing import Any

class ModifyToml(TutorialBase):
    def __init__(self):
        super().__init__(
            name="Modify pyproject.toml",
            description="Learn how to modify the pyproject.toml file"
        )
        self.target_file = "pyproject.toml"
        self.expected_content = {
            "project": {
                "name": "kickstart-mcp",
                "version": "0.1.0",
                "description": "A tutorial for learning MCP",
                "authors": [
                    {"name": "Your Name", "email": "your.email@example.com"}
                ],
                "dependencies": [
                    "click",
                    "colorama"
                ],
                "requires-python": ">=3.8",
                "readme": "README.md",
                "license": {"text": "MIT"},
                "keywords": ["tutorial", "mcp", "learning"],
                "classifiers": [
                    "Development Status :: 3 - Alpha",
                    "Intended Audience :: Developers",
                    "License :: OSI Approved :: MIT License",
                    "Programming Language :: Python :: 3",
                    "Programming Language :: Python :: 3.8",
                    "Programming Language :: Python :: 3.9",
                    "Programming Language :: Python :: 3.10",
                    "Programming Language :: Python :: 3.11",
                    "Topic :: Software Development :: Libraries :: Python Modules",
                ],
                "urls": {
                    "Homepage": "https://github.com/yourusername/kickstart-mcp",
                    "Bug Tracker": "https://github.com/yourusername/kickstart-mcp/issues",
                },
            },
            "build-system": {
                "requires": ["hatchling"],
                "build-backend": "hatchling.build",
            },
        }
        self.project_dir = "mcp-weather"
        self.editor = self._get_default_editor()

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

    def check(self) -> bool:
        """Check if the pyproject.toml file has been modified correctly"""
        try:
            # Check if project exists
            if not os.path.exists(self.project_dir):
                self.prompter.error("Project directory not found. Please complete the previous tutorial first.")
                return False

            toml_path = os.path.join(self.project_dir, "pyproject.toml")
            if not os.path.exists(toml_path):
                self.prompter.error("pyproject.toml not found. Please complete the previous tutorial first.")
                return False
            
            with open(toml_path, "rb") as f:
                content = tomli.load(f)
            
            # Check if all required sections exist
            if "project" not in content or "build-system" not in content:
                return False
            
            project = content["project"]

            # Check if all required fields exist and have correct types
            required_fields = {
                "name": str,
                "description": str,
                "authors": list,
                "dependencies": list,
                "requires-python": str,
                "readme": str,
                "license": str,
                "keywords": list,
            }
            
            for field, field_type in required_fields.items():
                if field not in project or not isinstance(project[field], field_type):
                    self.prompter.warn(f"there isn't required field in project {field}")
                    return False
            
            if project.get("requires-python") != ">=3.10":
                return False

            # Check if dependencies include required packages
            # required_deps = {"click", "colorama"}
            # if not all(dep in project["dependencies"] for dep in required_deps):
            #     return False
            #
            # # Check if license is MIT
            # if project["license"].get("text") != "MIT":
            #     return False
           
            # Check if build-system is correct
            build_system = content["build-system"]
            if (build_system.get("requires") != ["hatchling"] or 
                build_system.get("build-backend") != "hatchling.build"):
                return False
            
            # Check if scripts section exists and is correct
            if "scripts" not in project:
                return False
            
            scripts = project["scripts"]
            if "mcp-weather" not in scripts or scripts["mcp-weather"] != "mcp_weather:main":
                return False
            
            return True
            
        except Exception:
            return False

    def run(self) -> bool:
        prompter = self.prompter
        prompter.box("2. Let's modify pyproject.toml")

        # Check if project exists
        if not os.path.exists(self.project_dir):
            prompter.error("Project directory not found. Please complete the previous tutorial first.")
            return False

        toml_path = os.path.join(self.project_dir, "pyproject.toml")
        if not os.path.exists(toml_path):
            prompter.error("pyproject.toml not found. Please complete the previous tutorial first.")
            return False

        def _open(toml_path, mode: str) -> dict[str, Any] | None:
            with open(toml_path, mode) as f:
                try:
                    toml_data = tomli.load(f)
                    return toml_data
                except (tomli.TOMLDecodeError) as e:
                    prompter.error(f"could not decode as toml, did you write it correctly? {e}")
                    return None


        # Read current toml content
        if not _open(toml_path,  "rb"):
            return False

        prompter.instruct("Now We need to use mcp library and it requires python 3.10, so update minimum python version.")
        prompter.instruct("Modify requires_python")
        prompter.snippet('''requires-python = ">=3.10"''')

        prompter.instruct("Also, we need to add a script entry to your pyproject.toml file.")
        prompter.instruct("Add the following under [project]:")
        snippet = '''
[project.scripts]
'mcp-weather = "mcp_weather:main"')
'''
        prompter.snippet(snippet)


        prompter.instruct("\nThis modification will inform entry point to execute.", Fore.YELLOW + Style.BRIGHT)
        prompter.instruct("The mcp_weather is searched from ./src folder, and then mcp_weather > main ")

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
                current_data = _open(toml_path,"rb") 
                if not current_data:
                    continue
                
                # Check if the script entry exists
                if "project" in current_data and "scripts" in current_data["project"]:
                    scripts = current_data["project"]["scripts"]
                    if "mcp-weather" in scripts and scripts["mcp-weather"] == "mcp_weather:main":
                        prompter.success("Correct! You've successfully added the script entry.")
                        # Test the command
                        prompter.instruct("\nLet's test if the command works:")
                        try:
                            # subprocess.run(["cd","mcp-weather"])
                            # subprocess.run(["hatch", "run", "mcp-weather", "-help"])
                            result = subprocess.run(["hatch", "run", "mcp-weather", "-help"], 
                               cwd="mcp-weather",  # 작업 디렉토리 설정
                               check=True,
                               text=True,
                               capture_output=True)
                            print(result)
                        except subprocess.CalledProcessError as e:
                            print(e.stderr)
                            prompter.instruct("Oh! we added the entry point mcp_weather:main, but there isn't main func! "
                                "\nLet's modify it next tutorial")
                            return self.check()
                        finally:
                            pass
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
        return self.check()
