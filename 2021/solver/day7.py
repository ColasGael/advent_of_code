def main(input_lines):
    horizontal_positions = parse_horizontal_position(input_lines)

    part1_answer = part1_fuel_cost(horizontal_positions)
    part2_answer = part2_fuel_cost(horizontal_positions)

    return part1_answer, part2_answer


def parse_horizontal_position(input_lines):
    horizontal_positions = [
        int(horizontal_position) for horizontal_position in input_lines[0].split(",")
    ]
    horizontal_positions.sort()
    return horizontal_positions


def compute_median(values):
    """
    Assumption: 'values' is sorted in increasing order.
    """
    median_idx = len(values) // 2 - 1
    if len(values) % 2 == 0:
        median = 0.5 * (values[median_idx] + values[median_idx + 1])
    else:
        median = values[median_idx]
    return median


def part1_fuel_cost(horizontal_positions):
    """Fuel cost = absolute value of displacement : c(xi) = abs(x - xi)

    Constraint: x is an int.

    The value that minimizes the sum of absolute differences (L1-norm) is the: median.
    """
    median = round(compute_median(horizontal_positions))
    min_fuel_cost = sum(
        abs(median - horizontal_position)
        for horizontal_position in horizontal_positions
    )
    return int(min_fuel_cost)


def compute_mean(values):
    n_values = len(values)
    mean = float(sum(values)) / n_values
    return mean


def part2_fuel_cost(horizontal_positions):
    """Fuel cost : c(xi) = sum(j = 0 -> abs(x - xi) ; j) = 0.5 * ((x - xi)^2 + abs(x - xi))

    Constraint: x is an int.

    The value that minimizes the sum of squared differences (L2-norm) is the: mean +/- 1
    """
    mean = int(round(compute_mean(horizontal_positions)))
    min_fuel_cost = None
    for min_target in range(mean - 1, mean + 2):
        fuel_cost = sum(
            0.5
            * (
                (min_target - horizontal_position) ** 2
                + abs(min_target - horizontal_position)
            )
            for horizontal_position in horizontal_positions
        )
        if min_fuel_cost is None:
            min_fuel_cost = fuel_cost
        min_fuel_cost = min(min_fuel_cost, fuel_cost)
    return int(min_fuel_cost)
