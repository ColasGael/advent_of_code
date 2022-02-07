import re

from .day1 import is_sum_of_2


def main(input_lines, preamble_len=25):
    numbers = [int(line) for line in input_lines]

    for i, number in enumerate(numbers):
        if (i < preamble_len):
            continue
        if not is_sum_of_2(number, sorted(numbers[i - preamble_len: i])):
            break

    slice_sum = find_slice_sum(number, numbers)
    part2_answer = min(slice_sum) + max(slice_sum)

    return number, part2_answer


def find_slice_sum(target_number, numbers):
    i = 0
    slice_sum = 0
    for j, number in enumerate(numbers):
        if (number == target_number):
            i = j + 1
            slice_sum = 0

        slice_sum += number
        while (slice_sum > target_number):
            slice_sum -= numbers[i]
            i += 1

        if (slice_sum == target_number):
            return numbers[i: j+1]
