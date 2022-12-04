import re


BAG_RULE_PATTERN = re.compile(r"(?P<quantity>\d+) (?P<color>[a-z]+ [a-z]+) bag")


def main(input_lines, target_bag="shiny gold"):
    downward_inheritance = {}
    for line in input_lines:
        parent_bag_raw, child_bags_raw = line.split("contain")
        parent_bag = BAG_RULE_PATTERN.match("0 " + parent_bag_raw).group("color")
        child_bags = BAG_RULE_PATTERN.findall(child_bags_raw)
        downward_inheritance[parent_bag] = [
            (child_bag, int(quantity)) for (quantity, child_bag) in child_bags
        ]

    upward_inheritance = get_upward_inheritance(downward_inheritance)

    part1_answer = len(find_all_parents(target_bag, upward_inheritance))
    part2_answer = find_number_children(target_bag, downward_inheritance)
    return part1_answer, part2_answer


def get_upward_inheritance(downward_inheritance):
    upward_inheritance = {}
    for parent_bag, child_bags in downward_inheritance.items():
        for (child_bag, _quantity) in child_bags:
            if not child_bag in upward_inheritance:
                upward_inheritance[child_bag] = set()
            upward_inheritance[child_bag].add(parent_bag)
    return upward_inheritance


def find_all_parents(child, upward_inheritance, parents=None):
    if parents is None:
        parents = {}
    direct_parents = upward_inheritance.get(child, set())
    if len(direct_parents) == 0:
        return direct_parents

    all_parents = direct_parents
    for direct_parent in direct_parents:
        if direct_parent not in parents:
            parents[direct_parent] = find_all_parents(
                direct_parent, upward_inheritance, parents=parents
            )
        all_parents = all_parents.union(parents[direct_parent])
    return all_parents


def find_number_children(parent, downward_inheritance, children=None):
    if children is None:
        children = {}
    n_children = 0
    for (direct_child, quantity) in downward_inheritance[parent]:
        if direct_child not in children:
            children[direct_child] = find_number_children(
                direct_child, downward_inheritance, children=children
            )
        n_children += quantity * (1 + children[direct_child])
    return n_children
