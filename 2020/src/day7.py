import re

from io_utils import read_input_file


def extract_reversed_rules(input_list):
    reversed_rules = {}
    for line in input_list:
        line = line.strip()
        rule_subject, rule_objects = line.split(" bags contain ")
        rule_objects = re.compile(" bags*[\.,] *").split(rule_objects)
        for rule_object in rule_objects:
            if len(rule_object) == 0 or "no other" in rule_object:
                continue
            colour = re.compile("\d ").split(rule_object)[1]
            if colour not in reversed_rules:
                reversed_rules[colour] = []
            reversed_rules[colour].append(rule_subject)
    return reversed_rules


def get_encapsulating_bags(colour, reversed_rules):
    if colour not in reversed_rules:
        return set()
    encapsulating_bags = set(reversed_rules[colour])
    for encapsulating_bag in encapsulating_bags:
        encapsulating_bags = encapsulating_bags.union(get_encapsulating_bags(encapsulating_bag, reversed_rules))
    return encapsulating_bags


def day7_1():
    input_list = read_input_file("day7.txt", input_type=str)
    reversed_rules = extract_reversed_rules(input_list)
    bags = get_encapsulating_bags(colour="shiny gold", reversed_rules=reversed_rules)
    return len(bags)


def extract_rules_with_amount(input_list):
    rules = {}
    for line in input_list:
        line = line.strip()
        rule_subject, rule_objects = line.split(" bags contain ")
        rule_objects = re.compile(" bags*[\.,] *").split(rule_objects)
        for rule_object in rule_objects:
            if len(rule_object) == 0 or "no other" in rule_object:
                continue
            colour = re.compile("\d ").split(rule_object)[1]
            amount = re.compile(" \S").split(rule_object)[0]
            if rule_subject not in rules:
                rules[rule_subject] = []
            rules[rule_subject].append((colour, int(amount)))
    return rules


def get_encapsulated_bags_amount(colour, rules):
    if colour not in rules:
        return 0
    amount = 0
    encapsulated_bags = rules[colour]
    for encapsulated_bag in encapsulated_bags:
        bag_colour = encapsulated_bag[0]
        bags_amount = encapsulated_bag[1]
        amount += bags_amount
        amount += bags_amount * get_encapsulated_bags_amount(bag_colour, rules)
    return amount


def day7_2():
    input_list = read_input_file("day7.txt", input_type=str)
    rules = extract_rules_with_amount(input_list)
    final_amount = get_encapsulated_bags_amount(colour="shiny gold", rules=rules)
    return final_amount
