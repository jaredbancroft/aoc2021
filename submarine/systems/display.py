from __future__ import annotations
from dataclasses import dataclass
from os import supports_follow_symlinks
from typing import List


class SevenSegmentDisplay:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.patterns, self.outputs = self.parse_input()

    def parse_input(self) -> tuple[List, List]:
        patterns = []
        outputs = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                input_line = line.rstrip().split(" | ")
                pattern = input_line[0].split(" ")
                output = input_line[1].split(" ")
                patterns.append(pattern)
                outputs.append(output)
            return patterns, outputs

    def analyze_output(self) -> int:
        easy_count = 0
        for output in self.outputs:
            for digit in output:
                if len(digit) in (2, 3, 4, 7):
                    easy_count += 1
        return easy_count

    # 'SevenSegmentDisplay.decode' is too complex (19) - no shit flake8
    def decode(self) -> int:  # noqa: C901
        sms = []
        for pattern in self.patterns:
            sm = SegmentMap()
            sorted_list = sorted(pattern, key=len)
            # solve top
            top = sorted(sorted_list[1])
            right_side = sorted(sorted_list[0])
            for wire in right_side:
                top.remove(wire)
            sm.top = top[0]
            # solve bottom left and bottom
            eight = sorted(sorted_list[9])
            four_plus_top = sorted(sorted_list[2])
            four_plus_top.append(sm.top)
            for wire in four_plus_top:
                eight.remove(wire)
            seven = sorted(sorted_list[1])
            four = sorted(sorted_list[2])
            for wire in seven:
                if wire in four:
                    four.remove(wire)
            sixes = [
                sorted(sorted_list[6]),
                sorted(sorted_list[7]),
                sorted(sorted_list[8]),
            ]
            nine = []
            for possible_nine in sixes:
                if (
                    eight[0] not in possible_nine
                    or eight[1] not in possible_nine
                ):
                    nine = possible_nine
                    sixes.remove(nine)
            if eight[0] not in nine:
                sm.bottom_left = eight[0]
                sm.bottom = eight[1]
            else:
                sm.bottom_left = eight[1]
                sm.bottom = eight[0]
            # solve middle
            zero = []
            six = []
            for possible_zero in sixes:
                if (
                    right_side[0] in possible_zero
                    and right_side[1] in possible_zero
                ):
                    zero = possible_zero
            sixes.remove(zero)
            six = sixes[0]
            for letter in ["a", "b", "c", "d", "e", "g", "f"]:
                if letter not in zero:
                    sm.middle = letter
            # solve the rest
            for letter in ["a", "b", "c", "d", "e", "g", "f"]:
                if letter not in [
                    sm.top,
                    sm.middle,
                    sm.bottom,
                    sm.bottom_left,
                    right_side[0],
                    right_side[1],
                ]:
                    sm.top_left = letter
            for letter in ["a", "b", "c", "d", "e", "g", "f"]:
                if letter not in six:
                    sm.top_right = letter
            for letter in ["a", "b", "c", "d", "e", "g", "f"]:
                if letter not in [
                    sm.top,
                    sm.bottom,
                    sm.middle,
                    sm.top_left,
                    sm.top_right,
                    sm.bottom_left,
                ]:
                    sm.bottom_right = letter
            sms.append(sm)
        i = 0
        total = 0
        for output in self.outputs:
            total += sms[i].calc_digits(output)
            i += 1

        return total


@dataclass
class SegmentMap:
    top: str = ""
    top_left: str = ""
    top_right: str = ""
    middle: str = ""
    bottom_left: str = ""
    bottom_right: str = ""
    bottom: str = ""

    def calc_digits(self, input: str) -> int:
        zero = (
            self.top
            + self.top_right
            + self.bottom_right
            + self.bottom
            + self.bottom_left
            + self.top_left
        )
        one = self.top_right + self.bottom_right
        two = (
            self.top
            + self.top_right
            + self.middle
            + self.bottom_left
            + self.bottom
        )
        three = (
            self.top
            + self.top_right
            + self.middle
            + self.bottom_right
            + self.bottom
        )
        four = self.top_left + self.middle + self.top_right + self.bottom_right
        five = (
            self.top
            + self.top_left
            + self.middle
            + self.bottom_right
            + self.bottom
        )
        six = five + self.bottom_left
        seven = one + self.top
        eight = zero + self.middle
        nine = seven + self.top_left + self.middle + self.bottom

        digits = [zero, one, two, three, four, five, six, seven, eight, nine]
        sorted_digits = []
        for digit in digits:
            sd = sorted(digit)
            sorted_digits.append("".join(sd))
        reading = []
        for wires in input:
            reading.append(sorted_digits.index("".join(sorted(wires))))

        str_reading = [str(x) for x in reading]
        return int("".join(str_reading))
