from helpers import inputs
from submarine.submarine import Submarine


def solution(day):
    report = inputs.read_to_list(f"inputs/{day}.txt")
    s = Submarine()
    o2_rating = s.diagnostics("o2", report)
    co2_rating = s.diagnostics("co2", report)
    return o2_rating * co2_rating
