import os
import importlib
import inspect
import sys
import tty
import termios
import select
from typing import List, Dict, Type, Optional
from .utils import Prompt
from .state import TutorialState, TutorialGroup

class Tutorial:
    def __init__(self, name: str, description: str, module: str):
        self.name = name
        self.description = description
        self.module = module

class Selector:
    def __init__(self):
        self.tutorials: List[Tutorial] = []
        self.state = TutorialState()
        self.current_position = 0
        self.current_group = "basics"
        self.prompter = Prompt()
        self._load_tutorials()
        # Restore last position and group if exists
        last_pos = self.state.get_last_position()
        last_group = self.state.get_last_group()
        if last_pos is not None:
            self.current_position = last_pos
        if last_group is not None:
            self.current_group = last_group

    def _load_tutorials(self):
        """Load all tutorial modules from the tutorials directory"""
        tutorials_dir = os.path.join(os.path.dirname(__file__), "tutorials")
        
        # Get all Python files in the tutorials directory
        tutorial_files = [f for f in os.listdir(tutorials_dir) 
                         if f.endswith('.py') and not f.startswith('__')]
        
        # Sort files to ensure consistent order
        tutorial_files.sort()
        
        for file in tutorial_files:
            # Import the module
            module_name = f"kickstart_mcp.tutorials.{file[:-3]}"
            try:
                module = importlib.import_module(module_name)
                
                # Find the tutorial class in the module
                for name, obj in inspect.getmembers(module):
                    if (inspect.isclass(obj) and 
                        name not in ['Tutorial', 'Selector'] and 
                        hasattr(obj, 'main')):
                        
                        # Get description from docstring or use default
                        description = getattr(obj, '__doc__', '') or f"Tutorial {name}"
                        
                        self.tutorials.append(Tutorial(
                            name=name,
                            description=description,
                            module=module_name
                        ))
                        break
            except Exception as e:
                print(f"Error loading tutorial from {file}: {e}")

    def _get_key(self):
        """Get a single keypress from the user"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x03':  # Ctrl+C
                raise KeyboardInterrupt
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def _display_progress(self):
        """Display overall progress and group progress"""
        total_progress = self.state.get_total_progress()
        self.prompter.instruct(f"\nOverall Progress: {total_progress:.1%}")
        
        if self.current_group:
            group_progress = self.state.get_group_progress(self.current_group)
            group_name = self.state.groups[self.current_group].name
            self.prompter.instruct(f"{group_name} Progress: {group_progress:.1%}")

    def _display_tutorials(self):
        """Display available tutorials with their descriptions"""
        # Clear screen and move cursor to top
        self.prompter.clear()
        
        self.prompter.box("Available Tutorials")
        
        # Display groups
        for group_name, group in self.state.groups.items():
            # Add group header with progress
            progress = self.state.get_group_progress(group_name)
            cursor = ">" if group_name == self.current_group else " "
            self.prompter.instruct(f"\n{cursor} {group.name} ({progress:.1%})")
            self.prompter.instruct(f"   {group.description}")
            
            # Display tutorials in this group
            if group_name == self.current_group:
                for i, tutorial_name in enumerate(group.tutorials):
                    tutorial = next((t for t in self.tutorials if t.name == tutorial_name), None)
                    if tutorial:
                        status = "✓ " if self.state.is_tutorial_completed(tutorial.name) else "  "
                        cursor = ">" if i == self.current_position else " "
                        self.prompter.instruct(f"  {cursor} {status}{tutorial.name}")
                        self.prompter.instruct(f"     {tutorial.description}")
        
        self.prompter.instruct("\nUse ↑↓ to navigate, Enter to select, 'q' to quit")
        self._display_progress()

    def select(self) -> bool:
        """Display tutorial selection menu and run selected tutorial"""
        if not self.tutorials:
            print("No tutorials available.")
            return False

        # Hide cursor at the start
        print(self.prompter.hide_cursor, end="", flush=True)

        try:
            while True:
                self._display_tutorials()
                
                # Get keypress
                key = self._get_key()
                
                if key == 'q':
                    return False
                elif key == '\r':  # Enter key
                    if self.current_group:
                        group = self.state.groups[self.current_group]
                        if 0 <= self.current_position < len(group.tutorials):
                            tutorial_name = group.tutorials[self.current_position]
                            tutorial = next((t for t in self.tutorials if t.name == tutorial_name), None)
                            if tutorial:
                                self.state.set_current_tutorial(tutorial.name)
                                self._run_tutorial(tutorial)
                                self.state.mark_tutorial_completed(tutorial.name)
                                return True
                elif key == '\x1b':  # Escape sequence
                    next_key = self._get_key()
                    if next_key == '[':
                        direction = self._get_key()
                        if direction == 'A':  # Up arrow
                            if self.current_group:
                                group = self.state.groups[self.current_group]
                                self.current_position = (self.current_position - 1) % len(group.tutorials)
                        elif direction == 'B':  # Down arrow
                            if self.current_group:
                                group = self.state.groups[self.current_group]
                                self.current_position = (self.current_position + 1) % len(group.tutorials)
                        elif direction == 'C':  # Right arrow
                            # Move to next group
                            group_names = list(self.state.groups.keys())
                            if self.current_group:
                                current_idx = group_names.index(self.current_group)
                                self.current_group = group_names[(current_idx + 1) % len(group_names)]
                                self.current_position = 0
                            else:
                                self.current_group = group_names[0]
                        elif direction == 'D':  # Left arrow
                            # Move to previous group
                            group_names = list(self.state.groups.keys())
                            if self.current_group:
                                current_idx = group_names.index(self.current_group)
                                self.current_group = group_names[(current_idx - 1) % len(group_names)]
                                self.current_position = 0
                            else:
                                self.current_group = group_names[-1]
                
                # Save current position and group
                self.state.set_last_position(self.current_position)
                if self.current_group:
                    self.state.set_last_group(self.current_group)
        finally:
            # Show cursor when exiting
            print(self.prompter.show_cursor, end="", flush=True)

    def _run_tutorial(self, tutorial: Tutorial):
        """Run the selected tutorial"""
        try:
            # Import the module
            module = importlib.import_module(tutorial.module)
            
            # Find and instantiate the tutorial class
            for name, obj in inspect.getmembers(module):
                if (inspect.isclass(obj) and 
                    name == tutorial.name and 
                    hasattr(obj, 'main')):
                    
                    # Create instance and run main method
                    instance = obj(name=tutorial.name)
                    instance.main()
                    break
        except Exception as e:
            print(f"Error running tutorial {tutorial.name}: {e}")

