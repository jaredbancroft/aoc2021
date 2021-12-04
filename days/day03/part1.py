from helpers import inputs
from submarine.submarine import Submarine


def solution(day):
    report = inputs.read_to_list(f"inputs/{day}.txt")
    s = Submarine()
    power_consumption = s.diagnostics("power_consumption", report)
    return power_consumption
