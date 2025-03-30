from io import text_encoding
from colorama import init, Fore, Style
import os
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter
import sys
import tty
import termios
import pyperclip


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
        self.move_cursor = "\033[H"  # Move cursor to top-left
        self.hide_cursor = "\033[?25l"  # Hide cursor
        self.show_cursor = "\033[?25h"  # Show cursor
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

    def snippet(self, text: str, language: str | None = "python", copy: bool = True):
        """Display code snippet with syntax highlighting"""
        try:
            if language is not None:
                # Get the lexer for the specified language
                lexer = get_lexer_by_name(language)

                # Highlight the code
                highlighted_text = highlight(text, lexer, TerminalFormatter())

                # Split the highlighted code into lines
                lines = highlighted_text.rstrip().split("\n")
            else:
                lines = text.rstrip().split("\n")

            # Find the longest line length (excluding ANSI codes)
            def strip_ansi(s):
                import unicodedata

                result = ""
                i = 0
                while i < len(s):
                    if s[i] == "\033":
                        while i < len(s) and s[i] not in "m":
                            i += 1
                        i += 1  # skip 'm'
                    else:
                        char = s[i]
                        # Calculate the display width of the character
                        # East Asian width characters and emojis typically have width 2
                        width = (
                            2
                            if unicodedata.east_asian_width(char) in ("F", "W")
                            or ord(char) > 0x1F000
                            else 1
                        )
                        result += " " * width
                        i += 1
                return result

            # Calculate max width based on visible characters
            max_line_length = max(len(strip_ansi(line)) for line in lines)

            # Calculate box width
            box_width = max_line_length + 4

            # Create box parts
            top_line = (
                self.theme.box_top_left
                + self.theme.box_horizontal * (box_width - 2)
                + self.theme.box_top_right
            )
            bottom_line = (
                self.theme.box_bottom_left
                + self.theme.box_horizontal * (box_width - 2)
                + self.theme.box_bottom_right
            )

            # Print the box top
            print(self.theme.title_color + top_line + self.theme.reset)

            # Print each line of code with proper indentation
            for line in lines:
                visible_length = len(strip_ansi(line))
                padding = box_width - visible_length - 2
                print(
                    f"{self.theme.box_vertical} {line}{' ' * (padding - 1)}{self.theme.box_vertical}"
                )

            # Print the box bottom
            print(self.theme.title_color + bottom_line + self.theme.reset)

            # Add copy option
            if copy:
                print(
                    f"\n{self.theme.text_color}➤ Press 'c' to copy code to clipboard, or any other key to continue...{self.theme.reset}"
                )
                key = self.get_key()
                if key == "c":  # Enter key
                    pyperclip.copy(text)
                    print(
                        f"{self.theme.success_color}Code copied to clipboard!{self.theme.reset}"
                    )

        except Exception as e:
            # Fallback to non-highlighted version if highlighting fails
            print(f"Warning: Syntax highlighting failed: {e}")
            # self.snippet(text, language=None)

    def format_tutorial_item(
        self,
        cursor: str,
        status: str,
        name: str,
        description: str,
        is_selected: bool = False,
    ) -> str:
        """Format a tutorial item with proper colors and styling"""
        color = self.theme.selected_color if is_selected else self.theme.text_color
        status_color = (
            self.theme.completed_color
            if status == "✓ "
            else (
                self.theme.text_color_bright if is_selected else self.theme.text_color
            )
        )
        return (
            f"{color}{cursor} {status_color}{status}{name}{self.theme.reset}\n"
            f"     {self.theme.text_color}{description}{self.theme.reset}"
        )

    def format_progress(self, label: str, progress: float) -> str:
        """Format progress with a progress bar"""
        bar_width = 20
        filled = int(bar_width * progress)
        bar = "█" * filled + "░" * (bar_width - filled)
        return f"{self.theme.progress_color}{label}: [{bar}] {progress:.1%}{self.theme.reset}"

    def get_key(self):
        """Get a single keypress from the user"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == "\x03":  # Ctrl+C
                raise KeyboardInterrupt
            elif ch == "\x1b":  # ESC
                # Read the next two characters for special keys
                next_ch = sys.stdin.read(2)
                if next_ch == "[A":  # Up arrow
                    return "↑"
                elif next_ch == "[B":  # Down arrow
                    return "↓"
                elif next_ch == "[C":  # Right arrow
                    return "→"
                elif next_ch == "[D":  # Left arrow
                    return "←"
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
