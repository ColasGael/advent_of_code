import re
from typing import Any, Dict, List, Tuple


Monkey = Dict[str, Any]

OPERATION_PATTERN = re.compile(
    r"^\s*Operation: new = old (?P<operator>[\+\*]) (?P<value>(\d+|old))$"
)


def main(input_lines: List[str]) -> Tuple[int, int]:
    input_lines.append("")

    monkeys: List[Monkey] = parse_input(input_lines)

    part1_answer: int = get_monkey_business(monkeys, 3, 20)

    # Reset the inspection counts
    # Remark: no need to reset the items as part 1 and part 2 use independent items' representations
    for monkey in monkeys:
        monkey["inspect_count"] = 0

    part2_answer: int = get_monkey_business(monkeys, 1, 10000)

    return part1_answer, part2_answer


def parse_input(input_lines: List[str]) -> List[Monkey]:
    monkeys: List[Monkey] = []
    # Store the common multiple of all the divisible tests' values
    prod_div_test_values = 1
    prev_newline_idx = -1
    for i, input_line in enumerate(input_lines):
        if input_line == "":
            monkeys.append(init_monkey(input_lines[prev_newline_idx + 1 : i]))
            prod_div_test_values *= monkeys[-1]["div_test_value"]
            prev_newline_idx = i
    for monkey in monkeys:
        monkey["prod_div_test_values"] = prod_div_test_values
    return monkeys


def init_monkey(monkey_lines: List[str]) -> Monkey:
    assert len(monkey_lines) == 6
    # Extract the list of items the monkey is holding
    all_items = monkey_lines[1].split(":")[-1]
    items = [int(item) for item in all_items.split(",")]

    # Extract the worry-update operation
    match = OPERATION_PATTERN.match(monkey_lines[2])
    if not match:
        raise RuntimeError(f"Cannot parse operation {monkey_lines[2]}")
    operator = match.group("operator")
    value = match.group("value")
    if value == "old":
        operator = "**2"
    # pylint: disable=unnecessary-lambda-assignment
    if operator == "+":
        update_func = lambda worry_lvl: worry_lvl + int(value)
    elif operator == "*":
        update_func = lambda worry_lvl: worry_lvl * int(value)
    elif operator == "**2":
        update_func = lambda worry_lvl: worry_lvl**2
    else:
        raise RuntimeError(f"Unsupported update operator {operator}")
    # pylint: enable=unnecessary-lambda-assignment

    # Extract the test value
    div_test_value = int(monkey_lines[3].split(" ")[-1])

    # Extract the transition
    true_monkey = int(monkey_lines[4].split(" ")[-1])
    false_monkey = int(monkey_lines[5].split(" ")[-1])

    # Initialize the monkey
    monkey: Monkey = {
        "part1_items": list(items),
        "part2_items": list(items),
        "update_func": update_func,
        "div_test_value": div_test_value,
        "true_monkey": true_monkey,
        "false_monkey": false_monkey,
        "inspect_count": 0,
    }
    return monkey


def part1_round(monkeys: List[Monkey], worry_lvl_div: int) -> None:
    for monkey in monkeys:
        div_test_value = monkey["div_test_value"]
        while monkey["part1_items"]:
            item = monkey["part1_items"].pop()
            item = monkey["update_func"](item) // worry_lvl_div
            new_monkey_idx = (
                monkey["true_monkey"]
                if item % div_test_value == 0
                else monkey["false_monkey"]
            )
            monkeys[new_monkey_idx]["part1_items"].append(item)
            monkey["inspect_count"] += 1


def part2_round(monkeys: List[Monkey]) -> None:
    prod_div_test_values = monkeys[0]["prod_div_test_values"]

    for monkey in monkeys:
        div_test_value = monkey["div_test_value"]
        while monkey["part2_items"]:
            item = monkey["part2_items"].pop()
            item = monkey["update_func"](item) % prod_div_test_values
            new_monkey_idx = (
                monkey["true_monkey"]
                if item % div_test_value == 0
                else monkey["false_monkey"]
            )
            monkeys[new_monkey_idx]["part2_items"].append(item)
            monkey["inspect_count"] += 1


def get_monkey_business(
    monkeys: List[Monkey], worry_lvl_div: int, n_rounds: int
) -> int:
    for _i in range(n_rounds):
        if worry_lvl_div != 1:
            part1_round(monkeys, worry_lvl_div)
        else:
            part2_round(monkeys)

    most_active_monkey_counts = [0, 0]
    for monkey in monkeys:
        inspect_count = monkey["inspect_count"]
        if inspect_count >= most_active_monkey_counts[0]:
            most_active_monkey_counts = [inspect_count, most_active_monkey_counts[0]]
        elif inspect_count >= most_active_monkey_counts[1]:
            most_active_monkey_counts = [most_active_monkey_counts[0], inspect_count]

    return most_active_monkey_counts[0] * most_active_monkey_counts[1]
