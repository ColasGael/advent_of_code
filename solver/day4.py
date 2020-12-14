import re

import numpy as np


def main(input_lines):
    PASSPORT_ENTRY_PATTERN = re.compile("(?P<field>[a-z]+):(?P<value>[a-z0-9#]+)")

    passports = [{}]
    for line in input_lines:
        passport_entries = PASSPORT_ENTRY_PATTERN.findall(line)
        # Start a new passport
        if not passport_entries:
            passports.append({})
        else:
            passports[-1].update({
                field: entry for (field, entry) in passport_entries
            })

    REQUIRED_FIELDS = {
        'byr': lambda entry: 1920 <= int(entry) <= 2002,
        'iyr': lambda entry: 2010 <= int(entry) <= 2020,
        'eyr': lambda entry: 2020 <= int(entry) <= 2030,
        'hgt': lambda entry: ((150 <= int(entry[:-2]) <= 193) and (entry[-2:] == 'cm')) or ((59 <= int(entry[:-2]) <= 76) and (entry[-2:] == 'in')),
        'hcl': lambda entry: (len(entry) == 7) and (entry[0] == '#') and np.all([char in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'] for char in entry[1:]]),
        'ecl': lambda entry: entry in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'pid': lambda entry: (len(entry) == 9) and isinstance(int(entry), int),
    }
    OPTIONAL_FIELDS = ['cid']

    part1_n_valid_passport = 0
    part2_n_valid_passport = 0
    for passport in passports:
        if is_valid_passport_fields(passport, REQUIRED_FIELDS.keys(), OPTIONAL_FIELDS):
            part1_n_valid_passport += 1
        if is_valid_passport_data(passport, REQUIRED_FIELDS, OPTIONAL_FIELDS):
            part2_n_valid_passport += 1

    return part1_n_valid_passport, part2_n_valid_passport


def is_valid_passport_fields(passport, required_fields, optional_fields):
    for required_field in required_fields:
        if required_field not in passport:
            return False
    return True


def is_valid_passport_data(passport, required_fields, optional_fields):
    for required_field, data_validation_rule in required_fields.items():
        is_valid_passport = False
        if (required_field not in passport) or not data_validation_rule(passport[required_field]):
            return False
    return True
