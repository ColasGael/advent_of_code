def main(input_lines, tree_char='#'):
    tree_map = [[(char == tree_char) for char in line] for line in input_lines]

    SLOPE = (3, 1)
    part1_answer = find_trees_on_slope(tree_map, *SLOPE)

    SLOPES = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    part2_answer = 1
    for slope in SLOPES:
        part2_answer *= find_trees_on_slope(tree_map, *slope)

    return part1_answer, part2_answer


def find_trees_on_slope(tree_map, right, down):
    position = (0, 0)
    n_trees_on_slope = 0
    while position[1] < len(tree_map):
        tree_row = tree_map[position[1]]
        if tree_row[position[0] % len(tree_row)]:
            n_trees_on_slope += 1
        position = (position[0] + right, position[1] + down)
    return n_trees_on_slope
