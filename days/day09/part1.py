from submarine.systems.lava import LavaScan, HeightMap


def solution(day):
    scan = LavaScan(f"inputs/{day}.txt")
    return scan.hm.total_danger_level()
