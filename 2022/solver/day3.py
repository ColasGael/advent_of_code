import functools


def main(input_lines):
    rucksacks = []
    for line in input_lines:
        n = len(line)  # pylint: disable=invalid-name
        # Each compartiment stores the same number of items
        assert n % 2 == 0
        rucksacks.append((list(line[: n // 2]), list(line[n // 2 :])))

    part1_answer = solve_part_1(rucksacks)
    part2_answer = solve_part_2(rucksacks)
    return part1_answer, part2_answer


def priority(char):
    """Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.
    """
    ref_score = 1
    ref_char = "a"
    if not char.islower():
        ref_score += 26
        ref_char = "A"
    return ord(char) - ord(ref_char) + ref_score


def compute_score(misplaced_item_types):
    return sum(map(priority, misplaced_item_types))


def find_misplaced_item_type(rucksack):
    assert len(rucksack) == 2
    compartiment_1, compartiment_2 = rucksack
    # Each item type should only be present in 1 of the compartiment
    misplaced_item_types = set(compartiment_1).intersection(set(compartiment_2))
    assert len(misplaced_item_types) == 1
    return misplaced_item_types.pop()


def solve_part_1(rucksacks):
    return compute_score(map(find_misplaced_item_type, rucksacks))


def find_badge(group_rucksacks):
    assert len(group_rucksacks) == 3
    # The badge is only item type carried in all three rucksacks from the group
    badges = functools.reduce(
        set.intersection,
        map(
            lambda rucksack: set.union(set(rucksack[0]), set(rucksack[1])),
            group_rucksacks,
        ),
    )
    assert len(badges) == 1
    return badges.pop()


def solve_part_2(rucksacks):
    n = len(rucksacks)  # pylint: disable=invalid-name
    assert n % 3 == 0
    badges = []
    for i in range(0, n, 3):
        badges.append(find_badge(rucksacks[i : i + 3]))
    return compute_score(badges)
