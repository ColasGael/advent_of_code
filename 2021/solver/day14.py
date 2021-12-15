def main(input_lines):
    boundary_els, polymer_pair_counts, insertion_rules = parse_polymer_manual(input_lines)

    part1_answer = solve(boundary_els, polymer_pair_counts, insertion_rules, n_steps=10)
    part2_answer = solve(boundary_els, polymer_pair_counts, insertion_rules, n_steps=40)

    return part1_answer, part2_answer


def parse_polymer_manual(input_lines):
    polymer_template = [c for c in input_lines[0].strip()]
    boundary_els = (polymer_template[0], polymer_template[-1])

    polymer_pair_counts = {}
    prev_el = polymer_template[0]
    for next_el in polymer_template[1:]:
        el_pair = (prev_el, next_el)
        if el_pair not in polymer_pair_counts:
            polymer_pair_counts[el_pair] = 0
        polymer_pair_counts[el_pair] += 1
        prev_el = next_el

    insertion_rules = {}
    for input_line in input_lines[2:]:
        input_els, output_el = input_line.strip().split(" -> ")
        start_el, end_el = input_els
        insertion_rules[(start_el, end_el)] = output_el

    return boundary_els, polymer_pair_counts, insertion_rules


def step(prev_polymer_pair_counts, insertion_rules):
    new_polymer_pair_counts = {}
    for polymer_pair, count in prev_polymer_pair_counts.items():
        start_el, end_el = polymer_pair
        new_el = insertion_rules[polymer_pair]
        for new_pair in [(start_el, new_el), (new_el, end_el)]:
            if new_pair not in new_polymer_pair_counts:
                new_polymer_pair_counts[new_pair] = 0
            new_polymer_pair_counts[new_pair] += count
    return new_polymer_pair_counts


def solve(boundary_els, polymer_pair_counts, insertion_rules, n_steps=1):
    for i in range(n_steps):
        polymer_pair_counts = step(polymer_pair_counts, insertion_rules)

    el_counts = {el: 0.5 for el in boundary_els}
    for polymer_pair, count in polymer_pair_counts.items():
        for el in polymer_pair:
            if el not in el_counts:
                el_counts[el] = 0
            # Except for the start and end elements, all elements are counted 2 times
            el_counts[el] += 0.5 * count

    max_el_count = max(el_counts.values())
    min_el_count = min(el_counts.values())
    score = int(max_el_count - min_el_count)

    return score
