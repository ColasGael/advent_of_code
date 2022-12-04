def main(input_lines, part1_n_games=100, part2_n_games=10000000, part2_n_cups=1000000):
    part1_cups = parse_input(input_lines)
    part1_answer = "".join([str(cup) for cup in play(part1_cups, part1_n_games)[1:]])

    part2_cups = part1_cups + list(range(len(part1_cups) + 1, part2_n_cups + 1))
    part2_final_cup_order = play(part2_cups, part2_n_games)
    part2_answer = part2_final_cup_order[1] * part2_final_cup_order[2]

    return part1_answer, part2_answer


def parse_input(input_lines):
    cups = [int(char) for char in input_lines[0]]
    return cups


def play(cups, n_games):
    current_cup, next_cups = start(cups)
    for _i in range(n_games):
        current_cup, next_cups = move_cups(current_cup, next_cups)
    cups = find_final_cup_order(next_cups)
    return cups


def start(cups):
    cups = [cup - 1 for cup in cups]
    next_cups = [None] * len(cups)
    for idx, cup in enumerate(cups[:-1]):
        next_cups[cup] = cups[idx + 1]
    next_cups[cups[-1]] = cups[0]
    return cups[0], next_cups


def move_cups(current_cup, next_cups, n_cups_removed=3):
    removed_cups = []
    removed_cup = next_cups[current_cup]
    for _i in range(n_cups_removed):
        removed_cups.append(removed_cup)
        removed_cup = next_cups[removed_cup]
    next_cups[current_cup] = removed_cup

    destination_cup = (current_cup - 1) % len(next_cups)
    while destination_cup in removed_cups:
        destination_cup = (destination_cup - 1) % len(next_cups)
    next_cups[removed_cups[-1]] = next_cups[destination_cup]
    next_cups[destination_cup] = removed_cups[0]

    return removed_cup, next_cups


def find_final_cup_order(next_cups):
    cups = [1]
    current_cup = next_cups[0]
    while current_cup != 0:
        cups.append(current_cup + 1)
        current_cup = next_cups[current_cup]
    return cups


def play_naive(cups, n_games):
    for _i in range(n_games):
        cups = move_cups_naive(cups)
    cups = find_final_cup_order_naive(cups)
    return cups


def move_cups_naive(cups, n_cups_removed=3):
    current_cup = cups[0]
    removed_cups = cups[1 : 1 + n_cups_removed]
    remaining_cups = cups[1 + n_cups_removed :]

    destination_cup_idx, max_cup_idx = None, 0
    for idx, cup in enumerate(remaining_cups):
        if current_cup > cup:
            if (destination_cup_idx is None) or (
                cup > remaining_cups[destination_cup_idx]
            ):
                destination_cup_idx = idx
        elif cup > remaining_cups[max_cup_idx]:
            max_cup_idx = idx
    if destination_cup_idx is None:
        destination_cup_idx = max_cup_idx

    new_cups = (
        remaining_cups[: destination_cup_idx + 1]
        + removed_cups
        + remaining_cups[destination_cup_idx + 1 :]
        + [current_cup]
    )
    return new_cups


def find_final_cup_order_naive(cups):
    first_idx = cups.index(1)
    cups = cups[first_idx:] + cups[:first_idx]
    return cups
