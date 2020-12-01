import math
import string
from copy import copy
from random import randint, sample

from src.io_utils import output_to_file, read_coma_separated_array, read_input_file


def day1_1():
    filename = "day1.txt"
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
        r = requests.post(f"https://oppilas.eautokoulu.fi/api/v1/auth/activate/?licencekey-1={l1}&licencekey-2={l2}&licencekey-3={l3}", cookies=cookies)
        message = r.json()["message"]
        if message != "Antamaasi lisenssiavainta ei tunnistettu":
            print(message)
            print(l1+"-"+l2+"-"+l3)
            print(r.json())


def get_sum(number):
    last_digit = number%10
    middle_digit = (number%100 - last_digit)/10
    first_digit = (number - last_digit - middle_digit*10)/100
    sum = last_digit+first_digit+middle_digit
    # if sum > 9:
    #     return get_sum(sum)
    return sum



def lucky_numbbers():
    lucky_numbbers = 0
    for first_half in range(1,1000):
        for second_half in range(0, 1000):
            first_half_sum = get_sum(first_half)
            second_half_sum = get_sum(second_half)
            if first_half_sum == second_half_sum:
                print(first_half, second_half)
                lucky_numbbers +=1

    print(lucky_numbbers)

if __name__ == '__main__':
    # day1_1()
    # day1_2()
    # day2_1()
    # day2_2()
    # lucky_numbbers()
    send_code_request()
