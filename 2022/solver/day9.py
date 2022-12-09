from typing import List, Tuple

import numpy as np
import numpy.typing as npt


Coord = npt.NDArray[np.int8]
Motion = Tuple[Coord, int]


def main(input_lines: List[str]) -> Tuple[int, int]:
    motions: List[Motion] = parse_motions(input_lines)

    part1_answer: int = len(find_visited_tail_position(motions, n_knots=2))
    part2_answer: int = len(find_visited_tail_position(motions, n_knots=10))

    return part1_answer, part2_answer


def parse_motions(input_lines: List[str]) -> List[Motion]:
    motions: List[Motion] = []
    for input_line in input_lines:
        direction_indicator, n_steps = input_line.split(" ")
        if direction_indicator == "R":
            direction = (1, 0)
        elif direction_indicator == "L":
            direction = (-1, 0)
        elif direction_indicator == "U":
            direction = (0, 1)
        elif direction_indicator == "D":
            direction = (0, -1)
        else:
            raise RuntimeError(f"Unsupported direction {direction_indicator}")
        motions.append((np.array(direction), int(n_steps)))
    return motions


def follow(head_pos: Coord, tail_pos: Coord) -> Coord:
    diff = head_pos - tail_pos
    if np.max(np.abs(diff)) <= 1:
        # Head and tail are still touching each other
        new_direction = np.array((0, 0))
    else:
        new_direction = np.sign(diff)
    return new_direction


def find_visited_tail_position(motions: List[Motion], n_knots: int = 2):
    assert n_knots >= 2, "A rope must at least have a start and an end: >= 2 knots"

    # Initialization
    knots: List[Coord] = [np.array((0, 0)) for _i in range(n_knots)]
    # remark: np.array is not hashable
    visited_tail_pos = set()

    for motion in motions:
        initial_direction, n_steps = motion
        for _i in range(n_steps):
            # Update the following knots' positions
            for j, knot in enumerate(knots):
                if j == 0:
                    direction = initial_direction
                else:
                    direction = follow(knots[j - 1], knot)
                if np.sum(np.abs(direction)) == 0:
                    # Current knot did not move so following knots won't move either
                    break
                knots[j] += direction
            # Save the tail position
            visited_tail_pos.add(tuple(knots[-1]))

    return visited_tail_pos
