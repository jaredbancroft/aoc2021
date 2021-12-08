import statistics
from typing import List


class Aligner:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.run()

    def run(self) -> int:
        with open(self.filepath, "r", encoding="utf-8") as f:
            line = f.readline().rstrip().split(",")
        crabs = [int(x) for x in line]
        target = statistics.median(crabs)
        fuel = self.calculate_fuel(int(target), crabs, advanced=False)
        return fuel

    def run_brute_force(self) -> int:
        with open(self.filepath, "r", encoding="utf-8") as f:
            line = f.readline().rstrip().split(",")
        crabs = [int(x) for x in line]
        target = max(crabs)
        min_fuel = 100000000000000000000
        for i in range(0, target + 1):
            fuel = self.calculate_fuel(i, crabs, advanced=True)
            if fuel < min_fuel:
                min_fuel = fuel
        return min_fuel

    def calculate_fuel(self, target: int, crabs: List, advanced: bool) -> int:
        total_fuel = 0
        for crab in crabs:
            fuel = 0
            if advanced:
                distance = abs(crab - target)
                for i in range(0, distance):
                    fuel += (1 * i) + 1
                total_fuel += fuel
            else:
                total_fuel += abs(crab - target)
        return total_fuel
