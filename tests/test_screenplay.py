# pylint: disable=redefined-outer-name
from pathlib import Path

from pytest import fixture, mark

from otazky.brain import Brain, Environment
from otazky.scenario import validate_scenario_file


@fixture
def brain():
    env = Environment()
    brain = Brain(env)
    return brain


SCENARIO_LIST = ["exit.sc", "cannot_understand.sc", "list_modules.sc"]


@mark.parametrize("scenario", SCENARIO_LIST)
def test_something(brain, scenario):
    filename = Path("tests/") / scenario

    lines = filename.read_text().splitlines()

    said = []

    for test_line in lines:
        if test_line == "[dead]":
            if said:
                assert False, f"unexpected line {said[0]}, brain should be [dead]"
            assert brain.dead
        elif test_line.startswith("> "):
            if said:
                assert False, f"unexpected line {said[0]}, about to prompt {test_line}."
            test_line = test_line[2:]
            brain.last_message = test_line
            brain.react()
            said = brain.env.said_lines.copy()
        else:
            assert said, f"expected line {test_line}, nothing was said."
            said_line = said.pop()
            err_msg = f"said line '{said_line}' does not match expected '{test_line}'"
            assert said_line == test_line, err_msg


def test_replay(brain):
    filename = Path("tests/") / "exit.sc"
    validate_scenario_file(filename, brain)
