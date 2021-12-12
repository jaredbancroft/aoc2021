from submarine.systems.lava import LavaScan, HeightMap


def solution(day):
    scan = LavaScan(f"inputs/{day}.txt")
    return scan.hm.find_largest_basins()
