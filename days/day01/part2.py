from helpers import inputs


def solution():
    depths = inputs.read_to_list("inputs/day1.txt")
    part2_total = 0
    for index, depth in enumerate(depths):
        if index - 3 >= 0:
            current_window = (
                int(depth) + int(depths[index - 1]) + int(depths[index - 2])
            )
            previous_window = (
                int(depths[index - 1])
                + int(depths[index - 2])
                + int(depths[index - 3])
            )
            diff = current_window - previous_window
            if diff > 0:
                part2_total += 1
    return f"Day 01 Part 2 Total Depth Increase: {part2_total}"
