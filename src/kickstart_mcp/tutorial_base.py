from abc import ABC, abstractmethod
from typing import Optional, Callable, Any
from .utils import Prompt
import subprocess
import os
import platform

class TutorialBase(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.prompter = Prompt()
        self._editor = None
        self._check_function = None
        self.editor = self._get_default_editor()

    @abstractmethod
    def run(self) -> bool:
        """Run the tutorial"""
        pass

    @abstractmethod
    def check(self) -> bool:
        """Check if the tutorial is completed successfully"""
        pass

    def set_check_function(self, check_func: Callable[[], bool]):
        """Set a custom check function for the tutorial"""
        self._check_function = check_func

    def select_editor(self) -> str:
        """Let user select their preferred editor"""
        editors = {
            '1': ('VS Code', 'code'),
            '2': ('Sublime Text', 'subl'),
            '3': ('Vim', 'vim'),
            '4': ('Nano', 'nano'),
            '5': ('Emacs', 'emacs')
        }
        
        while True:
            self.prompter.clear()
            self.prompter.box("Select Your Editor")
            self.prompter.instruct("\nAvailable editors:")
            for key, (name, _) in editors.items():
                self.prompter.instruct(f"{key}. {name}")
            
            choice = self.prompter.read("\nEnter your choice (1-5): ")
            if choice in editors:
                return editors[choice][1]
            self.prompter.error("Invalid choice. Please try again.")

    def open_editor(self, file_path: str, editor: Optional[str] = None) -> bool:
        """Open the specified file in the selected editor"""
        if not editor:
            editor = self._get_default_editor()
            if editor == "nano":
                self.prompter.warn("Unable to find out default editor")
                editor = self._editor or self.select_editor()
                self._editor = editor
        try:
            if editor == 'code':
                subprocess.run(['code', file_path], check=True)
            elif editor == 'subl':
                subprocess.run(['subl', file_path], check=True)
            else:
                subprocess.run([editor, file_path], check=True)
            return True
        except subprocess.CalledProcessError:
            self.prompter.error(f"Failed to open {editor}. Please make sure it's installed.")
            return False

    def handle_editor_options(self, file_path: str) -> bool:
        """Handle common editor options and return True if user wants to continue"""
        while True:
            # Get user input
            self.prompter.instruct("\nWould you like to:")
            self.prompter.instruct("1. Edit the file")
            self.prompter.instruct("2. Check if changes are correct")
            self.prompter.instruct("3. Change editor")
            self.prompter.instruct("4. Exit")
            # self.prompter.instruct("\n1. Open in editor")
            # self.prompter.instruct("2. Check changes")
            # self.prompter.instruct("3. Change editor")
            # self.prompter.instruct("4. Exit tutorial")
            
            choice = self.prompter.read("\nEnter your choice (1-4): ")
            
            if choice == '1':
                if not self.open_editor(file_path):
                    continue
            elif choice == '2':
                # Test the command
                self.prompter.instruct("\nLet's test if the command works:")
                if self._check_function:
                    if self._check_function():
                        self.prompter.success("Changes look good!")
                    else:
                        self.prompter.error("Changes are not correct. Please try again.")
                else:
                    if self.check():
                        self.prompter.success("Changes look good!")
                    else:
                        self.prompter.error("Changes are not correct. Please try again.")
            elif choice == '3':
                self._editor = None
                if not self.open_editor(file_path):
                    continue
            elif choice == '4':
                return False
            
            # if self.prompter.read("\nContinue with tutorial? (y/n): ").lower() == 'y':
            #     return True
            return True

    def verify_file_exists(self, file_path: str) -> bool:
        """Verify if the file exists"""
        if not os.path.exists(file_path):
            self.prompter.error(f"File not found: {file_path}")
            return False
        return True 
    
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
