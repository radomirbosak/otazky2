from .base import Module


class ExitActor(Module):
    def can_act(self, intent):
        return intent == "Exit"

    def act(self, intent):
        if not self.can_act(intent):
            return
        self.brain.think("Exiting")
        self.brain.dead = True
