from ..tutorial_base import TutorialBase
import os
import tomli
import tomli_w
import subprocess
from typing import Any


class ModifyToml(TutorialBase):
    def __init__(self):
        super().__init__(
            name="ModifyToml",
            description="Learn how to modify the pyproject.toml file",
        )
        self.project_dir = "mcp-weather"
        self.target_file = f"{self.project_dir}/src/mcp_weather/pyproject.toml"
        self.expected_content = {
            "project": {
                "name": "kickstart-mcp",
                "version": "0.1.0",
                "description": "A tutorial for learning MCP",
                "authors": [{"name": "Your Name", "email": "your.email@example.com"}],
                "dependencies": ["click", "colorama"],
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
        self.editor = self._get_default_editor()

    def _open_in_editor(self, file_path):
        """Open the file in the selected editor"""
        try:
            if self.editor in ["code", "subl"]:
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
                self.prompter.error(
                    "Project directory not found. Please complete the previous tutorial first."
                )
                return False

            toml_path = os.path.join(self.project_dir, "pyproject.toml")
            if not os.path.exists(toml_path):
                self.prompter.error(
                    "pyproject.toml not found. Please complete the previous tutorial first."
                )
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
            if (
                build_system.get("requires") != ["hatchling"]
                or build_system.get("build-backend") != "hatchling.build"
            ):
                return False

            # Check if scripts section exists and is correct
            if "scripts" not in project:
                return False

            scripts = project["scripts"]
            if (
                "mcp-weather" not in scripts
                or scripts["mcp-weather"] != "mcp_weather:main"
            ):
                return False

            return True

        except Exception:
            return False

    def run(self) -> bool:
        prompter = self.prompter
        prompter.box_with_key("modify_toml.title")

        # Check if project exists
        if not os.path.exists(self.project_dir):
            prompter.error_with_key("modify_toml.error.pyproject_not_found")
            return False

        toml_path = os.path.join(self.project_dir, "pyproject.toml")
        if not os.path.exists(toml_path):
            prompter.error_with_key("modify_toml.error.toml_not_found")
            return False

        def _open(toml_path, mode: str) -> dict[str, Any] | None:
            with open(toml_path, mode) as f:
                try:
                    toml_data = tomli.load(f)
                    return toml_data
                except tomli.TOMLDecodeError as e:
                    prompter.error_with_key("modify_toml.error.toml_decode")
                    return None

        # Read current toml content
        if not _open(toml_path, "rb"):
            return False

        prompter.instruct_with_key("modify_toml.update_python.instruction")
        prompter.instruct_with_key("modify_toml.update_python.modify")
        prompter.snippet('''requires-python = ">=3.10"''')

        prompter.instruct_with_key("modify_toml.script_entry.instruction")
        prompter.instruct_with_key("modify_toml.script_entry.add")
        snippet = '''[project.scripts]
'mcp-weather = "mcp_weather:main"'
'''
        prompter.snippet(snippet)
        prompter.instruct_with_key("modify_toml.script_entry.explanation")
        prompter.instruct_with_key("modify_toml.script_entry.detail")
        # prompter.instruct_with_key("modify_toml.current_content")

        return self.handle_editor_options(self.target_file)
