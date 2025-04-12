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
from .i18n import i18n

logger = logging.getLogger("kickstart-mcp")


def load_config(path):
    # Check if the directory exists, if not, create it
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Check if the file exists
    if not os.path.exists(path):
        # Create the file with default content
        default_content = {}  # You can define default content here
        with open(path, "w") as file:
            json.dump(default_content, file, indent=4)
        print(
            Fore.YELLOW
            + f"Configuration file not found. Created a new one at {path} with default content."
        )
    # Load the configuration
    with open(path, "r") as file:
        return json.load(file)


@click.command()
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose mode. Use -v for INFO, -vv for DEBUG",
)
@click.option(
    "--env-file", type=click.Path(exists=True, dir_okay=False), help="Path to .env file"
)
@click.option(
    "--mcp-config-file", type=click.Path(dir_okay=False), help="Path to MCP config file"
)
@click.option("--lang", "-l", default="en", help="Language for the tutorial (en/ko)")
def main(
    verbose: bool, env_file: str | None, mcp_config_file: str | None, lang: str
) -> None:

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
    welcome_message = "Welcome to the kickstart-mcp"
    centered_message = welcome_message.center(box_width)
    #
    # # Print the welcome message in a box
    print(box_top)
    print(box_side + " " * box_width + box_side)
    print(box_side + centered_message + box_side)
    print(box_side + " " * box_width + box_side)
    print(box_bottom)

    # Print additional welcome message
    print(
        Fore.WHITE
        + "\nLearn Model Context Protocol (MCP) through interactive tutorials!"
    )
    print(
        Fore.WHITE
        + "From setting up MCP hosts to building your own servers and clients,"
    )
    print(Fore.WHITE + "we'll guide you through every step of your MCP journey.\n")
    print(
        Fore.YELLOW + "Have feedback? Visit: https://github.com/nolleh/kickstart-mcp\n"
    )

    prompt = Prompt()
    try:
        # Set the language in i18n
        i18n.set_language(lang)
    except ValueError:
        prompt.error(f"Not supported language: {lang}")

    prompt.instruct(
        "You can modify language by running the program with -l option. ex: -l ko"
    )
    prompt.instruct("➤ Press any key to continue")
    prompt.get_key()

    from .selector import Selector

    selector = Selector()
    selector.select()


__all__ = ["i18n"]

if __name__ == "__main__":
    main()
