from io_utils import read_input_file


def day10_1():
    adapters_list = read_input_file("day10.txt", input_type=int)
    adapters_list.sort()
    adapters_list.append(adapters_list[-1] + 3)  # adding embedded adaptor to the end
    previous_joltage = 0
    one_jolt_differences = 0
    three_jolt_differences = 0
    for adapter_input in adapters_list:
        if adapter_input - previous_joltage == 3:
            three_jolt_differences += 1
        if adapter_input - previous_joltage == 1:
            one_jolt_differences += 1
        previous_joltage = adapter_input
    return one_jolt_differences * three_jolt_differences


def get_next_possible_options(adapter_index, adapters_list):
    result = []
    for adapter in adapters_list[adapter_index + 1: min(adapter_index + 4, len(adapters_list))]:
        if adapter - adapters_list[adapter_index] <= 3:
            result.append(adapter)
    return result


def get_possible_combinations(adapter_index, adapters_list):
    if adapter_index == len(adapters_list) - 1:
        return 1
    next_steps = get_next_possible_options(adapter_index, adapters_list)
    possible_options = 0
    for adapter in next_steps:
        possible_next_step = adapters_list.index(adapter)
        possible_options += get_possible_combinations(possible_next_step, adapters_list)
    return possible_options


def split_into_sublists(adapters_list):
    last_added_list_index = 0
    result = [[adapters_list[last_added_list_index]]]
    last_added_adapter = adapters_list[last_added_list_index]
    for adapter_input in adapters_list[1:]:
        if adapter_input - last_added_adapter < 3:
            result[last_added_list_index].append(adapter_input)
        else:
            result.append([adapter_input])
            last_added_list_index += 1
        last_added_adapter = adapter_input
    return result


def day10_2():
    adapters_list = read_input_file("day10.txt", input_type=int)
    adapters_list.sort()
    adapters_list.append(adapters_list[-1] + 3)  # adding embedded adapter to the end
    adapters_list.insert(0, 0)  # adding charging outlet output at the begging
    sublists = split_into_sublists(adapters_list)
    possible_combinations = 1
    for sublist in sublists:
        possible_combinations *= get_possible_combinations(0, sublist)
    return possible_combinations
