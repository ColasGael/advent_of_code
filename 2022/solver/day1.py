from typing import List, Tuple


def main(input_lines: List[str], top_k: int = 3) -> Tuple[int, int]:
    input_lines.append("")
    calories_elves: List[List[int]] = [[]]
    for line in input_lines:
        if len(line) == 0:
            calories_elves.append([])
            continue
        calories_elves[-1].append(int(line))

    part1_answer: int = find_most_calories_elve(calories_elves)
    part2_answer: int = sum(find_most_calories_elves(calories_elves, top_k))
    return part1_answer, part2_answer


def find_most_calories_elve(calories_elves: List[List[int]]) -> int:
    # For the reason behind this ignore, see: https://github.com/python/mypy/issues/6811
    return max(map(sum, calories_elves))  # type: ignore


def find_most_calories_elves(calories_elves: List[List[int]], top_k: int) -> List[int]:
    total_calories_elves: List[int] = list(map(sum, calories_elves))  # type: ignore
    total_calories_elves.sort()
    return total_calories_elves[-top_k:]
