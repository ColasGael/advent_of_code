def main(input_lines):
    snailfish_nums = [parse_snailfish_num(input_line) for input_line in input_lines]
    part1_answer = compute_magnitude(compute_snailfish_sum(snailfish_nums))

    all_two_number_sums = [
        compute_snailfish_sum([snailfish_num_1, snailfish_num_2])
        for snailfish_num_1 in snailfish_nums
        for snailfish_num_2 in snailfish_nums
        if (snailfish_num_1 != snailfish_num_2)
    ]
    part2_answer = max(map(compute_magnitude, all_two_number_sums))

    return part1_answer, part2_answer


def parse_snailfish_num(input_line):
    # regular number
    try:
        return int(input_line)
    except ValueError:
        pass

    # Find the middle of the pair: same number of opening and closing brackets
    opening_bracket_num = 0
    for i, char in enumerate(input_line[1:-1], start=1):
        if char == "[":
            opening_bracket_num += 1
        elif char == "]":
            opening_bracket_num -= 1
        elif (char == ",") and (opening_bracket_num == 0):
            left_snailfish_num = parse_snailfish_num(input_line[1:i])
            right_snailfish_num = parse_snailfish_num(input_line[i + 1 : -1])
            return [left_snailfish_num, right_snailfish_num]

    raise RuntimeError("Cannot parse valid snailfish_num from: %s" % input_line)


# pylint: disable=invalid-name
def deepcopy(l):
    if isinstance(l, int):
        return l
    return [deepcopy(e) for e in l]


# pylint: enable=invalid-name


def compute_magnitude(snailfish_num):
    if isinstance(snailfish_num, int):
        return snailfish_num
    return 3 * compute_magnitude(snailfish_num[0]) + 2 * compute_magnitude(
        snailfish_num[1]
    )


def reduce(snailfish_num):
    open_snailfish_nums = [(1, 1, snailfish_num), (1, 0, snailfish_num)]

    last_snailfish_regular_num_info = None
    exploded_pair = None

    split_snailfish_regular_num_info = None

    while open_snailfish_nums:
        current_depth, side, current_snailfish_num_parent = open_snailfish_nums.pop()
        current_snailfish_num = current_snailfish_num_parent[side]

        if isinstance(current_snailfish_num, int):
            last_snailfish_regular_num_info = (side, current_snailfish_num_parent)
            if exploded_pair is not None:
                # pylint: disable=unsubscriptable-object
                current_snailfish_num_parent[side] += exploded_pair[1]
                # pylint: enable=unsubscriptable-object
                break
            if (split_snailfish_regular_num_info is None) and (
                current_snailfish_num >= 10
            ):
                split_snailfish_regular_num_info = (side, current_snailfish_num_parent)

        elif (exploded_pair is None) and (current_depth == 4):
            current_snailfish_num_parent[side] = 0

            exploded_pair = current_snailfish_num
            if last_snailfish_regular_num_info is not None:
                (  # pylint: disable=unpacking-non-sequence
                    side,
                    last_snailfish_regular_num_parent,
                ) = last_snailfish_regular_num_info
                last_snailfish_regular_num_parent[side] += exploded_pair[0]

        else:
            open_snailfish_nums.append((current_depth + 1, 1, current_snailfish_num))
            open_snailfish_nums.append((current_depth + 1, 0, current_snailfish_num))

    if exploded_pair is None:
        if split_snailfish_regular_num_info is not None:
            (
                side,
                split_snailfish_regular_num_parent,
            ) = split_snailfish_regular_num_info
            split_snailfish_regular_num = split_snailfish_regular_num_parent[side]
            half_snailfish_num = int(0.5 * split_snailfish_regular_num)
            split_snailfish_regular_num_parent[side] = [
                half_snailfish_num,
                split_snailfish_regular_num - half_snailfish_num,
            ]
            return True

    else:
        return True


def compute_snailfish_sum(snailfish_nums):
    snailfish_sum = deepcopy(snailfish_nums[0])
    for snailfish_num in snailfish_nums[1:]:
        new_snailfish_sum = [snailfish_sum, deepcopy(snailfish_num)]
        while reduce(new_snailfish_sum):
            pass
        snailfish_sum = new_snailfish_sum
    return snailfish_sum
