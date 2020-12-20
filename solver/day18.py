import re


def main(input_lines):
    part1_answer = sum([compute(input_line.strip(), part1_compute_wo_parenthesis) for input_line in input_lines])
    part2_answer = sum([compute(input_line.strip(), part2_compute_wo_parenthesis) for input_line in input_lines])

    return part1_answer, part2_answer


def compute(equation, compute_wo_parenthesis_method):
    INNER_PARENTHESIS_PATTERN = re.compile("\([\d\+\*\s]+\)")
    while True:
        inner_parenthesis_groups = INNER_PARENTHESIS_PATTERN.findall(equation)
        if not inner_parenthesis_groups:
            break
        for inner_parenthesis_group in inner_parenthesis_groups:
            group_result = compute_wo_parenthesis_method(inner_parenthesis_group[1:-1])
            equation = re.sub(re.escape(inner_parenthesis_group), str(group_result), equation)
    return compute_wo_parenthesis_method(equation)


def part1_compute_wo_parenthesis(equation):
    result, operator = None, None
    for char in equation.split(' '):
        if result is None:
            result = int(char)
        elif char in ('+', '*'):
            operator = char
        elif operator == '+':
            result += int(char)
        elif operator == '*':
            result *= int(char)
    return result


def part2_compute_wo_parenthesis(equation):
    ADDITION_PATTERN = re.compile("(?P<right_int>\d+) \+ (?P<left_int>\d+)")
    while True:
        m = ADDITION_PATTERN.search(equation)
        if not m:
            break
        addition_result = int(m.group('right_int')) + int(m.group('left_int'))
        equation = equation.replace(m.group(0), str(addition_result), 1)
    return part1_compute_wo_parenthesis(equation)

