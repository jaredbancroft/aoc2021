class HydrothermalVentScanner:
    def __init__(self, filepath):
        self.name = "HVS"
        self.filepath = filepath
        self.max_x = 0
        self.max_y = 0
        self.segments = self.init()

    def init(self):
        segments = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            while True:
                line = f.readline().rstrip()
                if not line:
                    break
                x1 = int(line.split(" -> ")[0].split(",")[0])
                x2 = int(line.split(" -> ")[1].split(",")[0])
                y1 = int(line.split(" -> ")[0].split(",")[1])
                y2 = int(line.split(" -> ")[1].split(",")[1])
                p1 = Point(x1, y1)
                p2 = Point(x2, y2)
                segment = LineSegment(p1, p2)
                self.set_grid_dimensions(segment)
                segments.append(segment)
            self.grid = self.make_grid(self.max_x, self.max_y)
            return segments

    def set_grid_dimensions(self, segment):
        for point in segment:
            self.max_dimensions(point)

    def max_dimensions(self, point):
        if point.x > self.max_x:
            self.max_x = point.x
        if point.y > self.max_y:
            self.max_y = point.y

    def make_grid(self, width, height):
        return [[0 for x in range(height + 1)] for x in range(width + 1)]

    def print_grid(self):
        for j in range(self.max_y + 1):
            for i in range(self.max_x + 1):
                print(f"{self.grid[i][j]} ", end="")
            print("\n")

    def calculate_danger(self):
        danger_level = 0
        for row in self.grid:
            for value in row:
                if value >= 2:
                    danger_level += 1
        return danger_level

    def analyze(self, diagonals=False):
        for segment in self.segments:
            if segment.is_horizontal():
                self.grid = segment.interpolate_horizontal(self.grid)
            if segment.is_vertical():
                self.grid = segment.interpolate_vertical(self.grid)
            if diagonals and segment.is_diagonal():
                self.grid = segment.interpolate_diagonal(self.grid)
        return self.calculate_danger()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def print(self):
        print(f"({self.x},{self.y})")

    def get_coords(self):
        return self.x, self.y


class LineSegmentIterator:
    def __init__(self, segment):
        self.segment = segment
        self.index = 0

    def __next__(self):
        point_list = [self.segment.p1, self.segment.p2]
        if self.index < len(point_list):
            result = point_list[self.index]
            self.index += 1
            return result
        raise StopIteration


class LineSegment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __iter__(self):
        return LineSegmentIterator(self)

    def print(self):
        print(f"{self.p1.get_coords()} -> {self.p2.get_coords()}")

    def is_horizontal(self):
        if self.p1.x == self.p2.x:
            return True
        return False

    def is_vertical(self):
        if self.p1.y == self.p2.y:
            return True
        return False

    def is_diagonal(self):
        if self.p1.x != self.p2.x and self.p1.y != self.p2.y:
            return True
        return False

    def interpolate_vertical(self, grid):
        low_bound, high_bound = self.bound_interpolation(self.p1.x, self.p2.x)
        for x in range(low_bound, high_bound + 1):
            grid[x][self.p1.y] += 1
        return grid

    def interpolate_horizontal(self, grid):
        low_bound, high_bound = self.bound_interpolation(self.p1.y, self.p2.y)
        for y in range(low_bound, high_bound + 1):
            grid[self.p1.x][y] += 1
        return grid

    def interpolate_diagonal(self, grid):
        if self.p1.x < self.p2.x:
            if self.p1.y < self.p2.y:
                i = 0
                for x in range(self.p1.x, self.p2.x + 1):
                    grid[x][self.p1.y + i] += 1
                    i += 1
            else:
                i = 0
                for x in range(self.p1.x, self.p2.x + 1):
                    grid[x][self.p1.y - i] += 1
                    i += 1
        elif self.p1.x > self.p2.x:
            if self.p1.y < self.p2.y:
                i = 0
                for x in range(self.p2.x, self.p1.x + 1):
                    grid[x][self.p2.y - i] += 1
                    i += 1
            else:
                i = 0
                for x in range(self.p2.x, self.p1.x + 1):
                    grid[x][self.p2.y + i] += 1
                    i += 1
        return grid

    def swap_bounds(self, low_bound, high_bound):
        return high_bound, low_bound

    def bound_interpolation(self, coord1, coord2):
        low_bound = coord1
        high_bound = coord2
        if low_bound > high_bound:
            low_bound, high_bound = self.swap_bounds(low_bound, high_bound)
        return low_bound, high_bound
