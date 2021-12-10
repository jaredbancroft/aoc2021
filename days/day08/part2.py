from submarine.systems.display import SevenSegmentDisplay


def solution(day):
    s = SevenSegmentDisplay(f"inputs/{day}.txt")
    return s.decode()
