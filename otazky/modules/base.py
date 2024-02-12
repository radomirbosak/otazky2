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

    def __str__(self):
        return self.__class__.__name__
