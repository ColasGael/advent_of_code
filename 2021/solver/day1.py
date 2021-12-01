def main(input_lines, window_size=3):
    depth_measurements = [int(line) for line in input_lines]

    part1_answer = compute_num_measurement_increases(depth_measurements)
    # Remark: this is equivalent to:
    # part1_answer = compute_num_window_increases(depth_measurements, 1)
    part2_answer = compute_num_window_increases(depth_measurements, window_size)
    return part1_answer, part2_answer


def compute_num_measurement_increases(depth_measurements):
    num_increases = 0
    for i, depth_measurement in enumerate(depth_measurements[:-1]):
        if depth_measurements[i + 1] > depth_measurement:
            num_increases += 1
    return num_increases


def compute_num_window_increases(depth_measurements, window_size):
    # Since we are considering CONSECUTIVE sums (sliding window).
    # a + b + c < b + c + d is equivalent to: a < d
    # We do not need to actually compute the sums.
    # Instead we can just compare elements that are 'window_size' apart.
    num_increases = 0
    for i, depth_measurement in enumerate(depth_measurements[:-window_size]):
        if depth_measurements[i + window_size] > depth_measurement:
            num_increases += 1
    return num_increases
