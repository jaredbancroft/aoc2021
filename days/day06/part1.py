from submarine.systems.fish import FastModel


def solution(day):
    b = FastModel(f"inputs/{day}.txt")
    fishies = b.run(80)
    return fishies
