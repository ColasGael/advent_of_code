from typing import List, Tuple


File = List[int]


def main(
    input_lines: List[str], decription_key: int = 811589153, part2_num_mixing: int = 10
) -> Tuple[int, int]:
    numbers: File = [int(line) for line in input_lines]

    part1_answer: int = sum(find_grove_coordinates(numbers))

    actual_numbers = [number * decription_key for number in numbers]
    part2_answer: int = sum(
        find_grove_coordinates(actual_numbers, num_mixing=part2_num_mixing)
    )

    return part1_answer, part2_answer


def find_grove_coordinates(numbers: File, num_mixing: int = 1) -> Tuple[int, int, int]:
    numbers_size: int = len(numbers)
    decoded_numbers: File = decode(numbers, num_mixing)
    zero_pos: int = decoded_numbers.index(0)
    grove_coordinates: Tuple[int, int, int] = (
        decoded_numbers[(zero_pos + 1000) % numbers_size],
        decoded_numbers[(zero_pos + 2000) % numbers_size],
        decoded_numbers[(zero_pos + 3000) % numbers_size],
    )
    return grove_coordinates


def decode(numbers: File, num_mixing) -> File:
    numbers_size: int = len(numbers) - 1
    # Make all numbers unique by indexing them
    decoded_numbers: List[Tuple[int, int]] = list(enumerate(numbers))
    for _k in range(num_mixing):
        for i, number in enumerate(numbers):
            number_pos = decoded_numbers.index((i, number))
            decoded_numbers.pop(number_pos)
            new_number_pos = (number_pos + number) % numbers_size
            decoded_numbers.insert(new_number_pos, (i, number))
    # Remove the indices
    return [number for _i, number in decoded_numbers]
