import re
from collections import deque

import numpy as np

from day11 import convolution2D


MONSTER_PATTERN = [
    "..................#.",
    "#....##....##....###",
    ".#..#..#..#..#..#...",
]


def main(input_lines, pixel_0='.', pixel_1='#'):
    tiles = parse_input(input_lines, pixel_0, pixel_1)
    puzzle = solve_puzzle(tiles)
    part1_answer = np.prod([puzzle[i, j] for i in (0, -1) for j in (0, -1)])

    final_image = merge_tiles(tiles, puzzle)
    monster_image = parse_tile(MONSTER_PATTERN, pixel_0, pixel_1)
    # visualize(apply_rotation(np.flipud(final_image), 90), pixel_0, pixel_1)
    n_monsters = find_monsters(final_image, monster_image)
    part2_answer = np.sum(final_image) - n_monsters * np.sum(monster_image)
    return part1_answer, part2_answer


def parse_input(input_lines, pixel_0, pixel_1):
    tiles = {}
    tile_raw = []
    for input_line in input_lines:
        if len(input_line) == 0:
            tiles[tile_id] = parse_tile(tile_raw, pixel_0, pixel_1)
            tile_raw = []
        elif 'Tile' in input_line:
            tile_id = int(re.search("\d+", input_line).group())
        else:
            tile_raw.append(input_line)
    tiles[tile_id] = parse_tile(tile_raw, pixel_0, pixel_1)
    return tiles


def parse_tile(tile_raw, pixel_0, pixel_1):
    tile_array = np.array([[char == pixel_1 for char in tile_line] for tile_line in tile_raw])
    return tile_array


def solve_puzzle(tiles):
    connections = find_connections(tiles)
    if not check_assumptions(connections):
        raise RuntimeError("This input cannot be solved with this method: 1 or more of the tile matches with another it is not connected with!")

    orientations = {
        this_tile_id: {
            this_orientation: other_tile_id for other_tile_id, this_orientation in this_tile_connections.items()
        } for this_tile_id, this_tile_connections in connections.items()
    }

    side_length = int(np.sqrt(len(tiles)))
    puzzle = np.full((side_length, side_length), None)

    first_corner_id = [tile_id for tile_id in connections.keys() if (len(connections[tile_id]) == 2)][0]
    puzzle[0, 0] = first_corner_id
    last_down_orientation, last_right_orientation = orientations[first_corner_id].keys()
    if not align_rotation(last_down_orientation, last_right_orientation) == 90:
        last_down_orientation, last_right_orientation = last_right_orientation, last_down_orientation

    for i in range(side_length):
        if i != 0:
            puzzle[i, 0] = orientations[puzzle[i-1, 0]][last_down_orientation]
            last_down_orientation = align_rotation(connections[puzzle[i, 0]][puzzle[i-1, 0]], 180)
            last_right_orientation = align_rotation(last_down_orientation, 90)
        tiles[puzzle[i, 0]] = apply_rotation(tiles[puzzle[i, 0]], align_rotation(last_down_orientation, 180))
        for j in range(1, side_length):
            puzzle[i, j] = orientations[puzzle[i, j-1]][last_right_orientation]
            last_right_orientation = align_rotation(connections[puzzle[i, j]][puzzle[i, j-1]], 180)
            tiles[puzzle[i, j]] = apply_rotation(tiles[puzzle[i, j]], align_rotation(last_right_orientation, 90))
    return puzzle


def check_assumptions(connections):
    n_tiles = len(connections)
    side_length = int(np.sqrt(n_tiles))
    n_connections = {}
    for tile_connections in connections.values():
        n_connection = len(tile_connections)
        n_connections[n_connection] = n_connections.get(n_connection, 0) + 1
    is_valid = True
    if set(n_connections.keys()) != set((2, 3, 4)):
        is_valid = False
    elif n_connections[2] != 4:
        is_valid = False
    elif n_connections[3] != 4 * (side_length - 2):
        is_valid = False
    elif n_connections[4] != n_tiles - 4 * (side_length - 1):
        is_valid = False
    return is_valid


def find_connections(tiles):
    borders = {tile_id: get_borders(tiles[tile_id]) for tile_id in tiles.keys()}
    connections = {tile_id: {} for tile_id in tiles.keys()}

    todo_tiles = deque()
    first_tile_id = tiles.keys()[0]
    todo_tiles.append(first_tile_id)
    is_done_tile = {tile_id: False for tile_id in tiles.keys()}
    while todo_tiles:
        this_tile_id = todo_tiles.popleft()
        this_tile_borders = borders[this_tile_id]
        is_done_tile[this_tile_id] = True
        for other_tile_id, other_tile_borders in borders.items():
            if is_done_tile[other_tile_id]:
                continue
            for (this_is_flipped, this_rotation), this_tile_border in this_tile_borders.items():
                if this_is_flipped:
                    continue
                for (other_is_flipped, other_rotation), other_tile_border in other_tile_borders.items():
                    if np.all(this_tile_border == other_tile_border[::-1]):
                        connections[this_tile_id][other_tile_id] = this_rotation
                        connections[other_tile_id][this_tile_id] = other_rotation
                        if other_is_flipped:
                            tiles[other_tile_id] = np.flipud(tiles[other_tile_id])
                            borders[other_tile_id] = {(not is_flipped, rotation): tile_border for (is_flipped, rotation), tile_border in borders[other_tile_id].items()}
                        todo_tiles.append(other_tile_id)
                        break
    return connections


def get_borders(tile):
    # (False, 0): tile[0, :], (False, 90): np.flip(tile[:, 0]), (False, 180): np.flip(tile[-1, :]), (False, 270): tile[:, -1],
    # (True, 0): tile[-1, :], (True, 90): tile[:, 0], (True, 180): np.flip(tile[0, :]), (True, 270): np.flip(tile[:, -1]),
    borders = {
        (is_flipped, rotation_angle): apply_rotation(np.flipud(tile) if is_flipped else tile, rotation_angle)[0, :]
        for is_flipped in (False, True) for rotation_angle in (0, 90, 180, 270)
    }
    return borders


def align_rotation(this_rotation, other_rotation):
    rotation = (this_rotation - other_rotation) % 360
    return rotation


def apply_rotation(tile, rotation):
    if rotation == 0:
        pass
    elif rotation == 90:
        tile = np.swapaxes(np.fliplr(tile), 0, 1)
    elif rotation == 180:
        tile = np.fliplr(np.flipud(tile))
    elif rotation == 270:
        tile = np.swapaxes(np.flipud(tile), 0, 1)
    return tile


def merge_tiles(tiles, puzzle):
    image_rows = []
    for i in range(puzzle.shape[0]):
        image_row_columns = []
        for j in range(puzzle.shape[1]):
            tile = tiles[puzzle[i, j]]
            cropped_tile = tile[1:-1, 1:-1]
            image_row_columns.append(cropped_tile)
        image_rows.append(np.hstack(image_row_columns))
    image = np.vstack(image_rows)
    return image


def visualize(tile, pixel_0, pixel_1):
    image_viz = ""
    for i in range(tile.shape[0]):
        for j in range(tile.shape[1]):
            image_viz = image_viz + (pixel_1 if tile[i, j] else pixel_0)
        image_viz = image_viz + '\n'
    print(image_viz)


def find_monsters(image, monster_image):
    image_height, image_length = image.shape
    monster_height, monster_length = monster_image.shape
    n_monster_pixels = np.sum(monster_image)

    n_monsters = 0
    oriented_images = [apply_rotation(np.flipud(image) if is_flipped else image, rotation_angle)
                       for is_flipped in (False, True) for rotation_angle in (0, 90, 180, 270)]
    for oriented_image in oriented_images:
        matched_image = convolution2D(oriented_image, monster_image)
        n_monsters = np.sum(matched_image == n_monster_pixels)
        if n_monsters != 0:
            break
    return n_monsters
