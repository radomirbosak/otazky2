#!/usr/bin/env python3

import argparse
from pathlib import Path

from otazky.brain import Brain, Environment
from otazky.scenario import validate_scenario_file


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file", type=Path)
    return parser.parse_args()


def main():
    args = parse_args()

    env = Environment()
    brain = Brain(env)

    validate_scenario_file(args.prompt_file, brain)


if __name__ == "__main__":
    main()
