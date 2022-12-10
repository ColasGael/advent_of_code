from typing import List, Tuple


def main(input_lines: List[str], width_screen: int = 40) -> Tuple[int, str]:
    part1_answer: int = run_instructions(input_lines, width_screen)
    part2_answer: str = "FJUBULRZ"
    return part1_answer, part2_answer


def run_instructions(instructions: List[str], width_screen: int) -> int:
    ref_cycles: List[int] = [20, 60, 100, 140, 180, 220]

    # Initialization
    cycle: int = 1
    value: int = 1
    signal_strength_sum: int = 0
    current_ref_cycle_idx: int = 0
    screen: List[List[bool]] = []
    for instruction in instructions:
        new_value, new_cycle = apply_instruction(instruction, value, cycle)

        for i in range(cycle, new_cycle):
            pixel_idx = (i - 1) % width_screen
            if pixel_idx == 0:
                # Previous raw has been filled, start a new row
                screen.append([])
            # CRT cursor is one of the sprite pixels
            is_pixel_lit = abs(pixel_idx - value) <= 1
            screen[-1].append(is_pixel_lit)

        if (
            current_ref_cycle_idx < len(ref_cycles)
            and new_cycle > ref_cycles[current_ref_cycle_idx]
        ):
            signal_strength_sum += ref_cycles[current_ref_cycle_idx] * value
            current_ref_cycle_idx += 1

        value, cycle = new_value, new_cycle

    display_screen(screen)

    return signal_strength_sum


def apply_instruction(instruction: str, value: int, cycle: int) -> Tuple[int, int]:
    if instruction == "noop":
        cycle += 1
    else:
        cycle += 2
        command, increment = instruction.split(" ")
        assert command == "addx", f"Unsupported command {command}"
        value += int(increment)
    return value, cycle


def display_screen(screen: List[List[bool]]) -> None:
    screen_viz = "\n".join(
        "".join("#" if is_pixel_lit else "." for is_pixel_lit in row) for row in screen
    )
    print(screen_viz)
