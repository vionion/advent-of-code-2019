from io_utils import read_input_file


def day1_1():
    arr = read_input_file("day1.txt")
    entry1, entry2 = find_entries_that_sum(arr, 2020)
    return entry1 * entry2


def find_entries_that_sum(arr, total):
    pairs_dict = dict((input_value, total - input_value) for input_value in arr)
    for value, pair in pairs_dict.items():
        if pair in pairs_dict.keys():
            return pair, value
    return None, None


def day1_2():
    arr = read_input_file("day1.txt")
    arr.sort()
    for entry1 in arr:
        subsum = 2020 - entry1
        subatr = [val for val in arr if val < subsum]  # kinda pointless optimisation. Works a few tens of ms faster tho
        entry2, entry3 = find_entries_that_sum(subatr, subsum)
        if entry2 is not None and entry3 is not None:  # second check just in case, but really no reason for that
            return entry1 * entry2 * entry3
