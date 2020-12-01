from io_utils import read_input_file


def day1_1():
    arr = read_input_file("day1.txt")
    pairs_dict = dict((input_value, 2020-input_value) for input_value in arr)
    for value, pair in pairs_dict.items():
        if pair in pairs_dict.keys():
            return pair * value
