from .intents import CleanSlateIntent, CorrectionIntent, ExitIntent


class Interpreter:
    def __init__(self, brain):
        brain.interpreters.append(self)


class HardMapInterpreter(Interpreter):
    def __init__(self, brain):
        super().__init__(brain)
        self.brain = brain

    def init_brain(self):
        self.brain.mem["last_message_intent_hardmap"] = {
            "bad": CorrectionIntent(),
            "btw": CleanSlateIntent(),
            "exit": ExitIntent(),
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
