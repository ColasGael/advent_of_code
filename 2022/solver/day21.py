# Safe to use 'eval' here as we control what we feed it
# pylint: disable=eval-used

import re
from typing import cast, Dict, List, Tuple, Union


Monkey = str
DependentMonkeyJob = Tuple[Monkey, str, Monkey]
MonkeyJob = Union[int, DependentMonkeyJob]


MONKEY_JOB_PATTERN = re.compile(
    r"^(?P<parent_monkey>\w+): ("
    r"(?P<number>\d+)|"
    r"(?P<child_monkey_1>\w+) (?P<operation>[\+\-\*\/]) (?P<child_monkey_2>\w+))$"
)


def main(
    input_lines: List[str], monkey_root: str = "root", you: str = "humn"
) -> Tuple[int, int]:
    monkey_jobs: Dict[Monkey, MonkeyJob] = parse_monkey_jobs(input_lines)

    part1_answer: int = find_root_monkey_number(monkey_root, monkey_jobs, {})
    part2_answer: int = find_your_number(monkey_root, you, monkey_jobs)

    return part1_answer, part2_answer


def parse_monkey_jobs(input_lines: List[str]) -> Dict[Monkey, MonkeyJob]:
    monkey_jobs: Dict[Monkey, MonkeyJob] = {}
    for input_line in input_lines:
        match = MONKEY_JOB_PATTERN.match(input_line)
        if match is None:
            raise RuntimeError(f"Failed to parse line: {input_line}")
        monkey = match.group("parent_monkey")
        assert monkey not in monkey_jobs, f"Monkey {monkey} has several jobs"
        if match.group("number") is not None:
            monkey_jobs[monkey] = int(match.group("number"))
        else:
            monkey_jobs[monkey] = (
                match.group("child_monkey_1"),
                match.group("operation"),
                match.group("child_monkey_2"),
            )
    return monkey_jobs


def find_root_monkey_number(
    monkey_root: str,
    monkey_jobs: Dict[Monkey, MonkeyJob],
    monkey_numbers: Dict[Monkey, int],
) -> int:
    def dfs(monkey) -> int:
        if monkey in monkey_numbers:
            return monkey_numbers[monkey]

        monkey_job = monkey_jobs.get(monkey)
        if monkey_job is None:
            raise RuntimeError(f"Unspecified job for monkey {monkey}")

        monkey_number: int
        if isinstance(monkey_job, int):
            monkey_number = monkey_job
        else:
            child_monkey_1, operation, child_monkey_2 = monkey_job
            child_monkey_1_number: int = dfs(child_monkey_1)
            child_monkey_2_number: int = dfs(child_monkey_2)
            # Remark: Can use 'eval' here as the regex restricts the possible values of 'operation'
            monkey_number = int(
                eval(f"{child_monkey_1_number} {operation} {child_monkey_2_number}")
            )

        # Cache the result
        monkey_numbers[monkey] = monkey_number
        return monkey_number

    return dfs(monkey_root)


def find_your_number(
    monkey_root: str, you: str, monkey_jobs: Dict[Monkey, MonkeyJob]
) -> int:
    # Pop your incorrect job
    monkey_jobs.pop(you)

    # Shared monkey numbers
    monkey_numbers: Dict[Monkey, int] = {
        monkey: monkey_job
        for monkey, monkey_job in monkey_jobs.items()
        if isinstance(monkey_job, int)
    }

    # Update the incorrect operation
    child_monkey_1, _operation, child_monkey_2 = cast(
        DependentMonkeyJob, monkey_jobs[monkey_root]
    )

    # Only 1 of the 2 child monkeys should depend on your number
    # Otherwise there is no unique solution
    try:
        monkey_numbers[child_monkey_2] = find_root_monkey_number(
            child_monkey_1, monkey_jobs, monkey_numbers=monkey_numbers
        )
    except RuntimeError:
        monkey_numbers[child_monkey_1] = find_root_monkey_number(
            child_monkey_2, monkey_jobs, monkey_numbers=monkey_numbers
        )

    open_monkeys: List[Monkey] = []

    while you not in monkey_numbers:
        if len(open_monkeys) == 0:
            # Check if we are able to set any new monkey
            for parent_monkey, monkey_job in monkey_jobs.items():
                if parent_monkey in monkey_numbers:
                    # The parent monkey is already set
                    continue
                child_monkey_1, operation, child_monkey_2 = cast(
                    DependentMonkeyJob, monkey_job
                )
                if (
                    child_monkey_1 not in monkey_numbers
                    or child_monkey_2 not in monkey_numbers
                ):
                    continue

                child_monkey_1_number: int = monkey_numbers[child_monkey_1]
                child_monkey_2_number: int = monkey_numbers[child_monkey_2]
                monkey_numbers[parent_monkey] = int(
                    eval(f"{child_monkey_1_number} {operation} {child_monkey_2_number}")
                )
                open_monkeys.append(parent_monkey)

        if len(open_monkeys) == 0:
            open_monkeys = list(monkey_numbers.keys())

        current_monkey: Monkey = open_monkeys.pop()
        current_monkey_number: int = monkey_numbers[current_monkey]

        monkey_job = monkey_jobs[current_monkey]
        if isinstance(monkey_job, int):
            continue

        child_monkey_1, operation, child_monkey_2 = monkey_job
        # Both children are not set cannot determine their numbers
        if (
            child_monkey_1 not in monkey_numbers
            and child_monkey_2 not in monkey_numbers
        ):
            continue
        # Both children are already set
        if child_monkey_1 in monkey_numbers and child_monkey_2 in monkey_numbers:
            continue

        this_monkey: str = child_monkey_1
        other_monkey: str = child_monkey_2
        is_left: bool = False
        if child_monkey_2 in monkey_numbers:
            this_monkey = child_monkey_2
            other_monkey = child_monkey_1
            is_left = True

        this_monkey_number = monkey_numbers[this_monkey]
        # Deduce the other monkey number
        if operation in ("-", "/") and not is_left:
            monkey_numbers[other_monkey] = int(
                eval(f"{this_monkey_number} {operation} {current_monkey_number}")
            )
        else:
            reversed_operation = reverse_operation(operation)
            # Remark: Can use 'eval' here as the we know the possible outputs of 'reverse_op'
            monkey_numbers[other_monkey] = int(
                eval(
                    f"{current_monkey_number} {reversed_operation} {this_monkey_number}"
                )
            )

        open_monkeys.append(other_monkey)

    # Should not happen
    return monkey_numbers[you]


def reverse_operation(operation: str) -> str:
    if operation == "+":
        return "-"
    if operation == "*":
        return "/"
    if operation == "-":
        return "+"
    if operation == "/":
        return "*"
    raise RuntimeError(f"Unsupported operation: {operation}")
