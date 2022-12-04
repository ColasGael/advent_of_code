import numpy as np


def main(input_lines):
    game_rounds = []
    for line in input_lines:
        game_round = []
        for char in line.split(" "):
            val = None
            if char in ["A", "X"]:
                val = 0
            elif char in ["B", "Y"]:
                val = 1
            elif char in ["C", "Z"]:
                val = 2
            game_round.append(val)
        game_rounds.append(game_round)
    game_rounds = np.array(game_rounds)

    part1_answer = compute_score(*part1_get_responses_outcomes(game_rounds))
    part2_answer = compute_score(*part2_get_responses_outcomes(game_rounds))
    return part1_answer, part2_answer


def compute_score(responses, outcomes):
    scores = (responses + 1) + outcomes * 3
    return np.sum(scores)


def part1_get_responses_outcomes(game_rounds):
    responses = game_rounds[:, 1]
    outcomes = np.mod(responses - game_rounds[:, 0] + 1, 3)
    return responses, outcomes


def part2_get_responses_outcomes(game_rounds):
    outcomes = game_rounds[:, 1]
    responses = np.mod(outcomes + game_rounds[:, 0] - 1, 3)
    return responses, outcomes
