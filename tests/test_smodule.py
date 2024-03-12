# import pytest

from otazky.brain import Brain, Environment
from otazky.smodules.hardmap_interpreter import HardMapInterpreter


def test_hardmap_interpreter():
    # create brain and env
    env = Environment()
    brain = Brain(env)

    # add and initialize modules
    hmi = HardMapInterpreter(brain)
    brain.init_modules()

    # prepare data
    brain.mem["hardmap"]["Ahoj"] = "pozdrav"

    # test
    assert brain.mem.get("output_HardMapInterpreter") is None
    brain.mem["last_message"] = "Ahoj"

    hmi()
    assert brain.mem["intent"] == "pozdrav"
