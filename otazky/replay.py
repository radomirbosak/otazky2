#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

from .brain import Brain


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
        match scline.type:
            case ScenarioLineType.USER_PROMPT:
                if said:
                    raise ValidationError("Expecting user prompt, got lines")
                brain.last_message = text
                brain.react()
                said = brain.env.said_lines.copy()

            case ScenarioLineType.BRAIN_REPLY:
                if not said:
                    raise ValidationError("Expected lines, got none")
                said_line = said.pop(0)
                if said_line != text:
                    err_msg = f"Said line '{said_line}' does not match expected {text}"
                    raise ValidationError(err_msg)

            case ScenarioLineType.META_SIGN:
                if text == "dead":
                    if said:
                        raise ValidationError("Expecting [dead], got lines")
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

    bot = Brain()

    for line in args.prompt_file:
        line = line.rstrip("\n")
        print(">", line)
        bot.last_message = line
        bot.react()


if __name__ == "__main__":
    main()
