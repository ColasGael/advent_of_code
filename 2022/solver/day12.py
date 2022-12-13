import heapq
from typing import Dict, List, Tuple

import numpy as np
import numpy.typing as npt


Coord = Tuple[int, int]
Map = npt.NDArray[np.int64]


def main(input_lines: List[str]) -> Tuple[int, int]:
    height_map: Map
    end: Coord
    start: Coord
    potential_starts: List[Coord]
    height_map, end, start, potential_starts = parse_height_map(input_lines)

    # part1_answer: int = a_star(height_map, start, end)

    dists_from_start_to_end: Dict[Coord, int] = dijkstra(
        height_map, potential_starts, end
    )
    part1_answer: int = dists_from_start_to_end[start]
    part2_answer: int = min(dists_from_start_to_end.values())

    return part1_answer, part2_answer


def parse_height_map(
    input_lines: List[str], start_char: str = "S", end_char: str = "E"
) -> Tuple[Map, Coord, Coord, List[Coord]]:
    height_map: Map = np.full(
        (len(input_lines), len(input_lines[0])), -1, dtype=np.int64
    )
    start: Coord = (-1, -1)
    potential_starts: List[Coord] = []
    end: Coord = (-1, -1)

    for i, input_line in enumerate(input_lines):
        for j, char in enumerate(input_line):
            if char == start_char:
                start = (i, j)
                potential_starts.append(start)
                char = "a"
            elif char == end_char:
                end = (i, j)
                char = "z"
            elif char == "a":
                potential_starts.append((i, j))
            height_map[i, j] = ord(char) - ord("a")

    return height_map, end, start, potential_starts


# pylint: disable=invalid-name
def get_neighs(height_map: Map, point: Coord) -> List[Coord]:
    n_row, n_col = height_map.shape
    x, y = point
    offsets: Tuple[Coord, ...] = ((0, 1), (0, -1), (1, 0), (-1, 0))
    neighs: List[Coord] = []
    for offset in offsets:
        dx, dy = offset
        if 0 <= x + dx < n_row and 0 <= y + dy < n_col:
            neighs.append((x + dx, y + dy))
    return neighs


# pylint: enable=invalid-name


def dijkstra(height_map: Map, starts: List[Coord], end: Coord) -> Dict[Coord, int]:
    """Reformulate the problem as: how to get from end to start?

    Why? To handle several starts.

    In the usual formulation: how to get from start to end?
    fscore[point] = shortest distance from start to point
    This cannot be re-used between runs from different start.

    However, if we reformulate the problem as: how to get from end to start?
    fscore[point] = shortest distance from point to end
    So the fscore matrix is the same regardless of the start.

    Remark: We cannot use A* anymore as there is no single goal anymore (several starts).
    """
    dists_from_start_to_end: Dict[Coord, int] = {}

    # Initialization
    open_points: List[Tuple[int, Coord]] = [(0, end)]
    heapq.heapify(open_points)
    visited: npt.NDArray[np.bool_] = np.full_like(height_map, False)
    gscore: Map = np.full_like(height_map, -1)
    gscore[end[0], end[1]] = 0

    while open_points:
        _gscore, point = heapq.heappop(open_points)
        if visited[point[0], point[1]]:
            continue
        visited[point[0], point[1]] = True

        # Wait to find the distance to end for all the starts
        if point in starts:
            dists_from_start_to_end[point] = gscore[point[0], point[1]]
            if len(dists_from_start_to_end) == len(starts):
                break

        for neigh in get_neighs(height_map, point):
            # Reformulated as: how to get from end to start
            # Can go down at most 1 step per move (but climb as many steps as wanted)
            if -(height_map[neigh[0], neigh[1]] - height_map[point[0], point[1]]) > 1:
                continue

            if visited[neigh[0], neigh[1]]:
                continue

            # Distance between neighbors is exactly 1
            tmp_gscore = gscore[point[0], point[1]] + 1
            if (
                gscore[neigh[0], neigh[1]] == -1
                or tmp_gscore < gscore[neigh[0], neigh[1]]
            ):
                gscore[neigh[0], neigh[1]] = tmp_gscore
                heapq.heappush(open_points, (tmp_gscore, neigh))

    return dists_from_start_to_end


def min_dist_to_end(point: Coord, end: Coord, height_map: Map) -> int:
    height_diff = height_map[end[0], end[1]] - height_map[point[0], point[1]]
    lateral_dist = abs(point[0] - end[0]) + abs(point[1] - end[1])
    return max(lateral_dist, height_diff)


def a_star(height_map: Map, start: Coord, end: Coord) -> int:
    # Initialization
    open_points: List[Tuple[int, Coord]] = [(0, start)]
    heapq.heapify(open_points)
    visited: npt.NDArray[np.bool_] = np.full_like(height_map, False)
    gscore: Map = np.full_like(height_map, -1)
    gscore[start[0], start[1]] = 0

    while open_points:
        _fscore, point = heapq.heappop(open_points)
        if visited[point[0], point[1]]:
            continue
        visited[point[0], point[1]] = True

        if point == end:
            break

        for neigh in get_neighs(height_map, point):
            # Can climb at most 1 step per move (but go down as many steps as wanted)
            if height_map[neigh[0], neigh[1]] - height_map[point[0], point[1]] > 1:
                continue

            if visited[neigh[0], neigh[1]]:
                continue

            # Distance between neighbors is exactly 1
            tmp_gscore = gscore[point[0], point[1]] + 1
            if (
                gscore[neigh[0], neigh[1]] == -1
                or tmp_gscore < gscore[neigh[0], neigh[1]]
            ):
                gscore[neigh[0], neigh[1]] = tmp_gscore
                fscore = gscore[neigh[0], neigh[1]] + min_dist_to_end(
                    neigh, end, height_map
                )
                heapq.heappush(open_points, (fscore, neigh))

    return gscore[end[0], end[1]]
