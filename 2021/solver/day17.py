def main(input_lines):
    target_area = parse_target_area(input_lines)

    max_initial_y_speed = find_max_y_speed(target_area)
    part1_answer = int(max_initial_y_speed * (max_initial_y_speed + 1) / 2)
    part2_answer = len(find_all_valid_initial_speeds(target_area))

    return part1_answer, part2_answer


def parse_target_area(input_lines):
    x_area_block, y_area_block = input_lines[0].split(":")[-1].strip().split(" ")
    x_area = x_area_block[2:-1].split("..")
    y_area = y_area_block[2:].split("..")
    target_area = ((int(x_area[0]), int(x_area[1])), (int(y_area[0]), int(y_area[1])))
    return target_area


def find_root(c):
    x_root = 0.5 * (-1 + (1 - 4 * c) ** 0.5)
    if int(x_root) == x_root:
        return int(x_root)
    else:
        return int(x_root) + 1


def find_max_y_speed(target_area):
    # 1. Find the minimum initial x-velocity that allows to reach the target area
    # Why? So it takes the maximum number of steps to reach it.
    # With the minimum speed, we reach the target area with current x-velocity: initial_x_speed = 0.
    # Since the x-velocity decreases by 1 at each step, the x-distance crossed is:
    # tot_x_distance = (initial_x_speed + 1) * initial_x_speed / 2
    # And we need to reach the target area: tot_x_distance >= target_area_min_x
    # The solution is the first integer greater then the positive root of the following polynomial:
    # initial_x_speed ** 2 + initial_x_speed - 2 * target_area_min_x = 0
    target_area_min_x = target_area[0][0]
    min_initial_x_speed = find_root(- 2 * target_area_min_x)

    # 2. Find the highest initial y-velocity
    # The maximum initial y-velocity candidate is the velocity
    # that would cause the probe to overshoot the target area in one step.
    # In x = 0, coming down, the probe has y-velocity: - initial_y_speed.
    # So the maximum initial y-velocity candidate is: - target_area_min_y
    highest_valid_initial_y_speed = -1
    target_area_min_y = target_area[1][0]
    for initial_y_speed in range(-target_area_min_y + 1):
        is_valid = is_valid_y_speed(initial_y_speed, target_area)
        if is_valid:
            highest_valid_initial_y_speed = initial_y_speed
    return highest_valid_initial_y_speed


def is_valid_y_speed(initial_y_speed, target_area):
    # 1. Find the timestamp where the highest y-position is reached
    highest_y_t = initial_y_speed
    highest_y = initial_y_speed * (initial_y_speed + 1) / 2
    # 2. Compute the minimum time to reach the target area y-span
    # At the timestamp where we reached the highest point the y-velocity is: 0.
    # Then it increases by 1 at each step, the y-velocity after t steps is: t.
    # So the timestamp difference to reach the target area is:
    # tot_y_distance = (in_area_t + 1) * in_area_t / 2.
    # And we need to reach the target area: tot_y_distance >= highest_y - target_area_max_y
    # The solution is the first integer greater then the positive root of the following polynomial:
    # in_area_t ** 2 + in_area_t - 2 * (highest_y - target_area_max_y) = 0
    target_area_max_y = target_area[1][1]
    tot_y_distance = highest_y - target_area_max_y
    in_area_t = find_root(- 2 * tot_y_distance)
    # 3. Check that the target area was not overshooted
    y_coord = highest_y - in_area_t * (in_area_t + 1) / 2
    target_area_min_y = target_area[1][0]

    return (y_coord >= target_area_min_y)


def find_all_valid_initial_speeds(target_area):
    all_valid_initial_speeds = []

    target_area_min_x, target_area_max_x = target_area[0]
    min_initial_x_speed = find_root(- 2 * target_area_min_x)
    max_initial_x_speed = target_area_max_x
    for initial_x_speed in range(min_initial_x_speed, max_initial_x_speed + 1):
        target_area_min_y, target_area_max_y = target_area[1]
        for initial_y_speed in range(target_area_min_y, -target_area_min_y + 1):
            if are_valid_initial_speeds(initial_x_speed, initial_y_speed, target_area):
                all_valid_initial_speeds.append((initial_x_speed, initial_y_speed))

    return all_valid_initial_speeds


def are_valid_initial_speeds(initial_x_speed, initial_y_speed, target_area):
    target_area_min_x, target_area_max_x = target_area[0]

    if initial_y_speed > 0:
        highest_y_t = initial_y_speed
        highest_y = initial_y_speed * (initial_y_speed + 1) / 2
    else:
        highest_y_t = initial_y_speed
        highest_y = (-initial_y_speed - 1) * (-initial_y_speed - 1 + 1) / 2

    target_area_min_y, target_area_max_y = target_area[1]
    in_area_y_min_t = find_root(- 2 * (highest_y - target_area_max_y))
    in_area_y_max_t = find_root(- 2 * (highest_y - target_area_min_y))

    for in_area_t in range(in_area_y_min_t, in_area_y_max_t + 1):
        y_coord = highest_y - in_area_t * (in_area_t + 1) / 2
        if not (target_area_min_y <= y_coord <= target_area_max_y):
            continue
        t = min(highest_y_t + 1 + in_area_t, initial_x_speed)
        x_coord = t * (initial_x_speed + (initial_x_speed - t + 1)) / 2
        if not (target_area_min_x <= x_coord <= target_area_max_x):
            continue
        return True
    return False
