import re


INSTRUCTION_PATTERN = re.compile(
    r"(?P<operation>[a-z][a-z][a-z]) (?P<argument>[+-]\d+)"
)


def main(input_lines):
    instructions = []
    for line in input_lines:
        match = INSTRUCTION_PATTERN.match(line)
        instructions.append((match.group("operation"), int(match.group("argument"))))

    part1_answer = check_infinite_loop(instructions)[1]
    part2_answer = check_infinite_loop(fix_infinite_loop(instructions))[1]
    return part1_answer, part2_answer


def execute_instruction(operation, argument, i, acc):
    if operation == "nop":
        i += 1
    elif operation == "acc":
        acc += argument
        i += 1
    elif operation == "jmp":
        i += argument
    else:
        raise RuntimeError("Operation {} not supported!".format(operation))
    return i, acc


def check_infinite_loop(instructions, i=0, acc=0, is_visited_before=None):
    if is_visited_before is not None:
        is_visited = list(is_visited_before)
    else:
        is_visited = [False] * len(instructions)

    while 0 <= i < len(instructions):
        if is_visited[i]:
            break
        is_visited[i] = True
        operation, argument = instructions[i]
        i, acc = execute_instruction(operation, argument, i, acc)

    return i, acc


def fix_infinite_loop(instructions):
    i, acc = 0, 0
    is_visited = [False] * len(instructions)

    while 0 <= i < len(instructions):
        operation, argument = instructions[i]
        if operation == "acc":
            is_visited[i] = True
            i, acc = execute_instruction(operation, argument, i, acc)
            continue
        if operation == "nop":
            new_operation = "jmp"
        elif operation == "jmp":
            new_operation = "nop"
        instructions[i] = (new_operation, argument)

        j, _acc = check_infinite_loop(
            instructions, i=i, acc=acc, is_visited_before=is_visited
        )

        if j == len(instructions):
            return instructions

        instructions[i] = (operation, argument)
        is_visited[i] = True
        i, acc = execute_instruction(operation, argument, i, acc)

    raise RuntimeError("Cannot fix the infinite loop in: {}.".format(instructions))
