#!/usr/bin/env python3


from .brain import Brain, Environment


def main():
    env = Environment()
    brain = Brain(env)

    while not brain.dead:
        prompt = input("> ")
        brain.last_message = prompt
        brain.react()


if __name__ == "__main__":
    main()
