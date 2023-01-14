from collections import defaultdict
from typing import Dict, List, Tuple


Coord = Tuple[int, int]


# Directions in which the elves can move (order matters here)
DIRECTIONS: Tuple[Coord, Coord, Coord, Coord] = (
    (-1, 0),  # N
    (+1, 0),  # S
    (0, -1),  # W
    (0, +1),  # E
)


def main(input_lines: List[str], part1_n_rounds: int = 10) -> Tuple[int, int]:
    positions: List[Coord] = parse_positions(input_lines)

    update_positions(positions, part1_n_rounds)
    part1_answer: int = compute_coverage(positions)

    part2_answer: int = converge(positions, part1_n_rounds)

    return part1_answer, part2_answer


def parse_positions(
    input_lines: List[str], elf_char="#", empty_char="."
) -> List[Coord]:
    positions: List[Coord] = []
    for i, input_line in enumerate(input_lines):
        for j, char in enumerate(input_line):
            if char == elf_char:
                positions.append((i, j))
            elif char != empty_char:
                raise RuntimeError(f"Unrecognized char in input: {char}")
    return positions


def update_positions(positions: List[Coord], n_rounds: int) -> None:
    for round_idx in range(n_rounds):
        step(round_idx, positions)


def converge(positions: List[Coord], start_round_idx: int = 0) -> int:
    round_idx = start_round_idx
    while step(round_idx, positions):
        round_idx += 1
    return round_idx + 1


def step(  # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    round_idx: int, positions: List[Coord]
) -> bool:
    # Sort the positions to make it easy to find an elf's neighbors
    positions.sort(key=sum)

    # Initialization
    # key: proposed position, value: idx of the elves that want to move there
    proposed_positions: Dict[Coord, List[int]] = defaultdict(list)

    # Part 1: Check where the elves want to move
    for elf_idx, position in enumerate(positions):
        key = sum(position)

        # In the same order as the DIRECTIONS
        can_move: List[bool] = [True] * len(DIRECTIONS)
        for other_elf_idx in range(elf_idx - 1, -1, -1):
            # Already know the elf cannot move, no need to process further
            if not any(can_move):
                break
            other_position = positions[other_elf_idx]
            # All the other elves will be too far, no need to process further
            if key - sum(other_position) > 2:
                break
            # The other elf is too far, it is not a neighbor
            if abs(other_position[0] - position[0]) > 1:
                continue
            if abs(other_position[1] - position[1]) > 1:
                continue
            # Check whether the other elf is blocking a direction
            if other_position[0] == position[0] - 1:
                can_move[0] = False
            elif other_position[0] == position[0] + 1:
                can_move[1] = False
            if other_position[1] == position[1] - 1:
                can_move[2] = False
            elif other_position[1] == position[1] + 1:
                can_move[3] = False
        for other_position in positions[elf_idx + 1 :]:
            # Already know the elf cannot move, no need to process further
            if not any(can_move):
                break
            # All the other elves will be too far, no need to process further
            if sum(other_position) - key > 2:
                break
            # The other elf is too far, it is not a neighbor
            if abs(other_position[0] - position[0]) > 1:
                continue
            if abs(other_position[1] - position[1]) > 1:
                continue
            # Check whether the other elf is blocking a direction
            if other_position[0] == position[0] - 1:
                can_move[0] = False
            elif other_position[0] == position[0] + 1:
                can_move[1] = False
            if other_position[1] == position[1] - 1:
                can_move[2] = False
            elif other_position[1] == position[1] + 1:
                can_move[3] = False

        if not any(can_move) or all(can_move):
            continue

        for k in range(len(DIRECTIONS)):
            direction_idx = (round_idx + k) % len(DIRECTIONS)
            if can_move[direction_idx]:
                direction = DIRECTIONS[direction_idx]
                # No neighbor: move in that direction
                new_position = (position[0] + direction[0], position[1] + direction[1])
                proposed_positions[new_position].append(elf_idx)
                break

    # Part 2: Update all the elves' positions
    is_updated = False
    for proposed_position, elves_idxs in proposed_positions.items():
        if len(elves_idxs) > 1:
            # More than 1 elf want to move there, no elves should move
            continue
        positions[elves_idxs[0]] = proposed_position
        is_updated = True

    return is_updated


def compute_coverage(positions: List[Coord]) -> int:
    min_row_idx, min_col_idx = positions[0]
    max_row_idx, max_col_idx = positions[0]
    for position in positions:
        row_idx, col_idx = position
        min_row_idx = min(min_row_idx, row_idx)
        max_row_idx = max(max_row_idx, row_idx)
        min_col_idx = min(min_col_idx, col_idx)
        max_col_idx = max(max_col_idx, col_idx)
    rectangle_area: int = (max_row_idx - min_row_idx + 1) * (
        max_col_idx - min_col_idx + 1
    )
    coverage: int = rectangle_area - len(positions)
    return coverage
