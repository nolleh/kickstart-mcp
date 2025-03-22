import os
import importlib
import inspect
from typing import List, Dict, Type
from .utils import Prompt

class Tutorial:
    def __init__(self, name: str, description: str, module: str):
        self.name = name
        self.description = description
        self.module = module

class Selector:
    def __init__(self):
        self.tutorials: List[Tutorial] = []
        self._load_tutorials()

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

    def _display_tutorials(self):
        """Display available tutorials with their descriptions"""
        prompter = Prompt()
        prompter.box("Available Tutorials")
        
        for i, tutorial in enumerate(self.tutorials, 1):
            prompter.instruct(f"{i}. {tutorial.name}")
            prompter.instruct(f"   {tutorial.description}")
        
        prompter.instruct("\nEnter the number of the tutorial you want to run (or 'q' to quit):")

    def select(self) -> bool:
        """Display tutorial selection menu and run selected tutorial"""
        if not self.tutorials:
            print("No tutorials available.")
            return False

        while True:
            self._display_tutorials()
            choice = input().strip().lower()
            
            if choice == 'q':
                return False
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(self.tutorials):
                    tutorial = self.tutorials[index]
                    self._run_tutorial(tutorial)
                    return True
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number or 'q' to quit.")

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

