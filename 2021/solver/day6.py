def main(input_lines):
    internal_timer_counts = parse_internal_timers(input_lines)

    part1_answer = reproduce(internal_timer_counts, 80)
    part2_answer = reproduce(internal_timer_counts, 256)

    return part1_answer, part2_answer


def parse_internal_timers(input_lines):
    # internal_timer_counts[i] = number of lanternfishes with an internal timer of i days
    internal_timer_counts = [0] * 9
    for internal_timer in input_lines[0].split(","):
        internal_timer_counts[int(internal_timer)] += 1
    return internal_timer_counts


def reproduce(internal_timer_counts, n_days):
    for _i in range(n_days):
        internal_timer_counts = step(internal_timer_counts)
    n_lanterfishes = sum(internal_timer_counts)
    return n_lanterfishes


def step(internal_timer_counts):
    new_internal_timer_counts = [0] * 9
    new_internal_timer_counts[0:-1] = internal_timer_counts[1:]
    new_internal_timer_counts[6] += internal_timer_counts[0]
    new_internal_timer_counts[8] = internal_timer_counts[0]
    return new_internal_timer_counts
