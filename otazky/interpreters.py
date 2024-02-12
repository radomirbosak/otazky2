from .modules import Module


class Interpreter:
    def __init__(self, brain):
        brain.interpreters.append(self)


class HardMapInterpreter(Module):
    def init_module(self):
        self.brain.mem["last_message_intent_hardmap"] = {
            "bad": "Correction",
            "btw": "CleanSlate",
            "exit": "Exit",
        }

    def interpret(self):
        hardmap = self.brain.mem.get("last_message_intent_hardmap")
        if hardmap is not None:
            if self.brain.last_message in hardmap:
                self.brain.think("Found intent in mem['last_message_intent_hardmap']")
                return hardmap[self.brain.last_message]
        return None

    def __eq__(self, other):
        return self.__class__ == other.__class__


class ExitActor(Module):
    def can_act(self, intent):
        return intent == "Exit"

    def act(self, intent):
        if not self.can_act(intent):
            return
        self.brain.think("Exiting")
        self.brain.dead = True
