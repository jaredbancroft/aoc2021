from helpers import inputs


def solution(day):
    depths = inputs.read_to_list(f"inputs/{day}.txt")
    part1_total = 0
    for index, depth in enumerate(depths):
        if index - 1 >= 0:
            diff = int(depth) - int(depths[index - 1])
            if diff > 0:
                part1_total += 1
    return f"Day 01 Part 1 Total Depth Increase: {part1_total}"
