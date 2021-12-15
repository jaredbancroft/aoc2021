from submarine.systems.paths import PathFinder


def solution(day):
    p = PathFinder(f"inputs/{day}.txt")
    path = []
    paths = p.find_paths(p.graph, "start", "end", path)
    return len(paths)
