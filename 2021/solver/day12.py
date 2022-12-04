def main(input_lines):
    edges = parse_edges(input_lines)

    part1_answer = len(find_paths(edges, visited_one_small_cave_twice=True))
    part2_answer = len(find_paths(edges))

    return part1_answer, part2_answer


def parse_edges(input_lines):
    edges = {}
    for input_line in input_lines:
        node_1, node_2 = input_line.split("-")
        for node in (node_1, node_2):
            if node not in edges:
                edges[node] = []
        edges[node_1].append(node_2)
        edges[node_2].append(node_1)
    return edges


def find_paths(
    edges,
    current_path=None,
    visited_one_small_cave_twice=False,
    start_node="start",
    end_node="end",
):
    def is_small_cave(node):
        return node == node.lower()

    next_paths = []

    if current_path is None:
        current_path = [start_node]

    current_node = current_path[-1]
    if current_node == end_node:
        return [current_path]

    for next_node in edges[current_node]:
        next_visited_one_small_cave_twice = visited_one_small_cave_twice
        if next_node == start_node:
            continue
        if is_small_cave(next_node) and (next_node in current_path):
            if visited_one_small_cave_twice:
                continue
            next_visited_one_small_cave_twice = True
        next_paths.extend(
            find_paths(
                edges,
                current_path=current_path + [next_node],
                visited_one_small_cave_twice=next_visited_one_small_cave_twice,
            )
        )

    return next_paths
