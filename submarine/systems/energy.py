from __future__ import annotations
from os import system, name
from typing import Optional


X_MAX: int = 10
Y_MAX: int = 10


class RemoteEnergyDetector:
    def __init__(self, filename) -> None:
        self.octopuses: dict[
            tuple[int, int], Octopus
        ] = self._init_energy_detector(filename)
        self.round: int = 0
        self.flashes: int = 0
        self.synchronize: int = 0

    def _init_energy_detector(
        self, filename: str
    ) -> dict[tuple[int, int], Octopus]:
        octopuses: dict[tuple[int, int], Octopus] = {}
        with open(filename, "r", encoding="utf-8") as f:
            for j in range(0, Y_MAX):
                line: str = f.readline().rstrip()
                for i in range(0, X_MAX):
                    energy: int = int(line[i])
                    position = (i, j)
                    octopus = Octopus(energy, position)
                    octopuses[position] = octopus
        return octopuses

    def run(self, rounds: int) -> int:
        while self.round != rounds:
            self.next_round()
            self.print_energy_grid()
        return self.flashes

    def run_sync(self) -> int:
        while self.synchronize == 0:
            self.next_round()
        return self.synchronize

    def print_energy_grid(self) -> None:
        self.clear()
        for j in range(0, Y_MAX):
            for i in range(0, X_MAX):
                energy_level: int = self.octopuses[(i, j)].energy_level
                if energy_level == 0:
                    print(f"\033[1m\033[93m{energy_level}\033[0m", end=" ")
                else:
                    print(energy_level, end=" ")
            print("")

    def next_round(self) -> None:
        self.round += 1
        self._increase_all_energy_levels()
        flashers: list[Octopus] = self._determine_flashers()
        neighbors: list[tuple[int, int]] = []
        for flasher in flashers:
            tmp: list[tuple[int, int]] = flasher.flash()
            for t in tmp:
                neighbors.append(t)
        while len(neighbors) > 0:
            for neighbor in neighbors:
                self._increase_energy_level(neighbor)
                new_flashers: list[Octopus] = self._determine_flashers()
                flashers.extend(new_flashers)
                for new_flasher in new_flashers:
                    tmp = new_flasher.flash()
                    for t in tmp:
                        neighbors.append(t)
                neighbors.remove(neighbor)
        self.flashes += len(flashers)
        self._reset()
        if self._check_all_zeros():
            self.synchronize = self.round

    def _reset(self) -> None:
        for j in range(0, Y_MAX):
            for i in range(0, X_MAX):
                self.octopuses[(i, j)].reset()

    def _check_all_zeros(self) -> bool:
        for j in range(0, Y_MAX):
            for i in range(0, X_MAX):
                if self.octopuses[(i, j)].energy_level != 0:
                    return False
        return True

    def _increase_all_energy_levels(self) -> None:
        for j in range(0, Y_MAX):
            for i in range(0, X_MAX):
                self._increase_energy_level((i, j))

    def _increase_energy_level(self, position: tuple[int, int]) -> None:
        self.octopuses[position].increase_energy_level()

    def _determine_flashers(self) -> list[Octopus]:
        flashers: list[Octopus] = []
        for j in range(0, Y_MAX):
            for i in range(0, X_MAX):
                if self.octopuses[(i, j)].will_flash():
                    flashers.append(self.octopuses[(i, j)])
        return flashers

    def clear(self) -> None:
        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")


class Octopus:
    def __init__(self, energy_level: int, position: tuple[int, int]) -> None:
        self.energy_level = energy_level
        self.position = position
        self.neighbors: list[tuple[int, int]] = []
        self.round: int = 0
        self.flashed: bool = False
        self._set_neighbors()

    def get_octopus_by_position(
        self, position: tuple[int, int]
    ) -> Optional[Octopus]:
        if self.position == position:
            return self
        return None

    def increase_energy_level(self) -> None:
        self.energy_level += 1

    def _can_flash(self) -> bool:
        if self.flashed:
            return False
        return True

    def will_flash(self) -> bool:
        if self._can_flash() and self.energy_level > 9:
            return True
        return False

    def flash(self) -> list[tuple[int, int]]:
        self.flashed = True
        return self.neighbors

    def reset(self) -> None:
        if self.flashed:
            self.energy_level = 0
            self.flashed = False

    def _set_neighbors(self) -> None:
        x: int = self.position[0]
        y: int = self.position[1]
        neighbors: list = [
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
        ]
        bads: list[tuple[int, int]] = []
        for neighbor in neighbors:
            if (
                neighbor[0] < 0
                or neighbor[0] >= X_MAX
                or neighbor[1] < 0
                or neighbor[1] >= Y_MAX
            ):
                bads.append(neighbor)
        for bad in bads:
            neighbors.remove(bad)
        self.neighbors = neighbors
