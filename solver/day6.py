def main(input_lines):
    group_answers = [[]]
    for line in input_lines:
        line = line.strip()
        if not line:
            group_answers.append([])
        else:
            group_answers[-1].append(line)

    n_anyone_yes_answers = 0
    n_everyone_yes_answers = 0
    for group_answer in group_answers:
        n_anyone_yes_answers += len(get_anyone_yes_answers(group_answer))
        n_everyone_yes_answers += len(get_everyone_yes_answers(group_answer))

    return n_anyone_yes_answers, n_everyone_yes_answers


def get_anyone_yes_answers(group_answer):
    all_answers = ''.join(group_answer)
    return set(all_answers)


def get_everyone_yes_answers(group_answer):
    all_answers = set(group_answer[0])
    for answer in group_answer:
        all_answers = all_answers.intersection(set(answer))
    return all_answers
