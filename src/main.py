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


if __name__ == '__main__':
    day1_1()
    day1_2()
    day2_1()
    day2_2()
