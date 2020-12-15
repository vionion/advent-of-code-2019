from io_utils import read_coma_separated_array


def say_number(spoken_numbers, turn, last_spoken_number):
    if last_spoken_number not in spoken_numbers.keys():
        spoken_numbers[last_spoken_number] = turn
        return 0
    else:
        last_time_spoken = spoken_numbers[last_spoken_number]
        spoken_numbers[last_spoken_number] = turn
        return turn - last_time_spoken


def day15_1():
    starting_numbers = read_coma_separated_array("day15.txt")
    return get_last_spoken_number(starting_numbers=starting_numbers, iterations=2020)


def get_last_spoken_number(starting_numbers, iterations):
    spoken_numbers = {}  # must be faster than list.index(val), as that one uses linear search
    turn = 1
    for number in starting_numbers[:-1]:
        spoken_numbers[number] = turn
        turn += 1
    last_spoken_number = starting_numbers[-1]
    while turn < iterations:
        last_spoken_number = say_number(spoken_numbers, turn, last_spoken_number)
        turn += 1
    return last_spoken_number


def day15_2():
    starting_numbers = read_coma_separated_array("day15.txt")
    return get_last_spoken_number(starting_numbers=starting_numbers, iterations=30000000)
