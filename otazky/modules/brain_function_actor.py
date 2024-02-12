from .base import Module


class BrainFunctionActor(Module):
    def __init__(self, brain, fn, fname=None):
        super().__init__(brain)
        self.fn = fn
        self.fname = fname or fn.__name__

    def init_module(self):
        intent = ("ExecuteBrainFunction", self.fname)
        self.brain.hardmap_intepreter.add(f"fn {self.fname}", intent)

    def can_act(self, intent):
        return intent == ("ExecuteBrainFunction", self.fname)

    def act(self, intent):
        self.fn(self.brain)

    def __str__(self):
        return f"{self.__class__.__name__}({self.fname})"
