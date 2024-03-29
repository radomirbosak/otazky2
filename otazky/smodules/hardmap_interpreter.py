class SModule:
    def __init__(self, brain):
        self.brain = brain
        brain.smodules.append(self)

    def init(self):
        pass


class HardMapInterpreter(SModule):

    def init(self):
        self.brain.mem.setdefault("hardmap", {})

    def __call__(self):
        """
        Take from last_message
        insert into intent
        """
        mem = self.brain.mem
        hardmap = mem.get("hardmap", {})
        last_message = mem.get("last_message")
        # self.brain.think(f"last_message is {last_message}")
        # self.brain.think(f"hardmap is {hardmap}")
        if last_message in hardmap:
            mem["intent"] = hardmap[last_message]


class ExitActor(SModule):

    def __call__(self):
        mem = self.brain.mem
        if mem.get("intent") == "Exit":
            self.brain.dead = True
            mem["done"] = True


def add_basic_hardmap_data(brain):
    hardmap = brain.mem["hardmap"]
    hardmap["bad"] = "Correction"
    hardmap["btw"] = "CleanSlate"
    hardmap["exit"] = "Exit"
