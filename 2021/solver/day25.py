def main(input_lines):
    map = parse_map(input_lines)

    part1_answer = converge(map)
    part2_answer = 49  # stars

    return part1_answer, part2_answer


def parse_map(input_lines):
    map = [list(input_line.strip()) for input_line in input_lines]
    return map


def step(map, empty_value=".", east_value=">", south_value="v"):
    has_moved = False

    new_map = [[value for value in row] for row in map]
    # First move the east-facing herd
    for row_idx, row in enumerate(map):
        for col_idx, value in enumerate(row):
            prev_col_idx = col_idx - 1
            prev_col_value = row[prev_col_idx]
            if (value == empty_value) and (prev_col_value == east_value):
                new_map[row_idx][prev_col_idx] = empty_value
                new_map[row_idx][col_idx] = east_value
                has_moved = True

    map = new_map
    new_map = [[value for value in row] for row in map]
    # Then move the (potential) south-facing herd
    for row_idx, row in enumerate(map):
        prev_row_idx = row_idx - 1
        for col_idx, value in enumerate(row):
            prev_row_value = map[prev_row_idx][col_idx]
            if (value == empty_value) and (prev_row_value == south_value):
                new_map[prev_row_idx][col_idx] = empty_value
                new_map[row_idx][col_idx] = south_value
                has_moved = True

    return has_moved, new_map


def converge(map):
    has_moved = True
    n_steps = 0
    while has_moved:
        has_moved, map = step(map)
        n_steps += 1
    return n_steps
