#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

from .brain import Brain, Environment


class ScenarioLineType(Enum):
    USER_PROMPT = auto()
    BRAIN_REPLY = auto()
    META_SIGN = auto()


@dataclass
class ScenarioLine:
    line: str
    type: ScenarioLineType

    @classmethod
    def from_str(cls, text):
        # > user prompt
        if text.startswith(">"):
            text = text.lstrip(">").lstrip()
            return cls(text, ScenarioLineType.USER_PROMPT)

        # [status_flag]
        if text.startswith("["):
            text = text.lstrip("[").rstrip("]")
            return cls(text, ScenarioLineType.META_SIGN)

        # bot reply
        return cls(text, ScenarioLineType.BRAIN_REPLY)


def load_scenario_file(scenario_file: Path) -> list[ScenarioLine]:
    return [
        ScenarioLine.from_str(line) for line in scenario_file.read_text().splitlines()
    ]


def validate_scenario_file(scenario_file, brain):
    scenario = load_scenario_file(scenario_file)
    validate_scenario(scenario, brain)


class ValidationError(Exception):
    pass


def validate_scenario(scenario: list[ScenarioLine], brain):
    said = []
    for scline in scenario:
        text = scline.line

        # is there are unconsumed brain texts, the next scenario line must be BRAIN_REPLY and must match
        if said:
            said_line = said.pop(0)
            if scline.type != ScenarioLineType.BRAIN_REPLY:
                raise ValidationError(f"Expecting brain reply {said_line}")
            if said_line != text:
                err_msg = f"Said line '{said_line}' does not match expected {text}"
                raise ValidationError(err_msg)
            continue  # brain reply matched, go to next line

        # all brain replies were consumed
        match scline.type:
            case ScenarioLineType.USER_PROMPT:
                brain.last_message = text
                brain.react()
                said = brain.env.said_lines.copy()

            case ScenarioLineType.BRAIN_REPLY:
                raise ValidationError("Expected lines, got none")

            case ScenarioLineType.META_SIGN:
                if text == "dead":
                    if not brain.dead:
                        raise ValidationError("Expecting [dead], not dead.")
            case _:
                assert False, "Unknown line type"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file", type=argparse.FileType("r"))
    return parser.parse_args()


def main():
    args = parse_args()

    env = Environment()
    bot = Brain(env)

    for line in args.prompt_file:
        line = line.rstrip("\n")
        print(">", line)
        bot.last_message = line
        bot.react()


if __name__ == "__main__":
    main()
