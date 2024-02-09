class Module:
    def __init__(self, brain):
        self.brain = brain
        brain.modules.append(self)

    def init_module(self):
        """Post-init after all modules are registered in brain"""

    def interpret(self):
        """Convert brain state (e.g. last_prompt) into Intent"""

    def act(self, intent):
        """Execute intent"""
