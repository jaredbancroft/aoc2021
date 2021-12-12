from __future__ import annotations
from dataclasses import dataclass


class LavaScan:
    def __init__(self, filepath: str) -> None:
        locations = self.load_input(filepath)
        self.hm = HeightMap(locations)

    def load_input(self, filepath: str) -> list[list[Location]]:
        locations: list[list[Location]] = []
        with open(filepath, "r", encoding="utf-8") as f:
            location: list[Location]
            while True:
                line = list(f.readline().rstrip())
                if not line:
                    break
                location = [Location(int(x)) for x in line]
                locations.append(location)
        return locations


class HeightMap:
    def __init__(self, locations: list[list[Location]]) -> None:
        self.locations = locations
        self.y_max = len(self.locations)
        self.x_max = len(self.locations[0])

    def find_largest_basins(self) -> int:
        sizes: list[int] = []
        low_point_coords = self.find_low_point_coordinates()
        for low_point_coord in low_point_coords:
            visited: list = []
            basin: Basin = Basin(visited)
            self.map_basin_size(low_point_coord, basin)
            sizes.append(basin.get_size())
        sizes.sort(reverse=True)
        return sizes[0] * sizes[1] * sizes[2]

    def map_basin_size(self, coord: tuple[int, int], basin: Basin) -> None:
        if self.locations[coord[1]][
            coord[0]
        ].height != 9 and basin.is_not_visited(coord):
            basin.add_visited(coord)
            neighbors: list[tuple[int, int]] = self.get_neighbors(
                coord[0], coord[1]
            )
            for neighbor in neighbors:
                self.map_basin_size(neighbor, basin)

    def total_danger_level(self) -> int:
        total = 0
        low_point_coords = self.find_low_point_coordinates()
        for low_point_coord in low_point_coords:
            low_point = self.get_low_point_location(
                low_point_coord[0], low_point_coord[1]
            )
            total += self.set_danger_level(low_point)
        return total

    def get_low_point_location(self, x: int, y: int) -> Location:
        low_point = self.locations[y][x]
        return low_point

    def set_danger_level(self, low_point: Location) -> int:
        low_point.danger_level = low_point.height + 1
        return low_point.danger_level

    def find_low_point_coordinates(self) -> list[tuple[int, int]]:
        low_points: list[tuple[int, int]] = []
        for y_index, locations in enumerate(self.locations):
            for x_index, location in enumerate(locations):
                neighbor_coords = self.get_neighbors(x_index, y_index)
                is_low = True
                for coord in neighbor_coords:
                    if (
                        location.height
                        >= self.locations[coord[1]][coord[0]].height
                    ):
                        is_low = False
                if is_low:
                    low_points.append((x_index, y_index))
        return low_points

    def get_neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []
        if self.left_neighbor_exists(x, y):
            neighbors.append((x - 1, y))
        if self.right_neighbor_exists(x, y):
            neighbors.append((x + 1, y))
        if self.bottom_neighbor_exists(x, y):
            neighbors.append((x, y + 1))
        if self.top_neighbor_exists(x, y):
            neighbors.append((x, y - 1))
        return neighbors

    def left_neighbor_exists(self, x: int, y: int) -> bool:
        if x - 1 >= 0:
            return True
        return False

    def right_neighbor_exists(self, x: int, y: int) -> bool:
        if x + 1 < self.x_max:
            return True
        return False

    def bottom_neighbor_exists(self, x: int, y: int) -> bool:
        if y + 1 < self.y_max:
            return True
        return False

    def top_neighbor_exists(self, x: int, y: int) -> bool:
        if y - 1 >= 0:
            return True
        return False


@dataclass
class Location:
    height: int
    danger_level: int = 0


class Basin:
    def __init__(self, visited: list[tuple[int, int]]) -> None:
        self.visited = visited

    def get_size(self) -> int:
        return len(self.visited)

    def add_visited(self, coord: tuple[int, int]) -> None:
        self.visited.append(coord)

    def is_not_visited(self, coord: tuple[int, int]) -> bool:
        if coord in self.visited:
            return False
        return True
