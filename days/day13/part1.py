from submarine.systems.fold import Origami


def solution(day):
    o = Origami(f"inputs/{day}.txt")
    num = o.run(only_once=True)
    return num
