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

    def diagnostics(self, test, inputs):
        if test == "power_consumption":
            return self._power_consumption(inputs)
        elif test == "o2":
            return self._o2_generator_rating(inputs)
        elif test == "co2":
            return self._co2_scrubber_rating(inputs)
        else:
            return "No such test"

    def _power_consumption(self, inputs):
        total_length = len(inputs)
        bit_length = len(inputs[0])
        acc = [0] * bit_length
        for input in inputs:
            i = bit_length
            for bit in input:
                acc[bit_length - i] += int(bit)
                i -= 1
            gamma = int(
                "".join([str(round(x / total_length)) for x in acc]), 2
            )
            epsilon = int(
                "".join([str(round(x / total_length) ^ 1) for x in acc]), 2
            )
        return gamma * epsilon

    def _o2_generator_rating(self, inputs):
        zeros = []
        ones = []
        i = 0
        while len(inputs) != 1:
            total_length = len(inputs)
            for input in inputs:
                if input[i] == "0":
                    zeros.append(input)
                else:
                    ones.append(input)
            if len(zeros) > total_length / 2:
                ones = []
                inputs = zeros
                zeros = []
            else:
                zeros = []
                inputs = ones
                ones = []
            i += 1
        return int("".join(inputs), 2)

    def _co2_scrubber_rating(self, inputs):
        zeros = []
        ones = []
        i = 0
        while len(inputs) != 1:
            total_length = len(inputs)
            for input in inputs:
                if input[i] == "0":
                    zeros.append(input)
                else:
                    ones.append(input)
            if len(zeros) <= total_length / 2:
                ones = []
                inputs = zeros
                zeros = []
            else:
                zeros = []
                inputs = ones
                ones = []
            i += 1
        return int("".join(inputs), 2)
