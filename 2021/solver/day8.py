def main(input_lines):
    entries = parse_entries(input_lines)
    part1_answer, part2_answer = solve(entries)
    return part1_answer, part2_answer


def parse_entries(input_lines):
    entries = []
    for input_line in input_lines:
        inputs, outputs = input_line.split("|")
        signal_patterns = [set(pattern) for pattern in inputs.split(" ")]
        output_digits = [set(pattern) for pattern in outputs.split(" ")]
        entries.append((signal_patterns, output_digits))
    return entries


def solve(entries):
    part1_answer = 0
    part2_answer = 0
    for entry in entries:
        output_number = decode_entry(entry)
        for i, output_digit in enumerate(output_number):
            if output_digit in (1, 4, 7, 8):
                part1_answer += 1
            part2_answer += output_digit * 10**i
    return part1_answer, part2_answer


def decode_entry(entry):
    signal_patterns, output_digits = entry
    # Find the patterns corresponding to the "easy" digits: with a unique number of segments
    decoded_patterns = {}
    undecoded_patterns = []
    for pattern in signal_patterns:
        if len(pattern) == 2:
            decoded_patterns[1] = pattern
        elif len(pattern) == 4:
            decoded_patterns[4] = pattern
        elif len(pattern) == 3:
            decoded_patterns[7] = pattern
        elif len(pattern) == 7:
            decoded_patterns[8] = pattern
        else:
            undecoded_patterns.append(pattern)

    # Identify which letter corresponds to which segment
    # The segments are numbered from top to bottom, left to right, as:
    #  1
    # 2 3
    #  4
    # 5 6
    #  7
    segments = {}
    # Segment 1: is used to draw a 7 but not a 1
    segments[1] = list(decoded_patterns[7] - decoded_patterns[1])[0]
    # Segments 1 ; 4 ; 7: are used to draw to all the five-segment digits (2 ; 5)
    candidate_segments = decoded_patterns[8].intersection(
        *[pattern for pattern in undecoded_patterns if len(pattern) == 5])
    # Segment 4: is the only one of these also used to draw a 4
    segments[4] = list(candidate_segments.intersection(decoded_patterns[4]))[0]
    # Segment 7: is the remaining one
    segments[7] = list(candidate_segments - set((segments[1], segments[4])))[0]
    # Segment 2: is used to draw a 4 but not a 1 ; and not segment 4
    segments[2] = list(decoded_patterns[4] - decoded_patterns[1] - set((segments[4])))[0]
    # Segment 5: is not used to draw a 1 ; and not segments 1 ; 2 ; 4 ; 7
    segments[5] = list(decoded_patterns[8] - decoded_patterns[1] -
                       set((segments[1], segments[2], segments[4], segments[7])))[0]
    # Segment 6: is used to draw all the 6-segment digits (0, 6, 9) ; and not segments 1 ; 2 ; 4 ; 7
    candidate_segments = decoded_patterns[8].intersection(
        *[pattern for pattern in undecoded_patterns if len(pattern) == 6])
    segments[6] = list(
        candidate_segments - set((segments[1], segments[2], segments[4], segments[7])))[0]
    # Segment 3: is the remaining one used to draw a 1
    segments[3] = list(decoded_patterns[1] - set((segments[6])))[0]

    # Decode the remaining patterns
    decoded_patterns.update({
        0: set((segments[1], segments[2], segments[3], segments[5], segments[6], segments[7])),
        2: set((segments[1], segments[3], segments[4], segments[5], segments[7])),
        3: set((segments[1], segments[3], segments[4], segments[6], segments[7])),
        5: set((segments[1], segments[2], segments[4], segments[6], segments[7])),
        6: set((segments[1], segments[2], segments[4], segments[5], segments[6], segments[7])),
        9: set((segments[1], segments[2], segments[3], segments[4], segments[6], segments[7])),
    })

    # Decypher the output
    output_number = []
    for output_digit in output_digits:
        for digit, pattern in decoded_patterns.items():
            if output_digit == pattern:
                output_number.append(digit)
                break
    output_number.reverse()
    return output_number
