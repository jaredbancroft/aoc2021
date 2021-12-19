from submarine.systems.polymers import Polymer


def solution(day):
    p = Polymer(f"inputs/{day}.txt")
    ans = p.polymerize(40)
    return ans
