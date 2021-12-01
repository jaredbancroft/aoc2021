"""
Advent of Code 2021
"""

# TODO: Make a menu and handle multiple days


import argparse
import importlib


def main(args):
    """
    Main function
    """
    print(args.day)
    part1 = importlib.import_module(f"days.{args.day}.part1")
    part2 = importlib.import_module(f"days.{args.day}.part2")
    print(part1.solution())
    print(part2.solution())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2021")
    parser.add_argument("day")
    args = parser.parse_args()
    main(args)
