from termcolor import cprint

# from .modules import ExitActor, HardMapInterpreter
# from .modules.brain_function_actor import BrainFunctionActor
from .smodules.hardmap_interpreter import (
    AdderActor,
    CallInterpreter,
    ExitActor,
    HardMapInterpreter,
)


def interpret(brain):
    """Meta-interpreting function"""
    # 1. last message-intent hardmap
    for module in brain.modules:
        intent = module.interpret()
        if intent is not None:
            return intent

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

    if len(actionable_modules) >= 2:  # noqa: PLR2004
        brain.think("Two or more modules can act on this intent. I will pick the first one.")

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

    def think(self, text):  # noqa: PLR6301
        cprint(f"({text})", "dark_grey")


class Brain:
    def __init__(self, env):
        self.env = env
        self.dead = False
        self.mem = {"last_message": None}
        # self.last_message = None
        self.known_functions = []
        self.interpret = interpret
        self.act = act
        self.modules = []
        self.smodules = []

        # interpreters
        self.hardmap_intepreter = HardMapInterpreter(self)
        self.call_interpreter = CallInterpreter(self)
        self.exit_actor = ExitActor(self)
        self.adder_actor = AdderActor(self)
        # self.mfunc = BrainFunctionActor(self)
        # self.mfunc.add(list_modules, fname="list_modules")
        # self.mfunc.add(list_hardcoded_intents, fname="list_commands")
        # self.hardmap_intepreter.add("help", ("ExecuteBrainFunction", "list_commands"))

        self.init_modules()

    def init_modules(self):
        for interpreter in self.modules:
            interpreter.init_module()
        for smodule in self.smodules:
            smodule.init()

    def react(self):
        # reset stop condition for smodule activation
        self.mem["done"] = False
        iterations = 0
        max_iterations = 2
        while not self.mem["done"]:
            if iterations >= max_iterations:
                self.think(f"Not done after {max_iterations} iterations")
                break
            for smodule in self.smodules:
                smodule()
            iterations += 1

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
    brain.say("These are the hardcoded commands that I know:")
    for command, intent in hardcoded_intents:
        brain.say(f"'{command}' which triggers the intent '{intent}'")
