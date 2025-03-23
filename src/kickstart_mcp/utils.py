from colorama import init, Fore, Style

class Prompt:
    def __init__(self):
        self.clear_screen = "\033[2J"  # Clear screen
        self.move_cursor = "\033[H"    # Move cursor to top-left
        self.hide_cursor = "\033[?25l" # Hide cursor
        self.show_cursor = "\033[?25h" # Show cursor

    def clear(self):
        """Clear the screen and move cursor to top"""
        print(self.clear_screen + self.move_cursor, end="", flush=True)

    def box(self, text: str):
        """Display text in a box"""
        width = len(text) + 4
        print("+" + "-" * (width - 2) + "+")
        print(f"| {text} |")
        print("+" + "-" * (width - 2) + "+")

    def instruct(self, text: str):
        """Display instruction text"""
        print(text)

    def error(self, text: str):
        """Display error text"""
        print(f"\033[91m{text}\033[0m")  # Red color

    def success(self, text: str):
        """Display success text"""
        print(f"\033[92m{text}\033[0m")  # Green color

    def read(self, prompt: str) -> str:
        """Read input from user"""
        return input(prompt)
