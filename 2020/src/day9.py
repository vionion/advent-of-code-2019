from io_utils import read_input_file


def can_be_constructed(available_vals, next_value):
    for first_val in available_vals:
        second_val = next_value - first_val
        if second_val in available_vals:
            return True
    return False


def find_xmas_protocol_mistake(preamble, vals):
    available_vals = vals[0:preamble]
    for next_value in vals[preamble:]:
        if not can_be_constructed(available_vals, next_value):
            return next_value
        else:
            available_vals.pop(0)
            available_vals.append(next_value)
    return None


def day9_1():
    input_list = read_input_file("day9.txt", input_type=int)
    divergent_value = find_xmas_protocol_mistake(preamble=25, vals=input_list)
    return divergent_value


def get_contiguous_set(vals, target):
    i = 0
    k = 1
    set_candidate = [vals[0]]
    sum = vals[0]
    while i < len(vals):
        set_candidate.append(vals[i + k])
        sum += vals[i+k]
        if sum == target:
            return set_candidate
        if sum > target:
            i += 1
            set_candidate = [vals[i]]
            sum = vals[i]
            k = 1
            continue
        k += 1
    pass


def day9_2():
    input_list = read_input_file("day9.txt", input_type=int)
    divergent_value = find_xmas_protocol_mistake(preamble=25, vals=input_list)
    contiguous_set = get_contiguous_set(vals=input_list, target=divergent_value)
    contiguous_set.sort()
    encryption_weakness = contiguous_set[0] + contiguous_set[-1]
    return encryption_weakness
