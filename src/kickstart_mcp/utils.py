from io import text_encoding
from colorama import init, Fore, Style
import os

class Theme:
    def __init__(self):
        
        # Colors
        self.title_color = Fore.CYAN + Style.BRIGHT
        self.text_color = Fore.WHITE + Style.NORMAL
        self.text_color_bright = Fore.WHITE + Style.BRIGHT
        self.intense_text = Fore.MAGENTA
        self.selected_color = Fore.YELLOW + Style.BRIGHT
        self.completed_color = Fore.GREEN
        self.progress_color = Fore.BLUE
        self.warning_color = Fore.YELLOW
        self.error_color = Fore.RED
        self.success_color = Fore.GREEN
        self.reset = Style.RESET_ALL

class Prompt:
    def __init__(self):
        # Initialize colorama with explicit settings
        init()
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

    def instruct(self, text: str, color: str = Fore.WHITE):
        """Display instruction text"""
        print(color + text + self.theme.reset)
    def intense_instruct(self, text: str):
        """Display intense instruction text"""
        print(self.theme.intense_text + text + self.theme.reset)

    def warn(self, text: str):
        """Display warning text"""
        print(self.theme.warning_color + text + self.theme.reset)
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
        status_color = self.theme.completed_color if status == "✓ " else (
            self.theme.text_color_bright if is_selected else self.theme.text_color)
        return (f"{color}{cursor} {status_color}{status}{name}{self.theme.reset}\n"
                f"     {self.theme.text_color}{description}{self.theme.reset}")

    def format_progress(self, label: str, progress: float) -> str:
        """Format progress with a progress bar"""
        bar_width = 20
        filled = int(bar_width * progress)
        bar = "█" * filled + "░" * (bar_width - filled)
        return f"{self.theme.progress_color}{label}: [{bar}] {progress:.1%}{self.theme.reset}"
