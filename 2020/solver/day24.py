import re

import numpy as np

from .day11 import convolution_2d


SUPPORTED_DIRECTIONS = ["e", "se", "sw", "w", "nw", "ne"]


def main(input_lines, n_days=100):
    tiles_directions = parse_input(input_lines, SUPPORTED_DIRECTIONS)
    initial_black_tiles = find_black_tiles(tiles_directions)
    part1_answer = len(initial_black_tiles)

    part2_answer = np.sum(
        finish_exhibit(initial_black_tiles, n_days, SUPPORTED_DIRECTIONS)
    )

    return part1_answer, part2_answer


def parse_input(input_lines, supported_directions):
    directions_pattern = re.compile(r"|".join(supported_directions))
    tiles_directions = []
    for input_line in input_lines:
        tiles_directions.append(directions_pattern.findall(input_line))
    return tiles_directions


def find_black_tiles(tiles_directions):
    black_tiles = []
    for tile_directions in tiles_directions:
        tile_coordinates = get_tile_coordinates(tile_directions)
        if tile_coordinates in black_tiles:
            black_tiles.remove(tile_coordinates)
        else:
            black_tiles.append(tile_coordinates)
    return black_tiles


def get_tile_coordinates(tile_directions):
    tile_coordinates = np.array((0, 0))
    for direction in tile_directions:
        coordinates_update = direction_to_coordinates(direction)
        tile_coordinates = tile_coordinates + coordinates_update
    return tile_coordinates.tolist()


def direction_to_coordinates(direction):
    if direction == "e":
        coordinates = (0, 1)
    elif direction == "se":
        coordinates = (-1, 1)
    elif direction == "sw":
        coordinates = (-1, 0)
    elif direction == "w":
        coordinates = (0, -1)
    elif direction == "nw":
        coordinates = (1, -1)
    elif direction == "ne":
        coordinates = (1, 0)
    else:
        raise RuntimeError("Unsupported direction: {} !".format(direction))
    return np.array(coordinates)


def finish_exhibit(initial_black_tiles, n_days, supported_directions):
    floor_plan = get_floor_plan(initial_black_tiles, n_days)
    neighbor_mask = get_neighbor_mask(supported_directions)
    for _i in range(n_days):
        floor_plan = step(floor_plan, neighbor_mask)
    return floor_plan


def get_floor_plan(initial_black_tiles, n_days):
    initial_dimensions = np.max(np.array(initial_black_tiles), axis=0) - np.min(
        np.array(initial_black_tiles), axis=0
    )
    final_dimensions = initial_dimensions + 2 * (n_days + 1)
    floor_plan = np.full(final_dimensions, False)
    for initial_black_tile in initial_black_tiles:
        floor_plan[
            initial_black_tile[0] + n_days + 1, initial_black_tile[1] + n_days + 1
        ] = True
    return floor_plan


def get_neighbor_mask(supported_directions):
    neighbor_mask = np.full((3, 3), False)
    for direction in supported_directions:
        coordinates = direction_to_coordinates(direction)
        neighbor_mask[coordinates[0], coordinates[1]] = True
    return neighbor_mask


def step(floor_plan, neighbor_mask):
    n_neighbors = convolution_2d(floor_plan, neighbor_mask)
    next_floor_plan = np.logical_or(
        np.logical_and(
            floor_plan, np.logical_not(np.logical_or(n_neighbors == 0, n_neighbors > 2))
        ),
        np.logical_and(np.logical_not(floor_plan), n_neighbors == 2),
    )
    return next_floor_plan
