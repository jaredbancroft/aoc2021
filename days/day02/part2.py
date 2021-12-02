from submarine.submarine import Submarine


def solution(day):
    s = Submarine()
    with open(f"inputs/{day}.txt", "r", encoding="utf-8") as f:
        while True:
            line = f.readline()
            if not line:
                break
            command = line.split()
            s.move(command[0], int(command[1]))

    return s.xpos * s.depth
