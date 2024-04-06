from .base import Module


class BrainFunctionActor(Module):
    def __init__(self, brain):
        super().__init__(brain)
        if not hasattr(brain, "functions"):
            brain.functions = {}

    def add(self, fn, fname=None):
        fname = fname or fn.__name__
        self.brain.functions[fname] = fn
        intent = ("ExecuteBrainFunction", fname)
        self.brain.hardmap_intepreter.add(f"fn {fname}", intent)

    def can_act(self, intent):
        if not isinstance(intent, tuple):
            return False
        if len(intent) != 2:  # noqa: PLR2004
            return False
        match intent:
            case ("ExecuteBrainFunction", fname):
                return fname in self.brain.functions
        return False

    def act(self, intent):
        _, fname = intent
        self.brain.functions[fname](self.brain)
