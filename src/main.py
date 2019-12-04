import math
from copy import copy
from os.path import join

INPUTS_FOLDER = "inputs"
OUTPUTS_FOLDER = "outputs"


def write_to_output_file(filename, output):
    with open(join(OUTPUTS_FOLDER, filename), "w") as file:
        file.write(output)


def read_input_file(filename):
    input_array = []
    file = open(join(INPUTS_FOLDER, filename), "r")
    for line in file:
        input_array.append(int(line))
    return input_array


def read_coma_separated_array(filename):
    file = open(join(INPUTS_FOLDER, filename), "r")
    input_array = file.readline().split(",")
    input_array = [int(x) for x in input_array]
    return input_array


def read_coma_separated_coordinates(filename):
    file = open(join(INPUTS_FOLDER, filename), "r")
    first_wire = file.readline().strip("\n").split(",")
    second_wire = file.readline().split(",")
    return first_wire, second_wire


def day1_1():
    filename = "day1_1.txt"
    modules_masses = read_input_file(filename)
    fuel = 0
    for mass in modules_masses:
        fuel += _get_required_fuel_mass(mass)
    write_to_output_file(filename, str(fuel))


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
    write_to_output_file(filename, str(fuel_mass))


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
    write_to_output_file(filename, str(output))


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
    write_to_output_file(filename, str(answer))


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


def day3_1():
    filename = "day3_1.txt"
    first_wire, second_wire = read_coma_separated_coordinates(filename)
    first_wire_coordinates = _paths_to_coordinates(first_wire)
    second_wire_coordinates = _paths_to_coordinates(second_wire)
    interception = _find_closest_interception(first_wire_coordinates, second_wire_coordinates)
    output = _manhattan_distance(interception[0], interception[1])
    write_to_output_file(filename, str(output))


def day3_2():
    filename = "day3_2.txt"
    first_wire, second_wire = read_coma_separated_coordinates(filename)
    first_wire_coordinates = _paths_to_coordinates(first_wire)
    second_wire_coordinates = _paths_to_coordinates(second_wire)
    interception = _find_closest_interception(first_wire_coordinates, second_wire_coordinates)
    output = interception[2]
    write_to_output_file(filename, str(output))


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


if __name__ == '__main__':
    day1_1()
    day1_2()
    day2_1()
    day2_2()
    day3_1()
    day3_2()
    day4_1()
    day4_2()
