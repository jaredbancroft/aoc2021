from collections import defaultdict, Counter


class PathFinder:
    def __init__(self, filename) -> None:
        self.graph: dict[str, list[str]] = self._load_arcs(filename)

    def _load_arcs(self, filename: str) -> dict[str, list[str]]:
        graph: defaultdict[str, list[str]] = defaultdict(list)
        with open(filename, "r", encoding="utf-8") as f:
            while True:
                line: str = f.readline().rstrip()
                if not line:
                    break
                parsed_line: list[str] = line.split("-")
                key: str = parsed_line[0]
                value: str = parsed_line[1]
                graph[key].append(value)
                key = parsed_line[1]
                value = parsed_line[0]
                graph[key].append(value)
        return dict(graph)

    def find_paths(
        self,
        graph: dict[str, list[str]],
        start: str,
        end: str,
        path: list[str] = [],
    ) -> list[list[str]]:
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths: list[list[str]] = []
        for node in graph[start]:
            if node not in path or node.isupper():
                newpaths = self.find_paths(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def find_paths2(
        self,
        graph: dict[str, list[str]],
        start: str,
        end: str,
        path: list[str] = [],
    ) -> list[list[str]]:
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths: list[list[str]] = []
        for node in graph[start]:
            if node not in path or node.isupper():
                newpaths = self.find_paths2(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
            elif node != "start" and self._only_one_lower_repeated(path):
                newpaths = self.find_paths2(graph, node, end, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def _only_one_lower_repeated(self, path: list[str]) -> bool:
        frequency: Counter = Counter(path)
        for key in frequency.keys():
            if key.islower() and frequency[key] == 2:
                return False
        return True
