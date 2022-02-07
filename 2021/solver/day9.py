def main(input_lines):
    heightmap = parse_heightmap(input_lines)
    part1_answer, part2_answer = find_basins(heightmap)
    return part1_answer, part2_answer


def parse_heightmap(input_lines):
    heightmap = [[int(c) for c in input_line] for input_line in input_lines]
    return heightmap


def find_basins(heightmap, max_height=9):
    # the i-th basin is described by the tuple: (number of points, height of low point)
    basins = []
    # indicate to which basin the points are associated
    basins_clusters = []
    # re-map the basins indices when merging basins
    basins_idx_remap = {}

    for row_idx, row in enumerate(heightmap):
        basins_clusters.append([])
        for col_idx, height in enumerate(row):
            # Skip the highest points: they are not associated with any basins
            if height == max_height:
                basins_clusters[-1].append(-1)
                continue

            # Find the adjacent points' basins
            associated_basins = []
            for neighbour in get_processed_neighbours(row_idx, col_idx):
                neighbour_basin = basins_clusters[neighbour[0]][neighbour[1]]
                if neighbour_basin != -1:
                    associated_basins.append(basins_idx_remap.get(neighbour_basin, neighbour_basin))

            # Create a new basin
            if len(associated_basins) == 0:
                basins.append([0, height])
                basin_idx = len(basins) - 1
            # Associate the point with the existing basin
            elif len(associated_basins) == 1:
                basin_idx = associated_basins[0]
            # Merge the two existing basins now connecting through the current point
            else:  # len(associated_basins) == 2
                if (associated_basins[0] != associated_basins[1]):
                    basin_idx = merge_basins(
                        basins, associated_basins[0], associated_basins[1], basins_idx_remap)

            # Update the associated basin
            update_basin(basins, basins_clusters, basin_idx, height)

    # Clean-up: filter merged basins ; sort the basins by increasing sizes
    basins = sorted([basin for basin in basins if basin is not None])

    risk_levels_sum = sum([1 + basin[1] for basin in basins])
    three_largest_basins_sizes_prod = basins[-1][0] * basins[-2][0] * basins[-3][0]

    return risk_levels_sum, three_largest_basins_sizes_prod


def get_processed_neighbours(row_idx, col_idx):
    neighbours = []
    if row_idx > 0:
        neighbours.append((row_idx - 1, col_idx))
    if col_idx > 0:
        neighbours.append((row_idx, col_idx - 1))
    return neighbours


def update_basin(basins, basins_clusters, basin_idx, height):
    basins[basin_idx][0] += 1
    basins[basin_idx][1] = min(basins[basin_idx][1], height)
    basins_clusters[-1].append(basin_idx)


def merge_basins(basins, first_basin_idx, second_basin_idx, basins_idx_remap):
    new_basin_idx = min(first_basin_idx, second_basin_idx)
    old_basin_idx = max(first_basin_idx, second_basin_idx)

    basins[new_basin_idx][0] += basins[old_basin_idx][0]
    basins[new_basin_idx][1] = min(basins[new_basin_idx][1], basins[old_basin_idx][1])
    basins[old_basin_idx] = None

    basins_idx_remap[old_basin_idx] = new_basin_idx
    for basin_idx, actual_basin_idx in basins_idx_remap.items():
        if actual_basin_idx == old_basin_idx:
            basins_idx_remap[basin_idx] = new_basin_idx
    return new_basin_idx
