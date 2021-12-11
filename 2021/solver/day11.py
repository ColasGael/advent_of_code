def main(input_lines):
    initial_state = parse_grid(input_lines)
    part1_answer, part2_answer = simulate(initial_state)
    return part1_answer, part2_answer


def parse_grid(input_lines):
    grid = []
    for input_line in input_lines:
        grid.append([])
        for c in input_line.strip():
            grid[-1].append(int(c))
    return grid


def simulate(state, n_steps=100):
    n_octopuses = len(state) * len(state[0])
    i = 0
    tot_flashes_cnt, flashes_cnt = 0, 0
    while flashes_cnt != n_octopuses:
        flashes_cnt = step(state)
        if i < n_steps:
            tot_flashes_cnt += flashes_cnt
        i += 1
    return tot_flashes_cnt, i


def step(state):
    max_row, max_col = len(state), len(state[0])
    backlog_octopuses = [
        (row_idx, col_idx) for row_idx in range(max_row) for col_idx in range(max_col)
    ]
    flashed_octopuses = []
    while len(backlog_octopuses) > 0:
        row_idx, col_idx = backlog_octopuses.pop()
        if (row_idx, col_idx) in flashed_octopuses:
            continue
        energy_lvl = state[row_idx][col_idx]
        if energy_lvl < 9:
            state[row_idx][col_idx] += 1
        else:
            state[row_idx][col_idx] = 0
            flashed_octopuses.append((row_idx, col_idx))
            backlog_octopuses.extend(get_neighbours(row_idx, col_idx, max_row, max_col))
    return len(flashed_octopuses)


def get_neighbours(row_idx, col_idx, max_row, max_col):
    neighbours = []
    if row_idx > 0:
        neighbours.append((row_idx - 1, col_idx))
    if row_idx < max_row - 1:
        neighbours.append((row_idx + 1, col_idx))
    if col_idx > 0:
        neighbours.append((row_idx, col_idx - 1))
    if col_idx < max_col - 1:
        neighbours.append((row_idx, col_idx + 1))
    if (row_idx > 0) and (col_idx > 0):
        neighbours.append((row_idx - 1, col_idx - 1))
    if (row_idx > 0) and (col_idx < max_col - 1):
        neighbours.append((row_idx - 1, col_idx + 1))
    if (row_idx < max_row - 1) and (col_idx > 0):
        neighbours.append((row_idx + 1, col_idx - 1))
    if (row_idx < max_row - 1) and (col_idx < max_col - 1):
        neighbours.append((row_idx + 1, col_idx + 1))
    return neighbours
