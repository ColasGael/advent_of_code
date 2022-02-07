def main(input_lines):
    risk_levels = parse_map(input_lines)
    part1_answer = a_star(risk_levels)

    risk_levels_extended = extend_map(risk_levels)
    part2_answer = a_star(risk_levels_extended)

    return part1_answer, part2_answer


def parse_map(input_lines):
    risk_levels = [
        [int(risk_level) for risk_level in row]
        for row in input_lines
    ]
    return risk_levels


def extend_map(risk_levels, n_repeats=5):
    risk_levels_extended = []
    for i in range(n_repeats):
        for row_idx in range(len(risk_levels)):
            risk_levels_extended.append([])
            for j in range(n_repeats):
                for col_idx in range(len(risk_levels[0])):
                    new_risk_level = (risk_levels[row_idx][col_idx] + i + j - 1) % 9 + 1
                    risk_levels_extended[-1].append(new_risk_level)
    return risk_levels_extended


def a_star(risk_levels):
    # Definition of the problem variables
    start_point = (0, 0)
    end_point = (len(risk_levels) - 1, len(risk_levels[0]) - 1)

    # Initialization
    current_point = start_point
    g_scores = {start_point: 0}
    f_scores = {start_point: 0}

    while current_point != end_point:
        for neighbour in get_neighbours(current_point, len(risk_levels), len(risk_levels[0])):
            tmp_g_score = g_scores[current_point] + distance(current_point, neighbour, risk_levels)
            if (neighbour in g_scores) and (g_scores[neighbour] <= tmp_g_score):
                continue
            # Update the estimates with the shortest path found
            g_scores[neighbour] = tmp_g_score
            f_scores[neighbour] = tmp_g_score + compute_h_score(current_point, neighbour)
        # Found shortest to 'current_point'
        current_point = min(f_scores.keys(), key=lambda point: f_scores[point])
        f_scores.pop(current_point)

    return g_scores[end_point]


def get_neighbours(point, max_row, max_col):
    row_idx, col_idx = point
    neighbours = []
    if row_idx > 0:
        neighbours.append((row_idx - 1, col_idx))
    if row_idx < max_row - 1:
        neighbours.append((row_idx + 1, col_idx))
    if col_idx > 0:
        neighbours.append((row_idx, col_idx - 1))
    if col_idx < max_col - 1:
        neighbours.append((row_idx, col_idx + 1))
    return neighbours


def distance(point_a, point_b, risk_levels):
    return risk_levels[point_b[0]][point_b[1]]


def compute_h_score(point, end_point):
    '''Lower bound on the cost of the shortest path from point to end point.
    '''
    dx = abs(end_point[0] - point[0])
    dy = abs(end_point[1] - point[1])
    return dx + dy
