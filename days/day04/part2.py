from submarine.systems.bingo import BingoSubsystem


def solution(day):
    b = BingoSubsystem(f"inputs/{day}.txt")
    score = b.play("lose")
    return score
