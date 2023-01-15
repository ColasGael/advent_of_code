def main(input_lines):
    ocean_map = parse_map(input_lines)

    part1_answer = converge(ocean_map)
    part2_answer = "unspecified"

    return part1_answer, part2_answer


def parse_map(input_lines):
    ocean_map = [list(input_line) for input_line in input_lines]
    return ocean_map


def step(old_map, empty_value=".", east_value=">", south_value="v"):
    has_moved = False

    new_map = [list(row) for row in old_map]
    # First move the east-facing herd
    for row_idx, row in enumerate(old_map):
        for col_idx, value in enumerate(row):
            prev_col_idx = col_idx - 1
            prev_col_value = row[prev_col_idx]
            if (value == empty_value) and (prev_col_value == east_value):
                new_map[row_idx][prev_col_idx] = empty_value
                new_map[row_idx][col_idx] = east_value
                has_moved = True

    old_map = new_map
    new_map = [list(row) for row in old_map]
    # Then move the (potential) south-facing herd
    for row_idx, row in enumerate(old_map):
        prev_row_idx = row_idx - 1
        for col_idx, value in enumerate(row):
            prev_row_value = old_map[prev_row_idx][col_idx]
            if (value == empty_value) and (prev_row_value == south_value):
                new_map[prev_row_idx][col_idx] = empty_value
                new_map[row_idx][col_idx] = south_value
                has_moved = True

    return has_moved, new_map


def converge(ocean_map):
    has_moved = True
    n_steps = 0
    while has_moved:
        has_moved, ocean_map = step(ocean_map)
        n_steps += 1
    return n_steps
