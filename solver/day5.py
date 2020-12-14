import numpy as np


def main(input_lines, max_column=8):
    seat_ids = []
    for line in input_lines:
        binary_space_partition_row = [char == 'B' for char in line[0:7]]
        row = space_partition_2_number(binary_space_partition_row)
        binary_space_partition_column = [char == 'R' for char in line[7:10]]
        column = space_partition_2_number(binary_space_partition_column)
        seat_id = row * max_column + column
        seat_ids.append(seat_id)

    return np.max(seat_ids), find_missing_number(seat_ids)


def space_partition_2_number(binary_space_partition, base=2):
    powers = np.array([base**i for i in range(len(binary_space_partition)-1, -1, -1)])
    number_in_base = np.array(binary_space_partition)
    number = np.sum(powers * number_in_base)
    return number


def find_missing_number(numbers):
    # Complexity: N * log(N) + N
    # numbers.sort()
    # for i, number in enumerate(numbers[:-1]):
    #     next_number = numbers[i+1]
    #     if (next_number != number + 1):
    #         return number + 1

    # Complexity: N * log(N) + log(N)
    # numbers.sort()
    # start_idx, end_idx = 0, len(numbers)
    # while (end_idx - start_idx > 1):
    #     mid_idx = int((start_idx + end_idx) / 2)
    #     expected_number = numbers[start_idx] + (mid_idx - start_idx)
    #     if (numbers[mid_idx] > expected_number):
    #         end_idx = mid_idx
    #     else:
    #         start_idx = mid_idx
    # return numbers[start_idx] + 1

    # Complexity: N
    # Space: N
    tot_numbers = len(numbers) + 1
    min_number = numbers[0]
    is_found_numbers = [False] * tot_numbers
    for number in numbers:
        min_number = min(min_number, number)
        is_found_numbers[number % tot_numbers] = True
    for number_i, is_found_number in enumerate(is_found_numbers):
        if not is_found_number:
            min_number_i = min_number % tot_numbers
            number = min_number + (number_i - min_number_i) + tot_numbers * (number_i < min_number_i)
            return number
