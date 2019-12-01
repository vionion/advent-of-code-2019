import math
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


if __name__ == '__main__':
    day1_1()
    day1_2()
