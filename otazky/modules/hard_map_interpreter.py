from .base import Module


class HardMapInterpreter(Module):
    def init_module(self):
        self.add("bad", "Correction")
        self.add("btw", "CleanSlate")
        self.add("exit", "Exit")

    def interpret(self):
        hardmap = self.brain.mem.get("last_message_intent_hardmap")
        if hardmap is not None:
            if self.brain.last_message in hardmap:
                self.brain.think("Found intent in mem['last_message_intent_hardmap']")
                return hardmap[self.brain.last_message]
        return None

    def add(self, last_message, intent):
        hardmap = self.brain.mem.setdefault("last_message_intent_hardmap", {})
        hardmap[last_message] = intent

    def __eq__(self, other):
        return self.__class__ == other.__class__

    def __hash__(self):
        return hash(self.__class__)
