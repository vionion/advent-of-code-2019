import re
from typing import List, Dict

from io_utils import read_input_file

REQUIRED_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
ALLOWED_EYE_COLOURS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
COLOUR_HEX_REGEXP = re.compile("^#[a-f0-9]{6}$")


def is_valid_passport(passport):
    for field in REQUIRED_FIELDS:
        if field not in passport.keys():
            return False
    return True


def is_valid_passport_strict(passport):
    for field in REQUIRED_FIELDS:
        if field not in passport.keys():
            return False
        try:
            if field == "byr" and not (1920 <= int(passport[field]) <= 2002):
                return False
            if field == "iyr" and not (2010 <= int(passport[field]) <= 2020):
                return False
            if field == "eyr" and not (2020 <= int(passport[field]) <= 2030):
                return False
            if field == "hgt":
                if passport[field][-2:] in ["in", "cm"]:
                    if passport[field][-2:] == "cm" and not (150 <= int(passport[field][:-2]) <= 193):
                        return False
                    if passport[field][-2:] == "in" and not (59 <= int(passport[field][:-2]) <= 76):
                        return False
                else:
                    return False
            if field == "hcl" and not (COLOUR_HEX_REGEXP.match(passport[field])):
                return False
            if field == "ecl" and passport[field] not in ALLOWED_EYE_COLOURS:
                return False
            if field == "pid" and not (len(passport[field]) == 9 and int(passport[field])):
                return False
        except TypeError:
            return False

    return True


def day4_1():
    input_list = read_input_file("day4.txt", input_type=str)
    passports = get_passports(input_list)
    valid_passports = []
    for passport in passports:
        if is_valid_passport(passport):
            valid_passports.append(passport)

    return len(valid_passports)


def get_passports(input_list):
    passports: List[Dict[str, str]] = []
    i = 0
    for line in input_list:
        if line == "\n":
            i += 1
        else:
            if i == len(passports):
                passports.append({})
            line = line.strip()
            fields_list = line.split(" ")
            for fields_pair in fields_list:
                passports[i][fields_pair.split(":")[0]] = fields_pair.split(":")[1]
    return passports


def day4_2():
    input_list = read_input_file("day4.txt", input_type=str)
    passports = get_passports(input_list)
    valid_passports = []
    for passport in passports:
        if is_valid_passport_strict(passport):
            valid_passports.append(passport)

    return len(valid_passports)
