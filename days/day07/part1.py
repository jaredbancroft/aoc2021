from submarine.systems.crab import Aligner


def solution(day):
    a = Aligner(f"inputs/{day}.txt")
    return a.run()
