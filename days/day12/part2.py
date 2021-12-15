from submarine.systems.paths import PathFinder


def solution(day):
    p = PathFinder(f"inputs/{day}.txt")
    path = []
    paths = p.find_paths2(p.graph, "start", "end", path)
    return len(paths)
