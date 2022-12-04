def main(input_lines):
    dots, instructions = parse_page(input_lines)

    part1_answer = len(apply_fold(dots, *instructions[0]))
    follow_instructions(dots, instructions)
    # Visual indentification
    part2_answer = "EBLUBRFH"

    return part1_answer, part2_answer


def parse_page(input_lines):
    dots = set()
    instructions = []
    for input_line in input_lines:
        if input_line.startswith("fold along"):
            fold_axis, line_num = input_line.split(" ")[-1].split("=")
            instructions.append((int(fold_axis == "y"), int(line_num)))
        elif len(input_line) == 0:
            continue
        else:
            x_coord, y_coord = input_line.split(",")
            dots.add((int(x_coord), int(y_coord)))
    return dots, instructions


def apply_fold(current_dots, fold_axis, line_num):
    new_dots = set()
    for dot in current_dots:
        if dot[fold_axis] < line_num:
            new_dots.add(dot)
        else:
            new_dot = list(dot)
            new_dot[fold_axis] = 2 * line_num - dot[fold_axis]
            new_dots.add(tuple(new_dot))
    return new_dots


def follow_instructions(dots, instructions):
    for instruction in instructions:
        dots = apply_fold(dots, *instruction)
    display_code(dots)


def display_code(dots):
    max_x = max(dot[0] for dot in dots)
    max_y = max(dot[1] for dot in dots)

    grid = [[False] * (max_x + 1) for i in range(max_y + 1)]
    for dot in dots:
        grid[dot[1]][dot[0]] = True

    image = ""
    for row in grid:
        for is_dot in row:
            image += "#" if is_dot else "."
        image += "\n"
    print(image)
