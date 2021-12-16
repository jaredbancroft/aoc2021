from __future__ import annotations


BIG = 9223372036854775807


class Origami:
    def __init__(self, filename) -> None:
        self.coords: dict[tuple[int, int], str] = {}
        self.instructions: list[str] = []
        self.x: int = BIG
        self.y: int = BIG
        self.y_list: list[int]
        self._parse_input_file(filename)

    def run(self, only_once=False) -> int:
        if only_once:
            i = self._parse_instruction(self.instructions[0])
            self._make_fold(i)
            return len(self.coords)
        else:
            for instruction in self.instructions:
                i = self._parse_instruction(instruction)
                self._make_fold(i)
            return 0

    def print(self) -> None:
        for j in range(0, self.y * 2 + 1):
            for i in range(0, self.x * 2 + 1):
                if (i, j) in self.coords:
                    print("#", end="")
                else:
                    print(".", end="")
            print("")

    def _parse_input_file(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()

        i = lines.index("\n")
        raw_coords = lines[0:i]
        raw_instructions = lines[i + 1 :]
        coords_list: list[tuple[int, int]] = [
            (int(x[0]), int(x[1]))
            for x in [(x.rstrip()).split(",") for x in raw_coords]
        ]
        coords: dict[tuple[int, int], str] = {}
        for coord in coords_list:
            coords[coord] = "#"
        instructions = [(x.rstrip()).split(" ")[2] for x in raw_instructions]
        self.coords = coords
        self.instructions = instructions

    def _make_fold(self, instruction: tuple[str, int]) -> None:
        direction: str = instruction[0]
        value: int = instruction[1]
        if direction == "y":
            self._fold_up(value)
        else:
            self._fold_left(value)

    def _fold_up(self, y_value: int) -> None:
        if y_value < BIG:
            self.y = y_value
        tmp_coords = self.coords.copy()
        for key in tmp_coords.keys():
            if key[1] > y_value:
                new_key = (key[0], 2 * y_value - key[1])
                del self.coords[key]
                self.coords[new_key] = "#"

    def _fold_left(self, x_value: int) -> None:
        if x_value < BIG:
            self.x = x_value
        tmp_coords = self.coords.copy()
        for key in tmp_coords.keys():
            if key[0] > x_value:
                new_key = (2 * x_value - key[0], key[1])
                del self.coords[key]
                self.coords[new_key] = "#"

    def _parse_instruction(self, instruction: str) -> tuple[str, int]:
        parsed: list[str] = instruction.split("=")
        return (parsed[0], int(parsed[1]))
