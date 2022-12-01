def main(input_lines, top_k=3):
    input_lines.append("")
    calories_elves = [[]]
    for line in input_lines:
        if len(line) == 0:
            calories_elves.append([])
            continue
        calories_elves[-1].append(int(line))

    part1_answer = find_most_calories_elve(calories_elves)
    part2_answer = sum(find_most_calories_elves(calories_elves, top_k))
    return part1_answer, part2_answer


def find_most_calories_elve(calories_elves):
    most_calories_elve = max(map(sum, calories_elves))
    return most_calories_elve


def find_most_calories_elves(calories_elves, top_k):
    total_calories_elves = list(map(sum, calories_elves))
    total_calories_elves.sort()
    most_calories_elves = total_calories_elves[-top_k:]
    return most_calories_elves
