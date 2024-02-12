from termcolor import cprint

from .modules import ExitActor, HardMapInterpreter
from .modules.brain_multiple_functions_actor import BrainMFunctionActor


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

    actionable_modules = []
    for module in brain.modules:
        if module.can_act(intent):
            actionable_modules.append(module)

    if not actionable_modules:
        brain.say(f"Sorry, I don't know how to act on intent {intent}")
        return

    if len(actionable_modules) >= 2:
        brain.think(
            "Two or more modules can act on this intent. I will pick the first one."
        )

    winner_module = actionable_modules[0]
    winner_module.act(intent)


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
        self.known_functions = []
        self.interpret = interpret
        self.act = act
        self.modules = []

        # interpreters
        self.hardmap_intepreter = HardMapInterpreter(self)
        self.exit_actor = ExitActor(self)
        self.mfunc = BrainMFunctionActor(self)
        self.mfunc.add(list_modules, fname="list_modules")
        self.mfunc.add(list_hardcoded_intents, fname="list_commands")

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


def list_modules(brain):
    module_names = (str(module) for module in brain.modules)
    reply = "Brain modules are: " + ", ".join(module_names)
    brain.say(reply)


def list_hardcoded_intents(brain):
    hardcoded_intents = brain.mem["last_message_intent_hardmap"].items()
    # reply = ", ".join(f"{intent} activated by {command}" for command, intent in hardcoded_intents)
    # brain.say(reply)
    brain.say("These are the hardcoded commands that I know:")
    for command, intent in hardcoded_intents:
        brain.say(f"'{command}' which triggers the intent '{intent}'")
