def main(input_lines):
    diagnostic_report = [[int(bit) for bit in diagnostic_line] for diagnostic_line in input_lines]

    gamma_rate, epsilon_rate = analyze_power_consumption(diagnostic_report)
    power_consumption = gamma_rate * epsilon_rate

    oxygen_generator_rating, co2_scrubber_rating = analyze_life_support(diagnostic_report)
    life_support_rating = oxygen_generator_rating * co2_scrubber_rating

    return power_consumption, life_support_rating


def binary_to_int(bin_number):
    # Horner's method for polynomial evaluation
    int_number = 0
    for bit in bin_number:
        int_number = 2 * int_number + bit
    return int_number


def analyze_power_consumption(diagnostic_report):
    '''Find the gamma and epsilon rates from the diagnostic report

    Args:
        diagnostic_report (list of lists of bits, len = n x m)

    Return:
        gamma_rate (int): the i-th bit is the most common element of the report i-th column
        epsilon_rate (int): the i-th bit is the least common element of the report i-th column

    Remark:
        Since each element of the diagnostic_report matrix is a bit (0 or 1),
    If the most common element of a column is 1, then the least common must be 0 (and reciprocally).
    So the binary representations of gamma_rate and epsilon_rate are exactly flipped.
    And they sum to: 111...1 (m bits) = 2^m - 1
    '''
    n = len(diagnostic_report)
    m = len(diagnostic_report[0])

    column_sum = [0] * m
    for diagnostic_line in diagnostic_report:
        for i, bit in enumerate(diagnostic_line):
            column_sum[i] += bit

    most_common_bits = []
    for bit_sum in column_sum:
        most_common_bit = int(bit_sum >= (n + 1) // 2)
        most_common_bits.append(most_common_bit)

    gamma_rate = binary_to_int(most_common_bits)
    epsilon_rate = (2**m - 1) - gamma_rate

    return gamma_rate, epsilon_rate


def find_most_common_bit(bin_numbers, position):
    n_numbers = len(bin_numbers)
    bit_sum = sum([bin_number[position] for bin_number in bin_numbers])
    most_common_bit = int(bit_sum >= (n_numbers + 1) // 2)
    return most_common_bit


def analyze_life_support(diagnostic_report):
    m = len(diagnostic_report[0])

    oxygen_generator_rating_candidates = diagnostic_report
    for position in range(m):
        if len(oxygen_generator_rating_candidates) == 1:
            break
        most_common_bit = find_most_common_bit(oxygen_generator_rating_candidates, position)
        oxygen_generator_rating_candidates = [
            rating_candidate for rating_candidate in oxygen_generator_rating_candidates
            if (rating_candidate[position] == most_common_bit)
        ]
    oxygen_generator_rating = binary_to_int(oxygen_generator_rating_candidates[0])

    co2_scrubber_rating_candidates = diagnostic_report
    for position in range(m):
        if len(co2_scrubber_rating_candidates) == 1:
            break
        most_common_bit = find_most_common_bit(co2_scrubber_rating_candidates, position)
        co2_scrubber_rating_candidates = [
            rating_candidate for rating_candidate in co2_scrubber_rating_candidates
            if (rating_candidate[position] == (1 - most_common_bit))
        ]
    co2_scrubber_rating = binary_to_int(co2_scrubber_rating_candidates[0])

    return oxygen_generator_rating, co2_scrubber_rating
