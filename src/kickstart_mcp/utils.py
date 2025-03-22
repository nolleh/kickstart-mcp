from colorama import init, Fore, Style

class Prompt:
    def box(self, message: str):
        box_width = 40
        box_top = Fore.CYAN + Style.BRIGHT + "╔" + "═" * box_width + "╗"
        box_bottom = Fore.CYAN + Style.BRIGHT + "╚" + "═" * box_width + "╝"
        box_side = Fore.CYAN + Style.BRIGHT + "║"

        # Center the welcome message
        message = "Welcome to the kickstart-mcp."
        centered_message = message.center(box_width)

        # Print the welcome message in a box
        print(box_top)
        print(box_side + " " * box_width + box_side)
        print(box_side + centered_message + box_side)
        print(box_side + " " * box_width + box_side)
        print(box_bottom)

    def instruct(self, message: str):
        print(Fore.YELLOW + Style.BRIGHT + message)

    def read(self, message: str):
        return input(Fore.GREEN + message).strip()

    def error(self, message: str):
        print(Fore.RED + message)
    def success(self, message: str):
        print(Fore.GREEN + message)
