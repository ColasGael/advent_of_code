def main(input_lines, part1_max_round=2020, part2_max_round=30000000):
    initial_numbers = [
        int(initial_number) for initial_number in input_lines[0].split(",")
    ]

    last_spoken = [None] * part2_max_round
    n_round = number = None
    for n_round, number in enumerate(initial_numbers):
        last_spoken[number] = n_round

    while n_round < part1_max_round - 1:
        number, n_round = step(last_spoken, number, n_round)
    part1_answer = number

    while n_round < part2_max_round - 1:
        number, n_round = step(last_spoken, number, n_round)
    part2_answer = number

    return part1_answer, part2_answer


def step(last_spoken, prev_number, n_round):
    next_number = (
        (n_round - last_spoken[prev_number])
        if (last_spoken[prev_number] is not None)
        else 0
    )
    last_spoken[prev_number] = n_round
    n_round += 1
    return next_number, n_round
