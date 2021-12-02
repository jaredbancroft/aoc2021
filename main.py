"""
Advent of Code 2021
"""

import argparse
import importlib


def main(args):
    """
    Main function
    """
    part1 = importlib.import_module(f"days.{args.day}.part1")
    part2 = importlib.import_module(f"days.{args.day}.part2")
    print(part1.solution(args.day))
    print(part2.solution(args.day))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code 2021")
    parser.add_argument("day")
    args = parser.parse_args()
    main(args)
