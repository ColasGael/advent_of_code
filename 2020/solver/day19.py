import itertools
import re


def main(input_lines):
    initial_rules, messages = parse_input(input_lines)

    part1_rules = list(initial_rules)
    part1_root_rule_possibilities = find_possibilities(part1_rules, 0)
    part1_answer = 0
    for message in messages:
        if message in part1_root_rule_possibilities:
            part1_answer += 1

    # part1_rules = [
    #     rule if not is_expanded_rule(initial_rules, rule_id) else rule[0]
    #     for rule_id, rule in enumerate(initial_rules)
    # ]
    # part1_root_rule_pattern = re.compile('^{}$'.format(find_pattern_recursive(part1_rules, 0)))
    # part1_answer = 0
    # for message in messages:
    #     if part1_root_rule_pattern.match(message):
    #         part1_answer += 1
    #         continue

    part2_answer = 0
    for message in messages:
        if part2_is_valid_message(message, part1_rules):
            part2_answer += 1

    return part1_answer, part2_answer


def parse_input(input_lines):
    rules = {}
    messages = []
    is_done_rules = False
    for input_line in input_lines:
        if len(input_line) == 0:
            is_done_rules = True
        if not is_done_rules:
            parse_rule(input_line, rules)
        else:
            messages.append(input_line)
    rules = [rules[rule_id] for rule_id in range(len(rules))]
    return rules, messages


def parse_rule(input_line, rules):
    rule_id, rule_description = input_line.split(":")
    rule_id, rule_description = int(rule_id), rule_description.strip()
    if rule_description.startswith('"'):
        rules[rule_id] = [rule_description[1:-1]]
    else:
        rules[rule_id] = [
            [
                int(child_rule_id)
                for child_rule_id in sub_rule.split(" ")
                if child_rule_id
            ]
            for sub_rule in rule_description.split("|")
        ]


def part2_is_valid_message(message, part1_rules):
    # Updated rules:
    # "8: 42 | 42 8"
    # "11: 42 31 | 42 11 31"
    # "0: 8 11"
    rule_0_pattern = re.compile(
        r"^(?P<rule_42_repetition>({rule_42_pat})+)"
        r"(?P<rule_31_repetition>({rule_31_pat})+)$".format(
            rule_42_pat="|".join(part1_rules[42]),
            rule_31_pat="|".join(part1_rules[31]),
        )
    )
    is_valid = True
    match = rule_0_pattern.match(message)
    if not match:
        is_valid = False
    else:
        n_42 = int(len(match.group("rule_42_repetition")) / len(part1_rules[42][0]))
        n_31 = int(len(match.group("rule_31_repetition")) / len(part1_rules[31][0]))
        is_valid = n_42 > n_31
    return is_valid


def is_expanded_rule(rules, rule_id):
    return isinstance(rules[rule_id][0], str)


def find_possibilities(rules, queried_rule_id):
    parent = [None] * len(rules)
    current_rule_id = queried_rule_id
    while not is_expanded_rule(rules, queried_rule_id):
        if is_expanded_rule(rules, current_rule_id):
            current_rule_id = parent[current_rule_id]
        else:
            is_expanded = True
            expanded_rule = []
            for sub_rule in rules[current_rule_id]:
                children_rules_possibilities = []
                for child_rule_id in sub_rule:
                    if not is_expanded_rule(rules, child_rule_id):
                        is_expanded = False
                        parent[child_rule_id] = current_rule_id
                        current_rule_id = child_rule_id
                        break
                    children_rules_possibilities.append(rules[child_rule_id])
                if not is_expanded:
                    break
                sub_rule_possibilities = [
                    "".join(combination)
                    for combination in itertools.product(*children_rules_possibilities)
                ]
                expanded_rule.extend(sub_rule_possibilities)
            if is_expanded:
                rules[current_rule_id] = expanded_rule
    return rules[queried_rule_id]


def find_possibilities_recursive(rules, rule_id):
    if is_expanded_rule(rules, rule_id):
        expanded_rule = rules[rule_id]
    else:
        expanded_rule = []
        for sub_rule in rules[rule_id]:
            children_rules_possibilities = [
                find_possibilities_recursive(rules, child_rule_id)
                for child_rule_id in sub_rule
            ]
            sub_rule_possibilities = [
                "".join(combination)
                for combination in itertools.product(*children_rules_possibilities)
            ]
            expanded_rule.extend(sub_rule_possibilities)
    rules[rule_id] = expanded_rule
    return expanded_rule


def find_pattern_recursive(rules, rule_id):
    if isinstance(rules[rule_id], str):
        expanded_rule = rules[rule_id]
    else:
        expanded_rule = ""
        for sub_rule in rules[rule_id]:
            sub_rule_pattern = "".join(
                [
                    find_pattern_recursive(rules, child_rule_id)
                    for child_rule_id in sub_rule
                ]
            )
            expanded_rule = expanded_rule + sub_rule_pattern + "|"
        expanded_rule = "(" + expanded_rule[:-1] + ")"
    rules[rule_id] = expanded_rule
    return expanded_rule
