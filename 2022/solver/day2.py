import numpy as np

def main(input_lines):
    rounds = []
    for line in input_lines:
        round = []
        for c in line.split(" "):
            val = None
            if c in ["A", "X"]:
                val = 0
            elif c in ["B", "Y"]:
                val = 1
            elif c in ["C", "Z"]:
                val = 2
            round.append(val)
        rounds.append(round)
    rounds = np.array(rounds)

    part1_answer = compute_score(*part1_get_responses_outcomes(rounds))
    part2_answer = compute_score(*part2_get_responses_outcomes(rounds))
    return part1_answer, part2_answer


def compute_score(responses, outcomes):
    scores = (responses + 1) + outcomes * 3
    return np.sum(scores)


def part1_get_responses_outcomes(rounds):
    responses = rounds[:, 1]
    outcomes = np.mod(responses - rounds[:, 0] + 1, 3)
    return responses, outcomes

def part2_get_responses_outcomes(rounds):
    outcomes =rounds[:, 1]
    responses = np.mod(outcomes + rounds[:, 0] - 1, 3)
    return responses, outcomes
