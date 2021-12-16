from submarine.systems.fold import Origami


def solution(day):
    o = Origami(f"inputs/{day}.txt")
    o.run(only_once=False)
    o.print()
