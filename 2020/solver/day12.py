import re


def main(input_lines, cardinal_points=['N', 'E', 'S', 'W'], initial_position=(0, 0), initial_orientation=1, waypoint_position=(1, 10)):
    SUPPORTED_ACTIONS = cardinal_points + ['L', 'R', 'F']
    INSTRUCTION_PATTERN = re.compile("(?P<action>[{}])(?P<value>\d+)".format("".join(SUPPORTED_ACTIONS)))

    actions = []
    for line in input_lines:
        m = INSTRUCTION_PATTERN.match(line)
        actions .append((m.group('action'), int(m.group('value'))))

    part1_position, part1_orientation = initial_position, initial_orientation
    part2_position, part2_orientation = initial_position, initial_orientation
    for action, value in actions:
        part1_position, part1_orientation = part1_apply_action(action, value, cardinal_points, part1_position, part1_orientation)
        part2_position, part2_orientation, waypoint_position = part2_apply_action(action, value, cardinal_points, part2_position, part2_orientation, waypoint_position)

    return manhattan_distance(part1_position), manhattan_distance(part2_position)


def manhattan_distance(position):
    return abs(position[0]) + abs(position[1])


def part1_apply_action(action, value, cardinal_points, position, orientation):
    if action == 'F':
        action = cardinal_points[orientation]

    if action == cardinal_points[0]:
        position = (position[0] + value, position[1])
    elif action == cardinal_points[2]:
        position = (position[0] - value, position[1])
    elif action == cardinal_points[1]:
        position = (position[0], position[1] + value)
    elif action == cardinal_points[3]:
        position = (position[0], position[1] - value)
    elif action == 'R':
        orientation = (orientation + int(value / 90)) % len(cardinal_points)
    elif action == 'L':
        orientation = (orientation - int(value / 90)) % len(cardinal_points)

    return position, orientation


def part2_apply_action(action, value, cardinal_points, position, orientation, waypoint_position):
    if action == cardinal_points[0]:
        waypoint_position = (waypoint_position[0] + value, waypoint_position[1])
    elif action == cardinal_points[2]:
        waypoint_position = (waypoint_position[0] - value, waypoint_position[1])
    elif action == cardinal_points[1]:
        waypoint_position = (waypoint_position[0], waypoint_position[1] + value)
    elif action == cardinal_points[3]:
        waypoint_position = (waypoint_position[0], waypoint_position[1] - value)

    elif action in ['R', 'L']:
        if value == 180:
            waypoint_position = (-waypoint_position[0], -waypoint_position[1])
        elif (action == 'R' and value == 90) or (action == 'L' and value == 270):
            waypoint_position = (-waypoint_position[1], waypoint_position[0])
        elif (action == 'L' and value == 90) or (action == 'R' and value == 270):
            waypoint_position = (waypoint_position[1], -waypoint_position[0])

    elif action == 'F':
        position = (position[0] + waypoint_position[0] * value, position[1] + waypoint_position[1] * value)

    return position, orientation, waypoint_position
