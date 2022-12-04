def main(input_lines):
    vent_lines, max_x, max_y = parse_vent_lines(input_lines)

    part1_answer = count_intersections(vent_lines, max_x, max_y, ignore_diagonal=True)
    part2_answer = count_intersections(vent_lines, max_x, max_y, ignore_diagonal=False)

    return part1_answer, part2_answer


def parse_vent_lines(input_lines):
    vent_lines = []
    max_x, max_y = 0, 0
    for input_line in input_lines:
        vent_line = []
        # Extract the end points of the vent line
        pieces = input_line.split(" ")
        for i in (0, -1):
            line_point_x, line_point_y = pieces[i].split(",")
            line_end_coords = (int(line_point_x), int(line_point_y))
            vent_line.append(line_end_coords)
        # Choose the start point to be the point with lower x-coord
        if vent_line[0][0] > vent_line[1][0]:
            vent_line = [vent_line[1], vent_line[0]]
        vent_lines.append(vent_line)
        max_x = max(max(max_x, vent_line[0][0]), vent_line[1][0])
        max_y = max(max(max_y, vent_line[0][1]), vent_line[1][1])
    return vent_lines, max_x, max_y


def count_intersections(vent_lines, max_x, max_y, ignore_diagonal=False):
    n_intersections = 0
    # Build the map of the sea floor
    intersections_map = [[0] * (max_x + 1) for i in range(max_y + 1)]
    # pylint: disable=invalid-name
    for vent_line in vent_lines:
        # vertical line: constant x
        if vent_line[0][0] == vent_line[1][0]:
            x = vent_line[0][0]
            start_y = min(vent_line[0][1], vent_line[1][1])
            end_y = max(vent_line[0][1], vent_line[1][1])
            for y in range(start_y, end_y + 1):
                # Check if the vent line is intersecting with a previously added vent line
                if intersections_map[y][x] == 1:
                    n_intersections += 1
                # Add the current vent line
                intersections_map[y][x] += 1
        # horizontal line: constant y
        elif vent_line[0][1] == vent_line[1][1]:
            y = vent_line[0][1]
            start_x = min(vent_line[0][0], vent_line[1][0])
            end_x = max(vent_line[0][0], vent_line[1][0])
            for x in range(start_x, end_x + 1):
                # Check if the vent line is intersecting with a previously added vent line
                if intersections_map[y][x] == 1:
                    n_intersections += 1
                # Add the current vent line
                intersections_map[y][x] += 1
        # diagonal line: slope +/- 1
        elif not ignore_diagonal:
            slope = 1
            if (vent_line[0][1] - vent_line[1][1]) * (
                vent_line[0][0] - vent_line[1][0]
            ) < 0:
                slope = -1
            start_x = min(vent_line[0][0], vent_line[1][0])
            end_x = max(vent_line[0][0], vent_line[1][0])
            y = slope * min(slope * vent_line[0][1], slope * vent_line[1][1])
            for x in range(start_x, end_x + 1):
                # Check if the vent line is intersecting with a previously added vent line
                if intersections_map[y][x] == 1:
                    n_intersections += 1
                # Add the current vent line
                intersections_map[y][x] += 1
                y += slope
    # pylint: enable=invalid-name
    return n_intersections
