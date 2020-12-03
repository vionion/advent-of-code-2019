from io_utils import read_2d_array


def day3_1():
    input_map = read_2d_array("day3.txt")
    return get_trees_count_on_slope(input_map, right_steps=3, down_steps=1)


def get_trees_count_on_slope(input_map, right_steps, down_steps):
    row, column = 0, 0
    trees_counter = 0
    pattern_length = len(input_map[column]) - 1  # because I am lazy to trim /n at the end of each line
    while column < len(input_map) - down_steps:
        column += down_steps
        row += right_steps
        if row > pattern_length - 1:  # because comparing index and length
            row = row - pattern_length
        if input_map[column][row] == "#":
            trees_counter += 1
    return trees_counter




def day3_2():
    input_map = read_2d_array("day3.txt")
    result = get_trees_count_on_slope(input_map, right_steps=1, down_steps=1)
    result *= get_trees_count_on_slope(input_map, right_steps=3, down_steps=1)
    result *= get_trees_count_on_slope(input_map, right_steps=5, down_steps=1)
    result *= get_trees_count_on_slope(input_map, right_steps=7, down_steps=1)
    result *= get_trees_count_on_slope(input_map, right_steps=1, down_steps=2)
    return result
