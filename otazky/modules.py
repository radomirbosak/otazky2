class Module:
    def __init__(self, brain):
        self.brain = brain
        brain.modules.append(self)

    def init_module(self):
        """Post-init after all modules are registered in brain"""

    def interpret(self):
        """Convert brain state (e.g. last_prompt) into Intent"""

    def can_act(self, intent) -> bool:
        """Returns whether this module can act on this intent"""

    def act(self, intent):
        """Execute intent"""


class BrainFunctionActor(Module):
    def __init__(self, brain, fn, fname=None):
        super().__init__(brain)
        self.fn = fn
        self.fname = fname or fn.__name__

    def init_module(self):
        intent = ("ExecuteBrainFunction", self.fname)
        self.brain.hardmap_intepreter.add(f"/fn {self.fname}", intent)

    def can_act(self, intent):
        return intent == ("ExecuteBrainFunction", self.fname)

    def act(self, intent):
        self.fn(self.brain)
