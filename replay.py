#!/usr/bin/env python3

import argparse

from brain import Brain


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
