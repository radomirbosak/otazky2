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


class CallInterpreter(SModule):

    def __call__(self):
        mem = self.brain.mem
        last_message = mem.get("last_message")
        if last_message.startswith("call"):
            mem["intent"] = "Call"

            call_parts = last_message.split()
            _, call_fn, *args = call_parts
            mem["call_fn"] = call_fn
            if len(args) > 3:
                raise RuntimeError("Calling function with more than 3 arguments is not supported")
            for idx, arg in enumerate(args, start=1):
                mem[f"arg{idx}"] = arg


class AdderActor(SModule):

    def __call__(self):
        mem = self.brain.mem
        intent = mem.get("intent")
        call_fn = mem.get("call_fn")
        if not (intent == "Call" and call_fn == "add"):
            return

        arg1 = mem.get("arg1")
        arg2 = mem.get("arg2")
        result = arg1 + arg2
        self.brain.say(f"Result is {result}")
        mem["done"] = True
