from typing import List, Tuple

import numpy as np
import numpy.typing as npt


Map = npt.NDArray[np.int64]


def main(input_lines: List[str]) -> Tuple[int, int]:
    tree_map: Map = parse_tree_map(input_lines)

    # Number of visible tress
    part1_answer: int = int(np.sum(find_visible_trees(tree_map)))
    # Maximum scenic score
    part2_answer: int = np.max(np.prod(find_viewing_distances(tree_map), axis=2))

    return part1_answer, part2_answer


def parse_tree_map(input_lines: List[str]) -> Map:
    assert len(input_lines) > 0, "Empty tree_map"
    tree_map: Map = np.empty(
        shape=(len(input_lines), len(input_lines[0])), dtype=np.int64
    )
    for row_idx, row in enumerate(input_lines):
        for col_idx, height in enumerate(row):
            tree_map[row_idx, col_idx] = int(height)
    return tree_map


def find_visible_trees(tree_map: Map) -> npt.NDArray[np.bool_]:
    # Initialization
    is_visible_map: npt.NDArray[np.bool_] = np.full(tree_map.shape, False)
    max_height_row: Map = np.full(tree_map.shape[0], -1)
    max_height_col: Map = np.full(tree_map.shape[1], -1)

    # Check how many trees are visible from the top or left
    for row_idx in range(tree_map.shape[0]):
        for col_idx in range(tree_map.shape[1]):
            height = tree_map[row_idx, col_idx]
            is_visible = False
            if height > max_height_row[col_idx]:
                max_height_row[col_idx] = height
                is_visible = True
            if height > max_height_col[row_idx]:
                max_height_col[row_idx] = height
                is_visible = True
            if is_visible and not is_visible_map[row_idx, col_idx]:
                is_visible_map[row_idx, col_idx] = is_visible

    max_height_row.fill(-1)
    max_height_col.fill(-1)
    # Check how many trees are visible from the bottom or right
    for row_idx in range(tree_map.shape[0] - 1, -1, -1):
        for col_idx in range(tree_map.shape[1] - 1, -1, -1):
            height = tree_map[row_idx, col_idx]
            is_visible = False
            if height > max_height_row[col_idx]:
                max_height_row[col_idx] = height
                is_visible = True
            if height > max_height_col[row_idx]:
                max_height_col[row_idx] = height
                is_visible = True
            if is_visible and not is_visible_map[row_idx, col_idx]:
                is_visible_map[row_idx, col_idx] = is_visible

    return is_visible_map


def find_viewing_distances(tree_map: Map) -> npt.NDArray[np.int64]:
    # Initialization
    viewing_dists: npt.NDArray[np.int64] = np.full(
        (tree_map.shape[0], tree_map.shape[1], 4), 0
    )

    # Compute the top and left viewing distances
    for row_idx in range(tree_map.shape[0]):
        for col_idx in range(tree_map.shape[1]):
            height = tree_map[row_idx, col_idx]
            if row_idx > 0:
                neigh_row_idx = row_idx - 1
                while neigh_row_idx > 0 and tree_map[neigh_row_idx, col_idx] < height:
                    neigh_row_idx -= viewing_dists[neigh_row_idx, col_idx, 0]
                viewing_dists[row_idx, col_idx, 0] = row_idx - neigh_row_idx

            if col_idx > 0:
                neigh_col_idx = col_idx - 1
                while neigh_col_idx > 0 and tree_map[row_idx, neigh_col_idx] < height:
                    neigh_col_idx -= viewing_dists[row_idx, neigh_col_idx, 1]
                viewing_dists[row_idx, col_idx, 1] = col_idx - neigh_col_idx

    # Compute the bottom and right viewing distances
    for row_idx in range(tree_map.shape[0] - 1, -1, -1):
        for col_idx in range(tree_map.shape[1] - 1, -1, -1):
            height = tree_map[row_idx, col_idx]
            if row_idx < tree_map.shape[0] - 1:
                neigh_row_idx = row_idx + 1
                while (
                    neigh_row_idx < tree_map.shape[0] - 1
                    and tree_map[neigh_row_idx, col_idx] < height
                ):
                    neigh_row_idx += viewing_dists[neigh_row_idx, col_idx, 2]
                viewing_dists[row_idx, col_idx, 2] = neigh_row_idx - row_idx

            if col_idx < tree_map.shape[1] - 1:
                neigh_col_idx = col_idx + 1
                while (
                    neigh_col_idx < tree_map.shape[1] - 1
                    and tree_map[row_idx, neigh_col_idx] < height
                ):
                    neigh_col_idx += viewing_dists[row_idx, neigh_col_idx, 3]
                viewing_dists[row_idx, col_idx, 3] = neigh_col_idx - col_idx

    return viewing_dists


# TODO(ColasGael): Is there a way to process the map in a single loop?
# IDEA: For a single row, here is a 1D approach to find both left and right-visible trees
# left_idx = 0
# left_max_height = -1
# right_idx = tree_map.shape[1] - 1
# right_max_height = -1
# while left_idx <= right_idx:
#     if left_max_height < right_max_height:
#         left_height =  tree_map[row_idx, left_idx]
#         if left_height > left_max_height:
#             left_max_height = left_height
#             if not is_visible[row_idx, left_idx]:
#                 is_visible[row_idx, left_idx] = True
#         left_idx += 1
#     else:
#         right_height =  tree_map[row_idx, right_idx]
#         if right_height > right_max_height:
#             right_max_height = right_height
#             if not is_visible[row_idx, right_idx]:
#                 is_visible[row_idx, right_idx] = True
#         right_idx -= 1
