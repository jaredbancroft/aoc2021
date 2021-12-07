from submarine.systems.vents import HydrothermalVentScanner


def solution(day):
    h = HydrothermalVentScanner(f"inputs/{day}.txt")
    danger_level = h.analyze(diagonals=True)
    return danger_level
