from os.path import join

INPUTS_FOLDER = "inputs"
OUTPUTS_FOLDER = "outputs"


def output_to_file(filename, output, base="2020"):
    with open(join(base, OUTPUTS_FOLDER, filename), "w") as file:
        file.write(output)


def read_input_file(filename, base="2020"):
    input_array = []
    file = open(join(base, INPUTS_FOLDER, filename), "r")
    for line in file:
        input_array.append(int(line))
    return input_array


def read_coma_separated_array(filename, base="2020"):
    file = open(join(base, INPUTS_FOLDER, filename), "r")
    input_array = file.readline().split(",")
    input_array = [int(x) for x in input_array]
    return input_array