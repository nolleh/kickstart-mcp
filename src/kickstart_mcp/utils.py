from colorama import init, Fore, Style
import time
import os

class Theme:
    def __init__(self):
        # Box characters (using ASCII characters)
        self.box_top_left = "+"
        self.box_top_right = "+"
        self.box_bottom_left = "+"
        self.box_bottom_right = "+"
        self.box_horizontal = "-"
        self.box_vertical = "|"
        
        # Colors
        self.title_color = Fore.CYAN + Style.BRIGHT
        self.text_color = Fore.WHITE
        self.selected_color = Fore.GREEN + Style.BRIGHT
        self.completed_color = Fore.YELLOW
        self.progress_color = Fore.BLUE
        self.error_color = Fore.RED
        self.success_color = Fore.GREEN
        self.reset = Style.RESET_ALL

class Prompt:
    def __init__(self):
        init()  # Initialize colorama
        self.theme = Theme()
        self.clear_screen = "\033[2J"  # Clear screen
        self.move_cursor = "\033[H"    # Move cursor to top-left
        self.hide_cursor = "\033[?25l" # Hide cursor
        self.show_cursor = "\033[?25h" # Show cursor
        self.terminal_width = os.get_terminal_size().columns

    def clear(self):
        """Clear the screen and move cursor to top"""
        print(self.clear_screen + self.move_cursor, end="", flush=True)

    def box(self, text: str):
        """Display text in a fancy box"""
        # Calculate box width (minimum 40 characters)
        box_width = 40
        box_top = Fore.CYAN + Style.BRIGHT + "╔" + "═" * box_width + "╗"
        box_bottom = Fore.CYAN + Style.BRIGHT + "╚" + "═" * box_width + "╝"
        box_side = Fore.CYAN + Style.BRIGHT + "║"

# Center the welcome message
        centered_message = text.center(box_width)

# Print the welcome message in a box
        print(box_top)
        print(box_side + " " * box_width + box_side)
        print(box_side + centered_message + box_side)
        print(box_side + " " * box_width + box_side)
        print(box_bottom)

    def instruct(self, text: str):
        """Display instruction text"""
        print(self.theme.text_color + text + self.theme.reset)

    def error(self, text: str):
        """Display error text"""
        print(self.theme.error_color + text + self.theme.reset)

    def success(self, text: str):
        """Display success text"""
        print(self.theme.success_color + text + self.theme.reset)

    def read(self, prompt: str) -> str:
        """Read input from user"""
        return input(self.theme.text_color + prompt + self.theme.reset).strip()

    def format_tutorial_item(self, cursor: str, status: str, name: str, description: str, is_selected: bool = False) -> str:
        """Format a tutorial item with proper colors and styling"""
        color = self.theme.selected_color if is_selected else self.theme.text_color
        status_color = self.theme.completed_color if status == "✓ " else self.theme.text_color
        return (f"{color}{cursor} {status_color}{status}{name}{self.theme.reset}\n"
                f"     {self.theme.text_color}{description}{self.theme.reset}")

    def format_progress(self, label: str, progress: float) -> str:
        """Format progress with a progress bar"""
        bar_width = 20
        filled = int(bar_width * progress)
        bar = "█" * filled + "░" * (bar_width - filled)
        return f"{self.theme.progress_color}{label}: [{bar}] {progress:.1%}{self.theme.reset}"
