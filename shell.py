#!/usr/bin/env python3


from otazky.brain import Brain, Environment


def main():
    env = Environment()
    brain = Brain(env)

    while not brain.dead:
        prompt = input("> ")
        brain.mem["last_message"] = prompt
        brain.react()


if __name__ == "__main__":
    main()
