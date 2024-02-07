#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
from enum import Enum, auto

from brain import Brain


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


def validate_scenario(scenario, brain):
    pass


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
