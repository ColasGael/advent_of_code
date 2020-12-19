import re

import intervals
import numpy as np

def main(input_lines):
    rules, my_ticket, other_tickets = parse_input(input_lines)

    part1_answer = 0
    i = 0
    while i < len(other_tickets):
        is_valid_ticket = True
        for value in other_tickets[i]:
            if not is_valid_value(value, rules):
                is_valid_ticket = False
                part1_answer += value
        if not is_valid_ticket:
            other_tickets.pop(i)
        else:
            i += 1

    position_to_field = find_fields_position(rules, other_tickets)
    part2_answer = np.prod([my_ticket[position] for position, field in position_to_field.items() if field.startswith('departure')])

    return part1_answer, part2_answer


def parse_input(input_lines):
    RULE_PATTERN = re.compile("(?P<start>[0-9]+)-(?P<end>[0-9]+)")

    rules = {}
    my_ticket = []
    other_tickets = []

    is_done_rules, is_done_my_ticket = False, False
    for input_line in input_lines:
        if (input_line == "\n") or ('ticket' in input_line):
            is_done_rules = True
            continue

        if not is_done_rules:
            field, valid_ranges_raw = input_line.split(':')
            rules[field] = intervals.empty()
            for start_range, end_range in RULE_PATTERN.findall(valid_ranges_raw):
                valid_interval = intervals.closed(int(start_range), int(end_range))
                rules[field] = rules[field].union(valid_interval)

        elif not is_done_my_ticket:
            my_ticket = [int(value) for value in input_line.split(',')]
            is_done_my_ticket = True

        else:
            other_ticket = [int(value) for value in input_line.split(',')]
            other_tickets.append(other_ticket)

    return rules, my_ticket, other_tickets


def is_valid_value(value, rules):
    for valid_interval in rules.values():
        if value in valid_interval:
            return True
    return False


def find_fields_position(rules, tickets):
    fields = rules.keys()
    position_to_field_hypothesis = np.full((len(tickets[0]), len(fields)), True)
    position_to_field_confirmed = {}

    for ticket in tickets:
        for position, value in enumerate(ticket):
            field_hypothesis = np.where(position_to_field_hypothesis[position, :])[0]
            for field_idx in field_hypothesis.tolist():
                field = fields[field_idx]
                if value not in rules[field]:
                    position_to_field_hypothesis[position, field_idx] = False

    while np.any(position_to_field_hypothesis):
        confirmed_fields = np.where(np.sum(position_to_field_hypothesis, axis=0) == 1)[0]
        for field_idx in confirmed_fields.tolist():
            position = np.where(position_to_field_hypothesis[:, field_idx])[0][0]
            position_to_field_confirmed[position] = fields[field_idx]
            position_to_field_hypothesis[position, :] = False
            position_to_field_hypothesis[:, field_idx] = False

        confirmed_positions = np.where(np.sum(position_to_field_hypothesis, axis=1) == 1)[0]
        for position in confirmed_positions.tolist():
            field_idx = np.where(position_to_field_hypothesis[position, :])[0][0]
            position_to_field_confirmed[position] = fields[field_idx]
            position_to_field_hypothesis[position, :] = False
            position_to_field_hypothesis[:, field_idx] = False

    return position_to_field_confirmed
