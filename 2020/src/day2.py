import re

from io_utils import read_input_file


def day2_1():
    valid_passwords = []
    passwords_list = read_input_file("day2.txt", input_type=str)
    min_occurrences_regex = re.compile("^\d+-")
    max_occurrences_regex = re.compile("-\d+ ")
    policy_letter_regex = re.compile(" [a-z]+$")
    for line in passwords_list:
        policy, password = line.split(": ")
        min_occurrences = int(min_occurrences_regex.findall(policy)[0][:-1])
        max_occurrences = int(max_occurrences_regex.findall(policy)[0][1:-1])
        policy_letter = str(policy_letter_regex.findall(policy)[0][1:])
        occurrences = 0
        for letter in password:
            if letter == policy_letter:
                occurrences += 1
                if occurrences > max_occurrences:
                    break
        if min_occurrences <= occurrences <= max_occurrences:
            valid_passwords.append(password)

    return len(valid_passwords)


def day2_2():
    valid_passwords = []
    passwords_list = read_input_file("day2.txt", input_type=str)
    first_index_regex = re.compile("^\d+-")
    second_index_regex = re.compile("-\d+ ")
    policy_letter_regex = re.compile(" [a-z]+$")
    for line in passwords_list:
        policy, password = line.split(": ")
        first_index = int(first_index_regex.findall(policy)[0][:-1]) - 1
        second_index = int(second_index_regex.findall(policy)[0][1:-1]) - 1
        policy_letter = str(policy_letter_regex.findall(policy)[0][1:])
        first_position_matches_policy = password[first_index] == policy_letter
        second_position_matches_policy = password[second_index] == policy_letter

        if first_position_matches_policy != second_position_matches_policy:
            valid_passwords.append(password)

    return len(valid_passwords)
