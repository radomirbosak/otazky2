class ExitIntent:
    def action(self, brain):
        brain.think("Exiting")
        brain.dead = True


class NoIntent:
    def action(self, brain):
        brain.think("Doing nothing.")


class CorrectionIntent:
    """User: Last decision was bad"""


class CleanSlateIntent:
    """User: I will ignore the last question, do not expect anything"""
