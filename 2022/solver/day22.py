from typing import Callable, List, Tuple, Union

import numpy as np
import numpy.typing as npt


Map = npt.NDArray[np.int8]
Instruction = Union[str, int]
# (row_idx, col_idx, orientation)
Position = Tuple[int, int, int]

WrapFunc = Callable[[Position, Map], Tuple[Position, Map]]

# (row_idx, col_idx)
Coord = Tuple[int, int]
# (top or left corner, whether it is an horizontal edge)
Edge = Tuple[Coord, bool]
# (first_edge, second_edge, is_flipped = whether we enter the second edge from the other side)
EdgeMapping = Tuple[Edge, Edge, bool]


# WARNING: The cube has been visually folded
# This is the hard-coded edge mapping for my input cube
# TODO(ColasGael): Find a way to do it algorithmically to support any cube
## For toy input
# EDGE_LENGTH = 4
# EDGES: List[EdgeMapping] = [
#     (((4, 0), True), ((0, 8), True), True),
#     (((4, 4), True), ((0, 8), False), False),
#     (((0, 11), False), ((8, 15), False), True),
#     (((4, 11), False), ((8, 12), True), True),
#     (((11, 12), True), ((8, 0), False), True),
#     (((11, 8), True), ((7, 0), True), True),
#     (((8, 8), False), ((8, 4), True), True),
# ]
## For actual input
EDGE_LENGTH = 50
EDGES: List[EdgeMapping] = [
    (((100, 0), True), ((50, 50), False), False),
    (((0, 50), False), ((100, 0), False), True),
    (((0, 50), True), ((150, 0), False), False),
    (((0, 100), True), ((199, 0), True), False),
    (((0, 149), False), ((100, 99), False), True),
    (((49, 100), True), ((50, 99), False), False),
    (
        ((149, 50), True),
        ((150, 49), False),
        True,
    ),  # weird: should be is_flipped = False
]


def main(input_lines: List[str]) -> Tuple[int, int]:
    board_map: Map
    instructions: List[Instruction]
    board_map, instructions = parse_notes(input_lines)

    part1_answer: int = compute_password(solve(board_map, instructions, part1_wrap))
    part2_answer: int = compute_password(solve(board_map, instructions, part2_wrap))

    return part1_answer, part2_answer


def parse_notes(
    input_lines: List[str], tile_char=".", wall_char="#"
) -> Tuple[Map, List[Instruction]]:
    raw_map: List[List[int]] = []

    for input_line in input_lines[:-2]:
        # Parse the next row of the map
        raw_map.append([])
        for char in input_line:
            map_value: int = -1
            if char == tile_char:
                map_value = 0
            elif char == wall_char:
                map_value = 1
            raw_map[-1].append(map_value)

    # Uniformize the lengths of the map rows
    max_row_len: int = max(map(len, raw_map))
    for row in raw_map:
        for _i in range(len(row), max_row_len):
            row.append(-1)

    # Convert to array
    board_map: Map = np.array(raw_map, dtype=np.int8)

    # Parse the instructions
    instructions: List[Instruction] = []
    steps = ""
    for char in input_lines[-1]:
        if char.isdigit():
            steps += char
        else:
            if len(steps) > 0:
                instructions.append(int(steps))
                steps = ""
            instructions.append(char)
    if len(steps) > 0:
        instructions.append(int(steps))

    return board_map, instructions


def solve(
    board_map: Map, instructions: List[Instruction], wrap_func: WrapFunc
) -> Position:
    # Find the initial position: first free tile on the first row, and facing right
    initial_col_idx = int(np.argmax(board_map[0] == 0))
    assert board_map[0, initial_col_idx] == 0
    position: Position = (0, initial_col_idx, 0)

    for instruction in instructions:
        position = move(position, instruction, board_map, wrap_func)

    return position


def move(  # pylint: disable=too-many-branches
    position: Position, instruction: Instruction, board_map: Map, wrap_func: WrapFunc
) -> Position:
    if isinstance(instruction, str):
        orientation: int = position[2]
        if instruction == "R":
            orientation = (position[2] + 1) % 4
        elif instruction == "L":
            orientation = (position[2] - 1) % 4
        else:
            raise RuntimeError(f"Unsupported orientation: {instruction}")
        position = (position[0], position[1], orientation)

    else:
        # Update to a move-to-right equivalent frame
        position, board_map = transform_axes(position, board_map)
        steps: int = instruction
        while steps > 0:
            forward_section = board_map[
                position[0], position[1] : position[1] + steps + 1
            ]
            # Check if we can move unobstructed
            first_non_tile_col_idx = int(np.argmax(forward_section != 0))
            if forward_section[first_non_tile_col_idx] == 1:
                # Encountered a wall: stop
                position = (
                    position[0],
                    position[1] + first_non_tile_col_idx - 1,
                    position[2],
                )
                steps = 0
            elif forward_section[first_non_tile_col_idx] == 0 and (
                forward_section.size == steps + 1
            ):
                # Moved as much as we wanted: stop
                position = (position[0], position[1] + steps, position[2])
                steps = 0
            else:
                # Moved unobstructed to the edge of the map: try moving on the other side
                if forward_section[first_non_tile_col_idx] == 0:
                    position = (
                        position[0],
                        position[1] + forward_section.size - 1,
                        position[2],
                    )
                    steps -= forward_section.size - 1
                else:
                    position = (
                        position[0],
                        position[1] + first_non_tile_col_idx - 1,
                        position[2],
                    )
                    steps -= first_non_tile_col_idx - 1
                # Wrap around
                wrapped_position, wrapped_board_map = wrap_func(position, board_map)
                if wrapped_board_map[wrapped_position[0], wrapped_position[1]] == 1:
                    # Encountered a wall: stop
                    steps = 0
                else:
                    position = wrapped_position
                    board_map = wrapped_board_map
                    steps -= 1

        # Reverse the previous operation on the axes
        position, board_map = transform_axes(position, board_map, reverse=True)

    return position


def transform_axes(
    position: Position, board_map: Map, reverse: bool = False
) -> Tuple[Position, Map]:
    orientation: int = position[2]
    num_rows, num_cols = board_map.shape
    # Update to make all movements equivalent to moving in the right direction
    # Remark: the operations return a view of the array, so they are run in constant time
    # if orientation == 0: nothing to do
    if orientation == 1:
        board_map = np.transpose(board_map)
        position = (position[1], position[0], orientation)
    elif orientation == 2:
        board_map = np.fliplr(board_map)
        position = (position[0], num_cols - 1 - position[1], orientation)
    elif orientation == 3:
        if not reverse:
            board_map = np.fliplr(np.transpose(board_map))
            position = (position[1], num_rows - 1 - position[0], orientation)
        else:
            board_map = np.transpose(np.fliplr(board_map))
            position = (num_cols - 1 - position[1], position[0], orientation)
    return position, board_map


def part1_wrap(position: Position, board_map: Map) -> Tuple[Position, Map]:
    # Find the first tile position of the row
    col_idx = int(np.argmax(board_map[position[0]] != -1))
    position = (position[0], col_idx, position[2])
    return position, board_map


def part2_wrap(position: Position, board_map: Map) -> Tuple[Position, Map]:
    # Get back to the original frame
    position, board_map = transform_axes(position, board_map, reverse=True)

    # Find the edge we are currently on
    found_edge: bool = False
    current_edge: Edge
    new_edge: Edge
    edge_is_flipped: bool
    for edge_1, edge_2, is_flipped in EDGES:
        for edge in (edge_1, edge_2):
            corner, is_horizontal = edge
            found_edge = (
                is_horizontal
                and corner[0] == position[0]
                and corner[1] <= position[1] < corner[1] + EDGE_LENGTH
            ) or (
                not is_horizontal
                and corner[1] == position[1]
                and corner[0] <= position[0] < corner[0] + EDGE_LENGTH
            )
            if found_edge:
                current_edge = edge
                edge_is_flipped = is_flipped
                break
        if found_edge:
            new_edge = edge_1 if current_edge == edge_2 else edge_2
            break
    if not found_edge:
        raise RuntimeError(
            f"Could not found on which edge the following position is: {position}"
        )

    # Get the exiting position oj the new edge
    offset = max(position[0] - current_edge[0][0], position[1] - current_edge[0][1])
    if edge_is_flipped:
        offset = EDGE_LENGTH - 1 - offset
    corner, is_horizontal = new_edge
    orientation: int
    if is_horizontal:
        # Check the exiting orientation
        if corner[0] == 0 or (board_map[corner[0] - 1, corner[1]] == -1):
            orientation = 1
        else:  # board_map[corner[0] + 1, corner[1]] == -1:
            orientation = 3
        position = (corner[0], corner[1] + offset, orientation)
    else:
        # Check the exiting orientation
        if corner[1] == 0 or (board_map[corner[0], corner[1] - 1] == -1):
            orientation = 0
        else:  # board_map[corner[0], corner[1] + 1] == -1:
            orientation = 2
        position = (corner[0] + offset, corner[1], orientation)

    # Update to a move-to-right equivalent frame
    position, board_map = transform_axes(position, board_map)

    return position, board_map


def compute_password(position: Position) -> int:
    return (position[0] + 1) * 1000 + (position[1] + 1) * 4 + position[2]
