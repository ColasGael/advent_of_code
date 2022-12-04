from itertools import product
import re

import numpy as np

from .day5 import bit_to_int


INSTRUCTION_PATTERN = re.compile(r"mem\[(?P<memory_address>\d+)\] = (?P<value>\d+)")


def main(input_lines, unchanged_char="X", unchanged_int=-1):
    mask_pattern = re.compile(r"mask = (?P<mask>[{}01]+)".format(unchanged_char))

    part1_memory = {}
    part2_memory = {}
    for input_line in input_lines:
        match = mask_pattern.match(input_line)
        if match:
            mask = load_mask(match.group("mask"), unchanged_char, unchanged_int)
            continue
        match = INSTRUCTION_PATTERN.match(input_line)
        if match:
            memory_address, value = int(match.group("memory_address")), int(
                match.group("value")
            )
            part1_update_memory(
                part1_memory, memory_address, value, mask, unchanged_int
            )
            part2_update_memory(
                part2_memory, memory_address, value, mask, unchanged_int
            )

    part1_answer = sum(part1_memory.values())
    part2_answer = sum(part2_memory.values())
    return part1_answer, part2_answer


def int_to_bit(j, n_bits, base=2):
    bit = np.full((n_bits,), 0)
    idx = n_bits - 1
    while j != 0:
        bit[idx] = j % base
        j = (j - bit[idx]) / base
        idx -= 1
    return bit


def load_mask(mask_raw, unchanged_char, unchanged_int):
    n_bits = len(mask_raw)
    mask = np.full((n_bits,), unchanged_int)
    for i, char in enumerate(mask_raw):
        if char == unchanged_char:
            continue
        mask[i] = int(char)
    return mask


def part1_update_memory(memory, memory_address, value, mask, unchanged_int):
    n_bits = mask.size
    if value > 2**n_bits - 1:
        raise RuntimeError(
            "Integer value {} cannot be stored with {} bits!".format(value, n_bits)
        )
    memory[memory_address] = part1_apply_mask(mask, value, unchanged_int)


def part1_apply_mask(mask, value, unchanged_int):
    n_bits = mask.size
    bit = int_to_bit(value, n_bits)
    new_bit = np.where(mask != unchanged_int, mask, bit)
    new_value = bit_to_int(new_bit)
    return new_value


def part2_update_memory(memory, memory_address, value, mask, unchanged_int):
    n_bits = mask.size
    if value > 2**n_bits - 1:
        raise RuntimeError(
            "Integer value {} cannot be stored with {} bits!".format(value, n_bits)
        )

    new_memory_addresses = part2_apply_mask(mask, memory_address, unchanged_int)
    for new_memory_address in new_memory_addresses:
        memory[new_memory_address] = value


def part2_apply_mask(mask, value, unchanged_int):
    n_bits = mask.size
    bit = int_to_bit(value, n_bits)
    masked_bit = np.where(mask == 1, mask, bit)

    n_floating_bits = np.sum(mask == unchanged_int)
    floating_combinations = [
        np.array(combination)
        for combination in product(range(2), repeat=n_floating_bits)
    ]

    new_values = []
    for floating_combination in floating_combinations:
        new_bit = masked_bit.copy()
        new_bit[mask == unchanged_int] = floating_combination
        new_values.append(bit_to_int(new_bit))
    return new_values
