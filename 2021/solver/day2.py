def main(input_lines):
    instructions = []
    for line in input_lines:
        direction, value = line.split()
        instructions.append((direction, int(value)))

    part1_initial_state = (0, 0) # (horizontal position, depth)
    part1_final_state = move(instructions, part1_initial_state, part_1_step)
    part1_answer = part1_final_state[0] * part1_final_state[1]

    part2_initial_state = (0, 0, 0) # (horizontal position, depth, aim)
    part2_final_state = move(instructions, part2_initial_state, part_2_step)
    part2_answer = part2_final_state[0] * part2_final_state[1]

    return part1_answer, part2_answer

def move(instructions, state, step_method):
    for direction, value in instructions:
        state = step_method(direction, value, state)
    return state

def part_1_step(direction, value, current_state):
    position, depth = current_state
    if direction == "forward":
        new_state = (position + value, depth)
    elif direction == "down":
        new_state = (position, depth + value)
    elif direction == "up":
        new_state = (position, depth - value)
    return new_state

def part_2_step(direction, value, current_state):
    position, depth, aim = current_state
    if direction == "forward":
        new_state = (position + value, depth + aim * value, aim)
    elif direction == "down":
        new_state = (position, depth, aim + value)
    elif direction == "up":
        new_state = (position, depth, aim - value)
    return new_state
