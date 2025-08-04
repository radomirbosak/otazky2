#!/usr/bin/env python3


from otazky.brain import Brain, Environment
from otazky.smodules.hardmap_interpreter import add_basic_hardmap_data


def main():
    env = Environment()
    brain = Brain(env)
    add_basic_hardmap_data(brain)

    while not brain.dead:
        prompt = input("> ")
        brain.mem["last_message"] = prompt
        brain.react()


if __name__ == "__main__":
    main()
