import re


PASSWORD_CHECK_PATTERN = re.compile(
    r"(?P<lower_bound>\d+)-(?P<upper_bound>\d+)\s(?P<target_char>[a-z]):\s(?P<password>[a-z]+)"
)


def main(input_lines):
    part1_n_valid_password = 0
    part2_n_valid_password = 0
    for line in input_lines:
        match = PASSWORD_CHECK_PATTERN.match(line)
        if not match:
            raise RuntimeError("Input line could not be parsed: {}".format(line))

        password = (
            int(match.group("lower_bound")),
            int(match.group("upper_bound")),
            match.group("target_char"),
            match.group("password"),
        )
        if part1_is_valid_password(*password):
            part1_n_valid_password += 1
        if part2_is_valid_password(*password):
            part2_n_valid_password += 1

    return part1_n_valid_password, part2_n_valid_password


def part1_is_valid_password(lower_bound, upper_bound, target_char, password):
    char_count = password.count(target_char)
    return lower_bound <= char_count <= upper_bound


def part2_is_valid_password(first_index, second_index, target_char, password):
    return (password[first_index - 1] == target_char) ^ (
        password[second_index - 1] == target_char
    )  # XOR
