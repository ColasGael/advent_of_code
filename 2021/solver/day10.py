def main(input_lines):
    part1_answer, part2_answer = check_chunks(input_lines)
    return part1_answer, part2_answer


def check_chunks(input_lines):
    char_pairs = {
        "(": ")",
        "[": "]",
        "{": "}",
        "<": ">",
    }

    corrupted_lines_illegal_chars = []
    incomplete_lines_missing_chars = []

    for input_line in input_lines:
        is_corrupted_line = False
        open_chunks = []

        for c in input_line:
            if c in char_pairs.keys():
                open_chunks.append(c)
            elif c in char_pairs.values():
                opening_c = open_chunks.pop()
                if char_pairs[opening_c] != c:
                    is_corrupted_line = True
                    corrupted_lines_illegal_chars.append(c)
                    break
            else:
                raise RuntimeError("Unsupported character: %s" % c)

        # Skip corrupted lines
        if is_corrupted_line:
            continue
        # Check if it is an incomplete line:
        if len(open_chunks) > 0:
            open_chunks.reverse()
            missing_chars = map(lambda c: char_pairs[c], open_chunks)
            incomplete_lines_missing_chars.append(missing_chars)

    tot_syntax_error_score = compute_syntax_error_score(corrupted_lines_illegal_chars)

    autocomplete_scores = list(map(
        lambda missing_chars: compute_autocomplete_score(missing_chars),
        incomplete_lines_missing_chars
    ))
    autocomplete_scores.sort()
    median_autocomplete_score = autocomplete_scores[len(autocomplete_scores) // 2]

    return tot_syntax_error_score, median_autocomplete_score


def compute_syntax_error_score(illegal_chars):
    char_scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    syntax_error_score = sum(map(lambda c: char_scores[c], illegal_chars))
    return syntax_error_score


def compute_autocomplete_score(missing_chars):
    char_scores = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    autocomplete_score = 0
    for c in missing_chars:
        autocomplete_score = 5 * autocomplete_score + char_scores[c]
    return autocomplete_score
