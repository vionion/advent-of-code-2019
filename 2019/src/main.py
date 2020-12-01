import math
import string
from copy import copy
from random import sample

from io_utils import output_to_file, read_coma_separated_array, read_input_file


def day1_1():
    filename = "day1_1.txt"
    modules_masses = read_input_file(filename)
    fuel = 0
    for mass in modules_masses:
        fuel += _get_required_fuel_mass(mass)
    output_to_file(filename, str(fuel))


def _get_required_fuel_mass(mass):
    return math.floor(mass / 3) - 2


def day1_2():
    filename = "day1_2.txt"
    modules_masses = read_input_file(filename)
    fuel_mass = 0
    for module_mass in modules_masses:
        module_fuel_mass = _get_required_fuel_mass(module_mass)
        additional_fuel_mass = _get_required_fuel_mass(module_fuel_mass)
        while additional_fuel_mass > 0:
            module_fuel_mass += additional_fuel_mass
            additional_fuel_mass = _get_required_fuel_mass(additional_fuel_mass)
        fuel_mass += module_fuel_mass
    output_to_file(filename, str(fuel_mass))


def day2_1():
    filename = "day2_1.txt"
    intcode_program = read_coma_separated_array(filename)

    # restoring state to '1202 program alarm'
    noun = 12
    verb = 2
    try:
        output = _run_intcode_program(intcode_program, noun, verb)
    except IndexError as e:
        print(e)
    output_to_file(filename, str(output))


def day2_2():
    filename = "day2_1.txt"
    intcode_program = read_coma_separated_array(filename)

    noun = -1
    verb = -1
    # looking for noun and verbs which give 19690720
    for n in range(0, 100):
        noun = n
        for v in range(0, 100):
            verb = v
            try:
                output = _run_intcode_program(intcode_program, n, v)
            except IndexError as e:
                continue
            if output == 19690720:
                break
        if output == 19690720:
            break
    # 100 * noun + verb
    answer = 100 * noun + verb
    output_to_file(filename, str(answer))


def _run_intcode_program(intcode_program, noun, verb):
    unchanged_input_data = copy(intcode_program)
    if len(unchanged_input_data) < 3:
        raise IndexError("intocde program too short!")
    unchanged_input_data[1] = noun
    unchanged_input_data[2] = verb
    index = 0
    value = unchanged_input_data[index]
    top_possible_index = len(unchanged_input_data) - 1
    while value != 99 and index < len(unchanged_input_data):
        # case when opcode is for sum
        if value == 1:
            index += 1
            a_index = unchanged_input_data[index]
            index += 1
            b_index = unchanged_input_data[index]
            index += 1
            result_index = unchanged_input_data[index]
            if a_index > top_possible_index or b_index > top_possible_index:
                raise IndexError("instruction's parameter points to non-existing index")
            else:
                result = unchanged_input_data[a_index] + unchanged_input_data[b_index]
            if result_index > top_possible_index:
                raise IndexError("instruction's parameter points to non-existing index")
            else:
                unchanged_input_data[result_index] = result
        # case when opcode is for multiplication
        if value == 2:
            index += 1
            a_index = unchanged_input_data[index]
            index += 1
            b_index = unchanged_input_data[index]
            index += 1
            result_index = unchanged_input_data[index]
            if a_index > top_possible_index or b_index > top_possible_index:
                raise IndexError("instruction's parameter points to non-existing index")
            else:
                result = unchanged_input_data[a_index] * unchanged_input_data[b_index]
            if result_index > top_possible_index:
                raise IndexError("instruction's parameter points to non-existing index")
            else:
                unchanged_input_data[result_index] = result
        index += 1
        value = unchanged_input_data[index]
    answer = unchanged_input_data[0]
    return answer


possible_symbols = list(string.ascii_uppercase) + list(string.digits)
num_possible_symbols = len(possible_symbols)


def get_random_string():
    random_string = "".join(sample(possible_symbols, 4))
    return random_string


def send_code_request():
    import requests
    cookies = {"eduboxfi": "k5bqosbp0msd1fdtgdsuih8ju3"}

    # l1 = "LTO1"
    # l2 = "KU9Z"
    # l3 = "WCEP"
    while True:
        l1 = get_random_string()
        l2 = get_random_string()
        l3 = get_random_string()
        r = requests.post(
            f"https://oppilas.eautokoulu.fi/api/v1/auth/activate/?licencekey-1={l1}&licencekey-2={l2}&licencekey-3={l3}",
            cookies=cookies)
        message = r.json()["message"]
        if message != "Antamaasi lisenssiavainta ei tunnistettu":
            print(message)
            print(l1 + "-" + l2 + "-" + l3)
            print(r.json())


def get_sum(number):
    last_digit = number % 10
    middle_digit = (number % 100 - last_digit) / 10
    first_digit = (number - last_digit - middle_digit * 10) / 100
    sum = last_digit + first_digit + middle_digit
    # if sum > 9:
    #     return get_sum(sum)
    return sum


def lucky_numbbers():
    lucky_numbbers = 0
    for first_half in range(1, 1000):
        for second_half in range(0, 1000):
            first_half_sum = get_sum(first_half)
            second_half_sum = get_sum(second_half)
            if first_half_sum == second_half_sum:
                print(first_half, second_half)
                lucky_numbbers += 1

    print(lucky_numbbers)


def day3_1():
    filename = "day3_1.txt"
    first_wire, second_wire = read_coma_separated_array(filename)
    first_wire_coordinates = _paths_to_coordinates(first_wire)
    second_wire_coordinates = _paths_to_coordinates(second_wire)
    interception = _find_closest_interception(first_wire_coordinates, second_wire_coordinates)
    output = _manhattan_distance(interception[0], interception[1])
    output_to_file(filename, str(output))


def day3_2():
    filename = "day3_2.txt"
    first_wire, second_wire = read_coma_separated_array(filename)
    first_wire_coordinates = _paths_to_coordinates(first_wire)
    second_wire_coordinates = _paths_to_coordinates(second_wire)
    interception = _find_closest_interception(first_wire_coordinates, second_wire_coordinates)
    output = interception[2]
    output_to_file(filename, str(output))


def _manhattan_distance(x, y, x0=0, y0=0):
    return abs(x - x0) + abs(y - y0)


def _find_closest_interception(first_wire_coordinates, second_wire_coordinates):
    # there are two subcases: first wire intercept second horizontally and vertically
    first_wire_segments_vert = _filter_vertical_segments(first_wire_coordinates)
    second_wire_segments_vert = _filter_vertical_segments(second_wire_coordinates)
    first_wire_segments_horiz = _filter_horisontal_segments(first_wire_coordinates)
    second_wire_segments_horiz = _filter_horisontal_segments(second_wire_coordinates)
    # first_wire_segments_vert_sorted = sorted(first_wire_segments_vert, key=lambda x: x[0][0])
    # 1st cross vertically
    interceptions = _find_interceptions(first_wire_segments_vert, second_wire_segments_horiz)
    # 1st cross horizontally
    interceptions.extend(_find_interceptions(second_wire_segments_vert, first_wire_segments_horiz))
    # interceptions_sorted = sorted(interceptions, key=lambda x: _manhattan_distance(x[0], x[1]))
    interceptions_sorted = sorted(interceptions, key=lambda x: x[2])
    closest_interception = interceptions_sorted[0]
    if closest_interception == (0, 0, 0):
        # if closest_interception == (0, 0):
        closest_interception = interceptions_sorted[1]
    return closest_interception


def _find_interceptions(wire_segments_vert, wire_segments_horiz):
    result = []
    for segment_vert in wire_segments_vert:
        for segment_horiz in wire_segments_horiz:
            vert_x = segment_vert[0][0]
            horiz_x1 = segment_horiz[0][0]
            horiz_x2 = segment_horiz[1][0]

            vert_y1 = segment_vert[0][1]
            vert_y2 = segment_vert[1][1]
            horiz_y = segment_horiz[0][1]
            if min(horiz_x1, horiz_x2) <= vert_x <= max(horiz_x1, horiz_x2):
                if min(vert_y1, vert_y2) <= horiz_y <= max(vert_y1, vert_y2):
                    steps_required_a = segment_vert[2] + _manhattan_distance(vert_x, horiz_y, segment_vert[0][0],
                                                                             segment_vert[0][1])
                    steps_required_b = segment_horiz[2] + _manhattan_distance(vert_x, horiz_y, segment_horiz[0][0],
                                                                              segment_horiz[0][1])
                    result.append((vert_x, horiz_y, steps_required_a + steps_required_b))
    return result


def _filter_vertical_segments(wire_coordinates):
    vertical_segments = []
    last_point = wire_coordinates[-1]
    steps_required = 0
    for i in range(0, len(wire_coordinates)):
        point = wire_coordinates[i]
        # just the most clear check for non-last point I could came up with
        if point is not last_point:
            next_point = wire_coordinates[i + 1]
            point_a_x = point[0]
            point_b_x = next_point[0]
            if point_a_x == point_b_x:
                vertical_segments.append((point, next_point, steps_required))
            steps_required += _manhattan_distance(next_point[0], next_point[1], point[0], point[1])
    return vertical_segments


def _filter_horisontal_segments(wire_coordinates):
    horisontal_segments = []
    last_point = wire_coordinates[-1]
    steps_required = 0
    for i in range(0, len(wire_coordinates)):
        point = wire_coordinates[i]
        # just the most clear check for non-last point I could came up with
        if point is not last_point:
            next_point = wire_coordinates[i + 1]
            point_a_y = point[1]
            point_b_y = next_point[1]
            if point_a_y == point_b_y:
                horisontal_segments.append((point, next_point, steps_required))
            steps_required += _manhattan_distance(next_point[0], next_point[1], point[0], point[1])
    return horisontal_segments


def _paths_to_coordinates(paths):
    zero_point = (0, 0)
    coordinates = [zero_point]
    previous_point = zero_point
    for path in paths:
        direction = path[0]
        distance = int(path[1:])
        if direction == "R":
            next_point = (previous_point[0] + distance, previous_point[1])
        elif direction == "U":
            next_point = (previous_point[0], previous_point[1] + distance)
        elif direction == "L":
            next_point = (previous_point[0] - distance, previous_point[1])
        elif direction == "D":
            next_point = (previous_point[0], previous_point[1] - distance)
        coordinates.append(next_point)
        previous_point = next_point
    return coordinates


def day4_1():
    min_limit = 284639
    max_limit = 748759
    valid_passwords = 0
    for password in range(min_limit, max_limit + 1):
        digits = [int(d) for d in str(password)]
        if _has_double(digits) and _dont_decrease(digits):
            valid_passwords += 1
    print(valid_passwords)


def day4_2():
    min_limit = 284639
    max_limit = 748759
    valid_passwords = 0
    for password in range(min_limit, max_limit + 1):
        digits = [int(d) for d in str(password)]
        if _has_double_and_only_double(digits) and _dont_decrease(digits):
            valid_passwords += 1
    print(valid_passwords)


def _has_double_and_only_double(digits):
    previous_digit = digits[0]
    group_size = 1
    for digit in digits[1:]:
        if previous_digit == digit:
            group_size += 1
        else:
            if group_size == 2:
                return True
            group_size = 1
        previous_digit = digit
    return group_size == 2


def _has_double(digits):
    previous_digit = digits[0]
    for digit in digits[1:]:
        if previous_digit == digit:
            return True
        previous_digit = digit
    return False


def _dont_decrease(digits):
    previous_digit = digits[0]
    for digit in digits[1:]:
        if previous_digit > digit:
            return False
        previous_digit = digit
    return True


def _run_diagnostic_intcode_program(intcode_program, input):
    unchanged_input_data = copy(intcode_program)
    input_iterator = iter(input)

    index = 0
    value = unchanged_input_data[index]
    top_possible_index = len(unchanged_input_data) - 1
    while value != 99 and index < len(unchanged_input_data):
        # case when opcode is for sum
        if value == 1:
            index += 1
            a_index = unchanged_input_data[index]
            index += 1
            b_index = unchanged_input_data[index]
            index += 1
            result_index = unchanged_input_data[index]
            if a_index > top_possible_index or b_index > top_possible_index:
                raise IndexError("instruction's parameter points to non-existing index")
            else:
                result = unchanged_input_data[a_index] + unchanged_input_data[b_index]
            if result_index > top_possible_index:
                raise IndexError("instruction's parameter points to non-existing index")
            else:
                unchanged_input_data[result_index] = result
        # case when opcode is for multiplication
        if value == 2:
            index += 1
            a_index = unchanged_input_data[index]
            index += 1
            b_index = unchanged_input_data[index]
            index += 1
            result_index = unchanged_input_data[index]
            if a_index > top_possible_index or b_index > top_possible_index:
                raise IndexError("instruction's parameter points to non-existing index")
            else:
                result = unchanged_input_data[a_index] * unchanged_input_data[b_index]
            if result_index > top_possible_index:
                raise IndexError("instruction's parameter points to non-existing index")
            else:
                unchanged_input_data[result_index] = result
        # case when opcode is for entering input
        if value == 3:
            index += 1
            index_for_input = unchanged_input_data[index]

            if index_for_input > top_possible_index:
                raise IndexError("instruction's parameter points to non-existing index")
            else:
                unchanged_input_data[index_for_input] = input_iterator
                next(input_iterator)
        # case when opcode is for output
        if value == 4:
            index += 1
            index_for_output = unchanged_input_data[index]

            if index_for_output > top_possible_index:
                raise IndexError("instruction's parameter points to non-existing index")
            else:
                print(unchanged_input_data[index_for_output])
        index += 1
        value = unchanged_input_data[index]
    return 0


def day5_1():
    filename = "day5_1.txt"
    diagnostic_intcode_program = read_coma_separated_array(filename)

    diagnostic_inputs = [1]
    try:
        output = _run_diagnostic_intcode_program(diagnostic_intcode_program, diagnostic_inputs)
    except IndexError as e:
        print(e)
    output_to_file(filename, str(output))


if __name__ == '__main__':
    # day1_1()
    # day1_2()
    # day2_1()
    # day2_2()
    # day3_1()
    # day3_2()
    # day4_1()
    # day4_2()
    day5_1()
