"""
Assumptions:
- Shapes are simple enough that the enclosed surfaces are smaller than the outside ones
"""

from collections import defaultdict
from typing import Dict, List, Tuple


Coord = Tuple[int, int, int]
Cluster = List[Coord]


def main(input_lines: List[str]) -> Tuple[int, int]:
    lava_droplets: List[Coord] = parse_lava_droplets(input_lines)

    total_visible_surface, total_exterior_surface = compute_surfaces(lava_droplets)

    part1_answer: int = total_visible_surface
    part2_answer: int = total_exterior_surface

    return part1_answer, part2_answer


def parse_lava_droplets(input_lines: List[str]) -> List[Coord]:
    lava_droplets: List[Coord] = []
    for input_line in input_lines:
        x_coord, y_coord, z_coord = input_line.split(",")
        lava_droplets.append((int(x_coord), int(y_coord), int(z_coord)))
    return lava_droplets


def compute_surfaces(lava_droplets: List[Coord]) -> Tuple[int, int]:
    clusters_and_surfaces = cluster_cubes(lava_droplets)
    total_visible_surface = sum(surface for _cluster, surface in clusters_and_surfaces)

    # Sort the clusters by decreasing sizes to check for inclusion
    clusters_and_surfaces.sort(
        key=lambda cluster_and_surface: -len(cluster_and_surface[0])
    )
    total_exterior_surface = total_visible_surface
    for k, (cluster, surface) in enumerate(clusters_and_surfaces):
        is_included = False
        for bigger_cluster, _surface in clusters_and_surfaces[:k]:
            is_included = is_included_in(cluster[0], bigger_cluster)
            if is_included:
                break

        if is_included:
            # The whole cluster is hidden from the exterior
            interior_surface = surface
        else:
            # Check what pockets of air are trapped inside the cluster
            interior_surface = compute_interior_surface(cluster)
        total_exterior_surface -= interior_surface

    return total_visible_surface, total_exterior_surface


def cluster_cubes(
    cubes: List[Coord], allow_diagonal: bool = True
) -> List[Tuple[Cluster, int]]:
    # Sort the cubes for efficiency
    cubes.sort(key=sum)

    # Initialization
    max_cluster_id: int = -1
    cluster_assignments: Dict[Coord, int] = {}
    cluster_contact_surfaces: Dict[int, int] = {}

    # Cluster the cubes
    for i, this_cube in enumerate(cubes):
        if this_cube not in cluster_assignments:
            max_cluster_id += 1
            cluster_assignments[this_cube] = max_cluster_id
            cluster_contact_surfaces[max_cluster_id] = 0
        this_cluster = cluster_assignments[this_cube]

        this_key = sum(this_cube)

        for other_cube in cubes[i + 1 :]:
            other_cluster = cluster_assignments.get(other_cube, -1)

            other_key = sum(other_cube)
            if other_key - this_key > 2:
                break

            num_diff_coords: int = 0
            for k, this_axis in enumerate(this_cube):
                other_axis = other_cube[k]
                if this_axis == other_axis:
                    continue
                if abs(this_axis - other_axis) == 1:
                    num_diff_coords += 1
                else:
                    num_diff_coords = 3
                    break

            if num_diff_coords == 1 or (allow_diagonal and num_diff_coords <= 2):
                if num_diff_coords == 1:
                    cluster_contact_surfaces[this_cluster] += 2
                if other_cluster >= 0 and other_cluster != this_cluster:
                    cluster_contact_surfaces[this_cluster] += cluster_contact_surfaces[
                        other_cluster
                    ]
                    cluster_contact_surfaces.pop(other_cluster)
                    for some_cube, some_cluster in cluster_assignments.items():
                        if some_cluster == other_cluster:
                            cluster_assignments[some_cube] = this_cluster
                else:
                    cluster_assignments[other_cube] = this_cluster

    clusters = defaultdict(list)
    for cube, cluster_id in cluster_assignments.items():
        clusters[cluster_id].append(cube)

    cluster_surfaces = {
        cluster_id: len(clusters[cluster_id]) * 6 - contact_surface
        for cluster_id, contact_surface in cluster_contact_surfaces.items()
    }

    clusters_and_surfaces = [
        (cluster, cluster_surfaces[cluster_id])
        for cluster_id, cluster in clusters.items()
    ]

    return clusters_and_surfaces


def is_included_in(cube: Coord, cluster: Cluster) -> bool:
    is_included = True
    for k, this_axis in enumerate(cube):

        is_bounded_on_axis = [False, False]
        for cluster_cube in cluster:

            is_bound_point = True
            for i, other_axis in enumerate(cube):
                if k == i:
                    continue
                if other_axis != cluster_cube[i]:
                    is_bound_point = False
                    break

            if is_bound_point:
                if cluster_cube[k] < this_axis:
                    is_bounded_on_axis[0] = True
                elif cluster_cube[k] > this_axis:
                    is_bounded_on_axis[1] = True
                if all(is_bounded_on_axis):
                    break

            if all(is_bounded_on_axis):
                break

        if not all(is_bounded_on_axis):
            is_included = False
            break

    return is_included


def compute_interior_surface(cluster: Cluster) -> int:
    # key: enveloppe cube, value: number of contact faces with cubes from the cluster
    enveloppe_cubes: Dict[Coord, int] = {}
    for cube in cluster:
        direct_neigh_coords, diagonal_neigh_coords = get_neighbors(cube)
        for enveloppe_cube in direct_neigh_coords + diagonal_neigh_coords:
            if enveloppe_cube in cluster:
                continue
            if enveloppe_cube not in enveloppe_cubes:
                enveloppe_cubes[enveloppe_cube] = 0
            if enveloppe_cube in direct_neigh_coords:
                enveloppe_cubes[enveloppe_cube] += 1

    enveloppe_clusters_and_surfaces = cluster_cubes(
        list(enveloppe_cubes.keys()), allow_diagonal=False
    )

    cluster_surfaces: List[int] = [0] * len(enveloppe_clusters_and_surfaces)
    for k, (enveloppe_cluster, _surface) in enumerate(enveloppe_clusters_and_surfaces):
        for enveloppe_cube in enveloppe_cluster:
            cluster_surfaces[k] += enveloppe_cubes[enveloppe_cube]

    # Remove the external surface
    enclosed_surface = sum(cluster_surfaces) - max(cluster_surfaces)
    return enclosed_surface


def get_neighbors(coord: Coord) -> Tuple[List[Coord], List[Coord]]:
    # Direct neighboring cubes
    direct_neigh_offsets = [
        (0, 0, 1),
        (0, 0, -1),
        (0, 1, 0),
        (0, -1, 0),
        (1, 0, 0),
        (-1, 0, 0),
    ]
    # Diagonal neighboring cubes
    diagonal_neigh_offsets = [
        (0, 1, 1),
        (0, 1, -1),
        (0, -1, 1),
        (0, -1, -1),
        (1, 0, 1),
        (1, 0, -1),
        (-1, 0, 1),
        (-1, 0, -1),
        (1, 1, 0),
        (1, -1, 0),
        (-1, 1, 0),
        (-1, -1, 0),
    ]
    direct_neigh_coords = []
    for neigh_offset in direct_neigh_offsets:
        neigh = list(coord)
        for k, axis in enumerate(neigh_offset):
            neigh[k] += axis
        direct_neigh_coords.append((neigh[0], neigh[1], neigh[2]))
    diagonal_neigh_coords = []
    for neigh_offset in diagonal_neigh_offsets:
        neigh = list(coord)
        for k, axis in enumerate(neigh_offset):
            neigh[k] += axis
        diagonal_neigh_coords.append((neigh[0], neigh[1], neigh[2]))
    return direct_neigh_coords, diagonal_neigh_coords
