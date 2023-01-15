from typing import Dict, List, Tuple


SNAFU_DIGIT_TO_INT: Dict[str, int] = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
INT_TO_SNAFU_DIGIT: Dict[int, str] = {v: k for k, v in SNAFU_DIGIT_TO_INT.items()}


SnafuNum = List[str]


def main(input_lines: List[str]) -> Tuple[str, str]:
    snafu_nums: List[SnafuNum] = [list(input_line) for input_line in input_lines]

    part1_answer: str = "".join(compute_sum_snafu(snafu_nums))
    part2_answer: str = "empty"

    return part1_answer, part2_answer


def compute_sum_snafu(snafu_nums: List[SnafuNum]) -> SnafuNum:
    # Step 1: Convert SNAFU numbers to decimals
    snafu_nums_decs = map(snafu_to_dec, snafu_nums)
    # Step 2: Sum the decimals
    sum_dec: int = sum(snafu_nums_decs)
    # Step 3: Convert sum back to SNAFU system
    sum_snafu: SnafuNum = dec_to_snafu(sum_dec)
    return sum_snafu


def snafu_to_dec(snafu_num: SnafuNum) -> int:
    dec_num: int = 0
    for snafu_digit in snafu_num:
        dec_num = 5 * dec_num + SNAFU_DIGIT_TO_INT[snafu_digit]
    return dec_num


def dec_to_snafu(dec_num: int) -> SnafuNum:
    snafu_num: SnafuNum = []
    while dec_num > 0:
        # Step 1: convert to base 5
        rest = dec_num % 5
        dec_num = dec_num // 5
        # Step 2: adjust for SNAFU offset
        if rest == 4:
            dec_num += 1
            rest = -1
        elif rest == 3:
            dec_num += 1
            rest = -2
        # Step 3: convert to SNAFU digit
        snafu_num.append(INT_TO_SNAFU_DIGIT[rest])
    snafu_num.reverse()
    return snafu_num
