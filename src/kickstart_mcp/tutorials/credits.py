from typing import Optional
from ..tutorial_base import TutorialBase
from ..utils import Prompt
import time
import random

class Credits(TutorialBase):
    def __init__(self):
        super().__init__(
            name="Credits",
            description="A little thank you note from the developers"
        )
        self.current_step = 1
        self.total_steps = 1

    def check(self) -> bool:
        return self.current_step > self.total_steps

    def show_ascii_art(self):
        self.prompter.snippet('''
 ██╗  ██╗██╗ ██████╗██╗  ██╗███████╗████████╗ █████╗ ██████╗ ████████╗
 ██║ ██╔╝██║██╔════╝██║ ██╔╝██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝
 █████╔╝ ██║██║     █████╔╝ ███████╗   ██║   ███████║██████╔╝   ██║
 ██╔═██╗ ██║██║     ██╔═██╗ ╚════██║   ██║   ██╔══██║██╔══██╗   ██║
 ██║  ██╗██║╚██████╗██║  ██╗███████║   ██║   ██║  ██║██║  ██║   ██║
 ╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝

███╗   ███╗ ██████╗██████╗
████╗ ████║██╔════╝██╔══██╗
██╔████╔██║██║     ██████╔╝
██║╚██╔╝██║██║     ██╔═══╝
██║ ╚═╝ ██║╚██████╗██║
╚═╝     ╚═╝ ╚═════╝╚═╝
''', language=None, copy=False)

    def show_star_message(self):
        messages = [
            "credits.star_message.1",
            "credits.star_message.2",
            "credits.star_message.3",
            "credits.star_message.4",
            "credits.star_message.5"
        ]
        self.prompter.instruct_with_key(random.choice(messages))
        self.prompter.instruct("https://github.com/nolleh/kickstart-mcp")

    def show_easter_egg(self):
        keys = []
        self.prompter.instruct_with_key("credits.easter_egg.prompt")

        while len(keys) < 10:
            key = self.prompter.get_key()
            if key in ['↑', '↓', '←', '→', 'b', 'a']:
                keys.append(key)
                if len(keys) >= 10 and keys == ['↑','↑','↓','↓','←','→','←','→','b','a']:
                    self.prompter.clear()
                    self.prompter.snippet('''
   ___________________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
  |                  ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
  |    KONAMI       ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
  |      CODE       ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
  |    MASTER!      ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
  |                  ¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
   -------------------¶¶¶¶¶¶¶¶¶¶¶¶¶
''', language=None, copy=False)
                    self.prompter.success_with_key("credits.easter_egg.success")
                    time.sleep(2)
                    return
            else:
                return

    def run_step(self, step_id: int) -> bool:
        if step_id == 1:
            self.prompter.clear()

            # Show the main ASCII art
            self.show_ascii_art()

            # Add some spacing
            print("\n")

            # Show a fun thank you message
            self.prompter.instruct_with_key("credits.thank_you.1")
            self.prompter.instruct_with_key("credits.thank_you.2")

            print("\n")

            # Show the star request with a random message
            self.show_star_message()

            print("\n")

            # Add the easter egg
            self.show_easter_egg()

            return True
        return False

    def run(self) -> bool:
        while self.current_step <= self.total_steps:
            if not self.run_step(self.current_step):
                return False
            self.current_step += 1
        return True
