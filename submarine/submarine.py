class Submarine:
    def __init__(self, xpos=0, depth=0, aim=0):
        self.xpos = xpos
        self.depth = depth
        self.aim = aim

    def move_incorrectly(self, direction, value):
        if direction == "forward":
            self.xpos += value
        elif direction == "up":
            self.depth -= value
        elif direction == "down":
            self.depth += value

    def move(self, direction, value):
        if direction == "forward":
            self.xpos += value
            self.depth += self.aim * value
        elif direction == "up":
            self.aim -= value
        elif direction == "down":
            self.aim += value
