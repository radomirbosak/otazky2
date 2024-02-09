from termcolor import cprint

from .intents import CleanSlateIntent, CorrectionIntent, ExitIntent, NoIntent
from .interpreters import HardMapInterpreter


def interpret(brain):
    """Meta-interpreting function"""
    # 1. last message-intent hardmap
    for module in brain.modules:
        intent = module.interpret()
        if intent is not None:
            return intent
    # intent = brain.hardmap_intepreter.interpret()
    # if intent is not None:
    #     return intent

    # 2. give up
    return None


def act(brain, intent):
    """Meta-acting function"""
    if intent is None:
        brain.say("Sorry, I was not able to understand your intent.")
        return

    if hasattr(intent, "action"):
        intent.action(brain)
        return

    brain.say(f"Sorry, I don't know how to act on intent {intent}")


class Environment:
    def __init__(self):
        self.said_lines = []

    def clear(self):
        self.said_lines = []

    def say(self, text):
        print(text)
        self.said_lines.append(text)

    def think(self, text):
        cprint(f"({text})", "dark_grey")


class Brain:
    def __init__(self, env):
        self.env = env
        self.dead = False
        self.mem = {}
        self.last_message = None
        self.known_intents = [
            ExitIntent(),
            NoIntent(),
            CorrectionIntent(),
            CleanSlateIntent(),
        ]
        self.known_functions = []
        self.interpret = interpret
        self.act = act
        self.modules = []

        # interpreters
        self.hardmap_intepreter = HardMapInterpreter(self)
        self.init_modules()

    def init_modules(self):
        for interpreter in self.modules:
            interpreter.init_module()

    def react(self):
        # find intent
        intent = self.interpret(self)
        self.think(f"The intent is {intent}")
        # respond to intent
        self.act(self, intent)

    def say(self, text):
        self.env.say(text)

    def think(self, text):
        self.env.think(text)
