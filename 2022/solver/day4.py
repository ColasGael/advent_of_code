from typing import Callable, List, Tuple


def main(input_lines: List[str]) -> Tuple[int, int]:
    cleaning_range_pairs: List[List[Tuple[int, int]]] = []
    for line in input_lines:
        cleaning_ranges: List[str] = line.split(",")
        assert len(cleaning_ranges) == 2
        cleaning_range_pair: List[Tuple[int, int]] = []
        for cleaning_range in cleaning_ranges:
            start_range, end_range = cleaning_range.split("-")
            cleaning_range_pair.append((int(start_range), int(end_range)))
        cleaning_range_pairs.append(cleaning_range_pair)
    part1_answer: int = solve(cleaning_range_pairs, fully_contains)
    part2_answer: int = solve(cleaning_range_pairs, overlaps)
    return part1_answer, part2_answer


def fully_contains(range_1: Tuple[int, int], range_2: Tuple[int, int]) -> bool:
    if range_2[0] < range_1[0] or range_2[1] > range_1[1]:
        range_1, range_2 = range_2, range_1
    return range_1[0] <= range_2[0] and range_2[1] <= range_1[1]


def overlaps(range_1: Tuple[int, int], range_2: Tuple[int, int]) -> bool:
    if range_2[0] < range_1[0]:
        range_1, range_2 = range_2, range_1
    return range_2[0] <= range_1[1]


RangeComparisonFunc = Callable[[Tuple[int, int], Tuple[int, int]], bool]


def solve(
    cleaning_range_pairs: List[List[Tuple[int, int]]], func: RangeComparisonFunc
) -> int:
    return sum(map(lambda ranges: func(*ranges), cleaning_range_pairs))
