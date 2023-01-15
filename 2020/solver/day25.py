def main(input_lines, subject_number=7, base=20201227):
    card_public_key, door_public_key = parse_input(input_lines)

    card_loop_size = find_loop_size(card_public_key, subject_number, base)
    door_loop_size = find_loop_size(door_public_key, subject_number, base)
    card_encription_key = compute_encription_key(door_public_key, card_loop_size, base)
    door_encription_key = compute_encription_key(card_public_key, door_loop_size, base)
    assert card_encription_key == door_encription_key
    part1_answer = card_encription_key

    part2_answer = "unspecified"

    return part1_answer, part2_answer


def parse_input(input_lines):
    card_public_key = int(input_lines[0])
    door_public_key = int(input_lines[1])
    return card_public_key, door_public_key


def find_loop_size(public_key, subject_number, base):
    number = 1
    loop_size = 0
    while number != public_key:
        number = step(number, subject_number, base)
        loop_size += 1
    return loop_size


def step(number, subject_number, base):
    number *= subject_number
    number = number % base
    return number


def compute_encription_key(this_public_key, other_loop_size, base):
    encription_key = 1
    for _i in range(other_loop_size):
        encription_key = step(encription_key, this_public_key, base)
    return encription_key
