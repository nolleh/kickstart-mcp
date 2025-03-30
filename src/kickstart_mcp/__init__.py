# SPDX-FileCopyrightText: 2025-present nolleh <nolleh7707@gmail.com>
#
# SPDX-License-Identifier: MIT

import os
import json
from colorama import init, Fore, Style
import platform
from .config import Config
import logging

import click
from dotenv import load_dotenv
from .utils import Prompt

logger = logging.getLogger("kickstart-mcp")

def load_config(path):
    # Check if the directory exists, if not, create it
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Check if the file exists
    if not os.path.exists(path):
        # Create the file with default content
        default_content = {}  # You can define default content here
        with open(path, 'w') as file:
            json.dump(default_content, file, indent=4)
        print(Fore.YELLOW + f"Configuration file not found. Created a new one at {path} with default content.")
    # Load the configuration
    with open(path, 'r') as file:
        return json.load(file)

@click.command()
@click.option("-v", "--verbose", count=True, help="Enable verbose mode. Use -v for INFO, -vv for DEBUG")
@click.option("--env-file", type=click.Path(exists=True, dir_okay=False), help="Path to .env file")
@click.option("--mcp-config-file", type=click.Path(dir_okay=False), help="Path to MCP config file")
def main(
    verbose: bool,
    env_file: str | None, 
    mcp_config_file: str | None) -> None:

    logging_level = logging.INFO
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG  

    logging.basicConfig(level=logging_level)

    # Initialize colorama
    init(autoreset=True)
    # Define box characters
    box_width = 40
    box_top = Fore.CYAN + Style.BRIGHT + "╔" + "═" * box_width + "╗"
    box_bottom = Fore.CYAN + Style.BRIGHT + "╚" + "═" * box_width + "╝"
    box_side = Fore.CYAN + Style.BRIGHT + "║"
    #
    # Center the welcome message
    welcome_message = "Welcome to the kickstart-mcp."
    centered_message = welcome_message.center(box_width)
    #
    # # Print the welcome message in a box
    print(box_top)
    print(box_side + " " * box_width + box_side)
    print(box_side + centered_message + box_side)
    print(box_side + " " * box_width + box_side)
    print(box_bottom)

    # Print additional welcome message
    print(Fore.WHITE + "\nLearn Model Context Protocol (MCP) through interactive tutorials!")
    print(Fore.WHITE + "From setting up MCP hosts to building your own servers and clients,")
    print(Fore.WHITE + "we'll guide you through every step of your MCP journey.\n")
    print(Fore.YELLOW + "Have feedback? Visit: https://github.com/nolleh/kickstart-mcp\n")

    prompt = Prompt()
    prompt.instruct("➤ Press any key to continue")
    prompt.get_key()

    from .selector import Selector
    selector = Selector()
    selector.select()

if __name__ == "__main__":
    main()
