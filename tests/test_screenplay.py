from pathlib import Path
from unittest.mock import Mock

from pytest import fixture
from pytest import mark


from brain import Brain, Environment


@fixture
def brain():
    env = Environment()
    brain = Brain(env)
    return brain


@mark.parametrize("scenario", ["exit.test"])
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
            assert said != [], f"expected line {test_line}, nothing was said."
            said_line = said.pop()
            assert said_line == test_line, f"said line '{said_line}' does not match expected '{test_line}'"
