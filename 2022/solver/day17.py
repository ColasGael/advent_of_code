from typing import Dict, List, Set, Tuple


ROCK_TYPES_FILEPATH = "2022/data/day17.txt"

Square = Tuple[int, int]
RockSquares = Set[Square]


def main(
    input_lines: List[str],
    part1_max_num_rocks: int = 2022,
    part2_max_num_rocks: int = 1000000000000,
) -> Tuple[int, int]:
    rock_types: List[RockSquares] = load_rock_types(ROCK_TYPES_FILEPATH)

    assert (
        len(input_lines) == 1
    ), f"Jet pattern should be specified on a single line, got {len(input_lines)} lines"

    jet_pattern: List[int] = get_jet_pattern(input_lines[0])

    part1_answer: int = solve(rock_types, jet_pattern, part1_max_num_rocks)
    part2_answer: int = solve(rock_types, jet_pattern, part2_max_num_rocks)

    return part1_answer, part2_answer


def load_rock_types(input_path: str, rock_char: str = "#") -> List[RockSquares]:
    with open(input_path, "r") as input_file:  # pylint: disable=unspecified-encoding
        input_lines = input_file.read().splitlines()

    rock_types: List[RockSquares] = [set()]
    row_idx = 0
    for input_line in reversed(input_lines):
        if len(input_line) == 0:
            rock_types.append(set())
            row_idx = 0
            continue

        for col_idx, char in enumerate(input_line):
            if char == rock_char:
                rock_types[-1].add((row_idx, col_idx))
        row_idx += 1

    rock_types.reverse()
    return rock_types


def get_jet_pattern(
    input_line: str, left_char: str = "<", right_char: str = ">"
) -> List[int]:
    jet_pattern: List[int] = []
    for char in input_line:
        if char == left_char:
            jet_pattern.append(-1)
        elif char == right_char:
            jet_pattern.append(+1)
        else:
            raise RuntimeError(f"Unrecognized jet pattern character: {char}")
    return jet_pattern


def solve(  # pylint: disable=too-many-locals
    rock_types: List[RockSquares],
    jet_pattern: List[int],
    max_num_rocks: int,
    chamber_width: int = 7,
) -> int:
    # Initialization
    # squares constituting the floor
    floor_squares: RockSquares = set((0, i) for i in range(chamber_width))
    # maximum height of a floor square
    max_floor_height: int = 0
    # no need to consider a floor square below this height
    min_floor_height: int = 0

    # Try to find a recurring sequence of rock positions
    # From the first rock type
    # key: index of the first jet to apply to the block
    # value: (number of rocks that fell before this one, floor squares to consider)
    first_rock_sequence_finder: Dict[int, Tuple[int, RockSquares]] = {}

    num_rocks: int = 0
    jet_pattern_idx: int = 0
    while num_rocks < max_num_rocks:
        rock_idx: int = num_rocks % len(rock_types)

        # Remark: Arbitrary choice to use the first rock type
        if rock_idx == 0:
            if jet_pattern_idx in first_rock_sequence_finder:
                # What was the state the previous time we encountered that jet on the first rock?
                prev_num_rocks, prev_floor_squares = first_rock_sequence_finder[
                    jet_pattern_idx
                ]
                prev_floor_height = max(
                    row_idx for row_idx, _col_idx in prev_floor_squares
                )

                # Check wheter we have the exact same (shifted) floor state
                sequence_height = max_floor_height - prev_floor_height
                shifted_floor_squares = set(
                    (row_idx + sequence_height, col_idx)
                    for row_idx, col_idx in prev_floor_squares
                )
                if len(shifted_floor_squares.difference(floor_squares)) == 0:
                    # We encountered a recurring sequence
                    sequence_period = num_rocks - prev_num_rocks
                    num_periods = (max_num_rocks - 1 - num_rocks) // sequence_period

                    # Update the state
                    # To be what we should be after the maximum number of recurring periods
                    num_rocks += num_periods * sequence_period
                    floor_squares = set(
                        (row_idx + num_periods * sequence_height, col_idx)
                        for row_idx, col_idx in floor_squares
                    )
                    max_floor_height = max_floor_height + num_periods * sequence_height

                    # Remark: The last few rocks need to be processed individually
                    first_rock_sequence_finder = {}

            # No recurring sequence was found: cache the state
            first_rock_sequence_finder[jet_pattern_idx] = (num_rocks, floor_squares)

        # Initialize the rock at its initial position
        rock_squares: RockSquares = set(
            (row_idx + max_floor_height + 4, col_idx + 2)
            for row_idx, col_idx in rock_types[rock_idx]
        )

        is_stopped: bool = False
        while not is_stopped:
            # The rock has not stopped
            rock_squares, is_stopped = step(
                floor_squares, rock_squares, jet_pattern[jet_pattern_idx], chamber_width
            )
            jet_pattern_idx = (jet_pattern_idx + 1) % len(jet_pattern)

        # Update the position of the floor with the stopped rock
        floor_squares = floor_squares.union(rock_squares)
        max_floor_height = max(
            max_floor_height, max(row_idx for row_idx, _col_idx in rock_squares)
        )

        # Find the first continuous "row": which cannot be crossed by any rock
        # Remark: Can only be closed just now by the new stopped rock
        is_continuous: bool = False
        row_idx: int = 0
        for row_idx, _col_idx in rock_squares:
            for col_idx in range(chamber_width):
                potential_squares: RockSquares = {
                    (row_idx, col_idx),
                    (row_idx - 1, col_idx),
                    (row_idx + 1, col_idx),
                }
                is_continuous = len(floor_squares.intersection(potential_squares)) > 0
                if not is_continuous:
                    # There is a hole in the "row"
                    break
            if is_continuous:
                break

        if is_continuous:
            # The continuous "row" cannot be crossed by any rock
            # No need to consider anything below it
            min_floor_height = row_idx - 1
            floor_squares = set(
                square for square in floor_squares if square[0] >= min_floor_height
            )

        num_rocks += 1

    return max_floor_height


def step(
    floor_squares: RockSquares,
    rock_squares: RockSquares,
    jet_direction: int,
    chamber_width: int,
) -> Tuple[RockSquares, bool]:
    # First: move laterally 1 step pushed by the jet
    new_rock_squares: RockSquares = set(
        (row_idx, col_idx + jet_direction) for row_idx, col_idx in rock_squares
    )
    # If collide with the walls or the floor: do not move
    collide_with_wall: bool = any(
        col_idx < 0 or col_idx >= chamber_width
        for _row_idx, col_idx in new_rock_squares
    )
    if not collide_with_wall and len(new_rock_squares.intersection(floor_squares)) == 0:
        rock_squares = new_rock_squares

    # Then: move vertically 1 step
    new_rock_squares = set((row_idx - 1, col_idx) for row_idx, col_idx in rock_squares)
    # If collide with the floor: do not move
    collide_with_floor = len(new_rock_squares.intersection(floor_squares)) > 0
    if not collide_with_floor:
        rock_squares = new_rock_squares

    return rock_squares, collide_with_floor
