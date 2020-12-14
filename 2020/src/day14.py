from io_utils import read_input_file


def add_leading_zeros(param_bin):
    num_zeros = 36-len(param_bin)
    zeros = ['0'] * num_zeros
    zeros.extend(param_bin)
    return zeros


def apply_mask(mask, param):
    param_bin = list(bin(param))[2:]
    param_bin = add_leading_zeros(param_bin)
    for i, char in enumerate(mask):
        if mask[i] != "X":
            param_bin[i] = mask[i]

    param_dec = int("".join(param_bin), 2)
    return param_dec


def day14_1():
    init_program = read_input_file("day14.txt", input_type=str, strip=True)
    mem = {}
    mask = ["X"] * 36
    for instruction in init_program:
        instruction, param = instruction.split(" = ")
        if instruction == "mask":
            mask = list(param)
        if "mem" in instruction:
            address = int(instruction[4:-1])
            dec_param = apply_mask(mask, int(param))
            mem[address] = dec_param
    sum = 0
    for cell in mem.values():
        sum += cell
    return sum


def apply_address_mask(mask, address):
    address_bin = list(bin(address))[2:]
    address_bin = add_leading_zeros(address_bin)
    for i, char in enumerate(mask):
        if mask[i] == "0":
            continue
        else:
            address_bin[i] = mask[i]
    return address_bin


def populate_masked_address(floating_address):
    addresses = []
    for i, char in enumerate(floating_address):
        if char == "X":
            option_a = floating_address.copy()
            option_a[i] = '0'
            option_b = floating_address.copy()
            option_b[i] = '1'
            addresses.extend(populate_masked_address(option_a))
            addresses.extend(populate_masked_address(option_b))
            return addresses
    return [floating_address]


def day14_2():
    init_program = read_input_file("day14.txt", input_type=str, strip=True)
    mem = {}
    mask = ["X"] * 36
    for instruction in init_program:
        instruction, param = instruction.split(" = ")
        if instruction == "mask":
            mask = list(param)
        if "mem" in instruction:
            address = int(instruction[4:-1])
            floating_address = apply_address_mask(mask, address)
            bin_addresses = populate_masked_address(floating_address)
            for bin_address in bin_addresses:
                dec_address = int("".join(bin_address), 2)
                mem[dec_address] = int(param)
    sum = 0
    for cell in mem.values():
        sum += cell
    return sum
