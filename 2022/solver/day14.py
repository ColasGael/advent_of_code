from typing import List, Tuple

import numpy as np
import numpy.typing as npt


Map = npt.NDArray[np.bool_]
Range = Tuple[int, Tuple[int, int]]


def main(input_lines: List[str], sand_x=500) -> Tuple[int, int]:
    cave_map: Map
    cave_map, sand_x = parse_cave_map(input_lines, sand_x)

    part1_answer: int = simulate(cave_map, sand_x)

    # Warm-start
    cave_map, sand_x = build_full_map(cave_map, sand_x)
    part2_answer: int = simulate(cave_map, sand_x) + part1_answer

    return part1_answer, part2_answer


def parse_cave_map(input_lines: List[str], sand_x: int) -> Tuple[Map, int]:
    min_x: int = sand_x
    max_x: int = sand_x
    max_y: int = 0
    x_ranges: List[Range] = []
    y_ranges: List[Range] = []

    for input_line in input_lines:
        raw_segments: List[str] = input_line.split(" -> ")
        assert (
            len(raw_segments) >= 2
        ), f"A path must have a start and end, got: {input_line}"

        segments: List[Tuple[int, int]] = []
        for raw_segment in raw_segments:
            start, end = raw_segment.split(",")
            segments.append((int(start), int(end)))

        for i, (start_x, start_y) in enumerate(segments[:-1]):
            # Extract the range of the path segment
            end_x, end_y = segments[i + 1]
            if start_x == end_x:
                if end_y < start_y:
                    end_y, start_y = start_y, end_y
                y_ranges.append((start_x, (start_y, end_y)))
            elif start_y == end_y:
                if end_x < start_x:
                    end_x, start_x = start_x, end_x
                x_ranges.append((start_y, (start_x, end_x)))
            else:
                raise RuntimeError(
                    f"Unsupported segment: {segments[i]} - {segments[i + 1]}"
                )
            # Update the bounds of the map
            min_x = min(min_x, start_x)
            max_x = max(max_x, end_x)
            max_y = max(max_y, end_y)

    # Build the map
    # cave_map[i,j] = is there a rock in (x = min_x + j, y = i)
    cave_map: Map = np.full((max_y + 1, max_x - min_x + 1), False, dtype=np.bool_)
    for fixed_y, (start_x, end_x) in x_ranges:
        start_x -= min_x
        end_x -= min_x
        cave_map[fixed_y, start_x : end_x + 1] = True
    for fixed_x, (start_y, end_y) in y_ranges:
        fixed_x -= min_x
        cave_map[start_y : end_y + 1, fixed_x] = True

    # Update the relative position of the sand
    sand_x -= min_x

    return cave_map, sand_x


def build_full_map(cave_map: Map, sand_x: int) -> Tuple[Map, int]:
    height: int
    width: int
    height, width = cave_map.shape
    # The infinite floor is 2 y-unit down
    new_height = height + 2
    # Compute the maximum width of the sand pyramid centered in sand_x
    pyramid_width = 1 + 2 * height + 2
    x_offset = max(0, (pyramid_width - 1) // 2 - sand_x)
    new_width = x_offset + max(width, sand_x + (pyramid_width - 1) // 2 + 1)
    # Update the relative position of the sand
    sand_x += x_offset

    # Build the new map
    full_cave_map: Map = np.full((new_height, new_width), False, dtype=np.bool_)
    full_cave_map[0:height, x_offset : x_offset + width] = cave_map
    full_cave_map[-1, :] = True
    return full_cave_map, sand_x


def step(cave_map: Map, sand_x: int) -> bool:
    """Add one unit of sand."""
    for y_coord in range(0, cave_map.shape[0]):
        if cave_map[y_coord, sand_x]:
            # Tile is occupied
            # 1. Try to go diagonally left
            if sand_x == 0:
                # Fall of the cave
                return False
            if not cave_map[y_coord, sand_x - 1]:
                sand_x -= 1
            # 2. Try to go diagonally right
            elif sand_x == cave_map.shape[1] - 1:
                # Fall of the cave
                return False
            elif not cave_map[y_coord, sand_x + 1]:
                sand_x += 1
            else:
                # Sand is blocked and settles above the tile
                cave_map[y_coord - 1, sand_x] = True
                return True
    return False


def simulate(cave_map: Map, sand_x: int) -> int:
    n_sand: int = 0
    while step(cave_map, sand_x):
        n_sand += 1
    return n_sand
