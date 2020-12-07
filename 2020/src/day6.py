from typing import List, Set

from io_utils import read_input_file


def day6_1():
    input_list = read_input_file("day6.txt", input_type=str)
    answers = get_all_yes_answers_per_group(input_list)
    amount_yes_answers = 0
    for answers_per_group in answers:
        amount_yes_answers += len(answers_per_group)
    return amount_yes_answers


def get_all_yes_answers_per_group(input_list):
    answers: List[Set[str]] = []
    i = 0
    for line in input_list:
        if line == "\n":
            i += 1
        else:
            if i == len(answers):
                answers.append(set())
            line = line.strip()
            for char in line:
                answers[i].add(char)
    return answers


def get_common_yes_answers_per_group(input_list):
    answers: List[Set[str]] = []
    i = 0
    for line in input_list:
        if line == "\n":
            i += 1
        else:
            line = line.strip()
            if i == len(answers):
                answers.append(set(line))
            else:
                answers[i] = answers[i].intersection(line)
    return answers


def day6_2():
    input_list = read_input_file("day6.txt", input_type=str)
    answers = get_common_yes_answers_per_group(input_list)
    amount_yes_answers = 0
    for answers_per_group in answers:
        amount_yes_answers += len(answers_per_group)
    return amount_yes_answers
