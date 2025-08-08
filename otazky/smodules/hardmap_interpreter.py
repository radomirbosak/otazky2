class SModule:
    def __init__(self, brain):
        self.brain = brain
        brain.smodules.append(self)
        self.mem = self.brain.mem
        self.memget = self.brain.mem.get

    def init(self):
        pass

    def setdone(self):
        self.mem["done"] = True

    @property
    def intent(self):
        return self.memget("intent")

    @intent.setter
    def intent(self, value):
        self.mem["intent"] = value

    @property
    def last_message(self):
        return self.memget("last_message")


class HardMapInterpreter(SModule):

    def init(self):
        self.mem.setdefault("hardmap", {})

    def __call__(self):
        """
        Take from last_message
        insert into intent
        """
        hardmap = self.memget("hardmap", {})
        if self.last_message in hardmap:
            self.intent = hardmap[self.last_message]


class ExitActor(SModule):

    def __call__(self):
        if self.intent == "Exit":
            self.brain.dead = True
            self.setdone()


def add_basic_hardmap_data(brain):
    hardmap = brain.mem["hardmap"]
    hardmap["bad"] = "Correction"
    hardmap["btw"] = "CleanSlate"
    hardmap["exit"] = "Exit"


class CallInterpreter(SModule):
    MAX_ARGS = 3

    def __call__(self):
        if self.last_message.startswith("call"):
            self.intent = "Call"

            call_parts = self.last_message.split()
            _, call_fn, *args = call_parts
            self.mem["call_fn"] = call_fn
            if len(args) > self.MAX_ARGS:
                raise RuntimeError("Calling function with more than 3 arguments is not supported")
            for idx, arg in enumerate(args, start=1):
                self.mem[f"arg{idx}"] = arg


class AdderActor(SModule):

    def __call__(self):
        if not (self.intent == "Call" and self.memget("call_fn") == "add"):
            return

        arg1 = self.memget("arg1")
        arg2 = self.memget("arg2")
        result = arg1 + arg2
        self.mem["result"] = result


class CallPrintActor(SModule):

    def __call__(self):
        result = self.memget("result")
        if self.intent == "Call" and result is not None:
            self.brain.say(f"Result is {result}")
            self.setdone()
