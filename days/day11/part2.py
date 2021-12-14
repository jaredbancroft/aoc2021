from submarine.systems.energy import RemoteEnergyDetector


def solution(day):
    r = RemoteEnergyDetector(f"inputs/{day}.txt")
    return r.run_sync()
