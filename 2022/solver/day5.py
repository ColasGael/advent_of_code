import re
from typing import Callable, List, Tuple


MOVE_PATTERN = re.compile(
    r"move\s*(?P<num_stacks>\d+)\s*from\s*(?P<start_idx>\d+)\s*to\s*(?P<end_idx>\d+)\s*"
)


def main(input_lines: List[str]) -> Tuple[str, str]:
    part1_stacks, actions = parse_input(input_lines)
    part2_stacks = [list(crate) for crate in part1_stacks]

    part1_answer: str = find_top_stacks(part1_stacks, actions, part1_execute_action)
    part2_answer: str = find_top_stacks(part2_stacks, actions, part2_execute_action)

    return part1_answer, part2_answer


def parse_input(
    input_lines: List[str],
) -> Tuple[List[List[str]], List[Tuple[int, Tuple[int, int]]]]:
    stacks: List[List[str]] = []
    actions: List[Tuple[int, Tuple[int, int]]] = []

    completed_parsing_stacks: bool = False
    for input_line in input_lines:
        if len(input_line) == 0:
            completed_parsing_stacks = True
            continue

        if not completed_parsing_stacks:
            for stack_idx, crate in enumerate(input_line[1::4]):
                if crate.isdigit():
                    # Skip the input line: it's the stacks numbering
                    break
                if stack_idx >= len(stacks):
                    stacks.append([])
                if crate == " ":
                    assert (
                        len(stacks[stack_idx]) == 0
                    ), f"stacks hanging in the air for stack {stack_idx}!"
                    continue
                assert crate.isalpha(), f"Crate '{crate}' is not a letter"
                stacks[stack_idx].append(crate)

        else:
            match = MOVE_PATTERN.match(input_line)
            if not match:
                raise RuntimeError(f"Could not parse input line: {input_line}")
            # Handles Python 0-indexing
            actions.append(
                (
                    int(match.group("num_stacks")),
                    (
                        int(match.group("start_idx")) - 1,
                        int(match.group("end_idx")) - 1,
                    ),
                )
            )

    # Re-order the stacks from bottom to top
    for stack in stacks:
        stack.reverse()

    return stacks, actions


ExecuteActionFunc = Callable[[List[List[str]], Tuple[int, Tuple[int, int]]], None]


def part1_execute_action(
    stacks: List[List[str]], action: Tuple[int, Tuple[int, int]]
) -> None:
    num_stacks: int
    start_idx: int
    end_idx: int
    num_stacks, (start_idx, end_idx) = action

    assert (
        len(stacks[start_idx]) >= num_stacks
    ), f"Cannot remove {num_stacks} crate from stack {start_idx}, with len {len(stacks[start_idx])}"

    for _i in range(num_stacks):
        stacks[end_idx].append(stacks[start_idx].pop())


def part2_execute_action(
    stacks: List[List[str]], action: Tuple[int, Tuple[int, int]]
) -> None:
    num_stacks: int
    start_idx: int
    end_idx: int
    num_stacks, (start_idx, end_idx) = action

    assert (
        len(stacks[start_idx]) >= num_stacks
    ), f"Cannot remove {num_stacks} crate from stack {start_idx}, with len {len(stacks[start_idx])}"

    stacks[end_idx].extend(stacks[start_idx][-num_stacks:])
    del stacks[start_idx][-num_stacks:]


def find_top_stacks(
    stacks: List[List[str]],
    actions: List[Tuple[int, Tuple[int, int]]],
    execute_action: Callable,
) -> str:
    for action in actions:
        execute_action(stacks, action)

    top_stacks: str = "".join(map(lambda stacks: stacks[-1] if stacks else "", stacks))
    return top_stacks
