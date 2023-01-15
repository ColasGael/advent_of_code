from typing import List, Tuple

import numpy as np
import numpy.typing as npt


Coord = Tuple[int, int]
# map[i, j, k] = is there a blizzard of direction k in position (i, j) ?
# With: k = 0 (up) ; 1 (down) ; 2 (left) ; 3 (right)
Map = npt.NDArray[np.bool_]


def main(input_lines: List[str]) -> Tuple[int, int]:
    valley_map: Map
    start_pos: Coord
    end_pos: Coord
    valley_map, start_pos, end_pos = parse_valley_map(input_lines)

    # Remark: Why add 2 below?
    # start at t = 1: as this is not the start position,
    # but actually the second one (first in the valley)
    # end at t = t_end + 1: as this is not the end position,
    # but actually the second to last on (last in the valley)

    # One-way
    first_trip_forward, valley_map = bfs(valley_map, start_pos, end_pos)
    part1_answer: int = 1 + first_trip_forward + 1

    # Round-trip + one-way
    # pylint: disable=arguments-out-of-order
    trip_back_time, valley_map = bfs(valley_map, end_pos, start_pos)
    second_trip_forward_time, valley_map = bfs(valley_map, start_pos, end_pos)
    # pylint: enable=arguments-out-of-order
    part2_answer: int = (
        1 + first_trip_forward + trip_back_time + second_trip_forward_time + 1
    )

    return part1_answer, part2_answer


def parse_valley_map(  # pylint: disable=too-many-arguments, too-many-locals
    input_lines: List[str],
    empty_char: str = ".",
    up_char: str = "^",
    down_char: str = "v",
    left_char: str = "<",
    right_char: str = ">",
) -> Tuple[Map, Coord, Coord]:
    assert len(input_lines) > 2

    # To account for the valley's walls
    num_rows: int = len(input_lines) - 2
    num_cols: int = len(input_lines[0]) - 2
    valley_map: Map = np.full((num_rows, num_cols, 4), False, dtype=np.bool_)

    # Get the start position
    start_col_idx: int = input_lines[0].index(empty_char) - 1
    start_pos: Coord = (0, start_col_idx)

    # Build the map
    for i, input_line in enumerate(input_lines[1:-1]):
        for j, char in enumerate(input_line[1:-1]):
            if char == up_char:
                valley_map[i, j, 0] = True
            elif char == down_char:
                valley_map[i, j, 1] = True
            elif char == left_char:
                valley_map[i, j, 2] = True
            elif char == right_char:
                valley_map[i, j, 3] = True
            elif char != empty_char:
                raise RuntimeError(f"Unsupported character {char}")

    valley_map = step_map(valley_map)

    # Get the end position
    end_col_idx: int = input_lines[-1].index(empty_char) - 1
    end_pos: Coord = (num_rows - 1, end_col_idx)

    return valley_map, start_pos, end_pos


def bfs(valley_map: Map, start_pos: Coord, end_pos: Coord) -> Tuple[int, Map]:
    # Initialization
    time: int = 0
    # reachable[i, j] = is this point reachable at t?
    reachable: npt.NDArray[np.bool_] = np.full(
        valley_map.shape[:2], False, dtype=np.bool_
    )

    # Step 1: Wait for the start position to be reachable
    while np.any(valley_map[start_pos[0], start_pos[1]]):
        time += 1
        # Update the positions of the blizzards
        valley_map = step_map(valley_map)
    reachable[start_pos[0], start_pos[1]] = True

    # Step 2: Move in the valley
    while not reachable[end_pos[0], end_pos[1]]:
        time += 1
        # Update the positions of the blizzards
        valley_map = step_map(valley_map)
        # Check which positions can be moved to
        movable = np.copy(reachable)
        movable[:-1, :] = np.logical_or(movable[:-1, :], reachable[1:, :])  # move up
        movable[1:, :] = np.logical_or(movable[1:, :], reachable[:-1, :])  # move down
        movable[:, :-1] = np.logical_or(movable[:, :-1], reachable[:, 1:])  # move left
        movable[:, 1:] = np.logical_or(movable[:, 1:], reachable[:, :-1])  # move right
        # Check which positions do not have any blizzard
        no_blizzard = np.logical_not(np.any(valley_map, axis=2))
        # Get the reachable positions at time t
        reachable = np.logical_and(movable, no_blizzard)
        # The start position is always reachable when there is no blizzard
        reachable[start_pos[0], start_pos[1]] = no_blizzard[start_pos[0], start_pos[1]]

    return time, valley_map


def step_map(valley_map: Map):
    new_valley_map = np.full_like(valley_map, False)
    # Upward-facing blizzards
    new_valley_map[:-1, :, 0] = valley_map[1:, :, 0]
    new_valley_map[-1, :, 0] = valley_map[0, :, 0]
    # Downward-facing blizzards
    new_valley_map[1:, :, 1] = valley_map[:-1, :, 1]
    new_valley_map[0, :, 1] = valley_map[-1, :, 1]
    # Leftward-facing blizzards
    new_valley_map[:, :-1, 2] = valley_map[:, 1:, 2]
    new_valley_map[:, -1, 2] = valley_map[:, 0, 2]
    # Rightward-facing blizzards
    new_valley_map[:, 1:, 3] = valley_map[:, :-1, 3]
    new_valley_map[:, 0, 3] = valley_map[:, -1, 3]
    return new_valley_map
