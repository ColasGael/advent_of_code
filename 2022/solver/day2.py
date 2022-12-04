from typing import List, Tuple

import numpy as np
import numpy.typing as npt


Games = npt.NDArray[np.int64]


def main(input_lines: List[str]) -> Tuple[int, int]:
    game_rounds: Games = np.empty(shape=(len(input_lines), 2), dtype=np.int64)
    for i, line in enumerate(input_lines):
        for j, char in enumerate(line.split(" ")):
            val: int = -1
            if char in ["A", "X"]:
                val = 0
            elif char in ["B", "Y"]:
                val = 1
            elif char in ["C", "Z"]:
                val = 2
            game_rounds[i, j] = val

    part1_answer: int = compute_score(*part1_get_responses_outcomes(game_rounds))
    part2_answer: int = compute_score(*part2_get_responses_outcomes(game_rounds))
    return part1_answer, part2_answer


def compute_score(responses: Games, outcomes: Games) -> int:
    scores: Games = (responses + 1) + outcomes * 3
    return np.sum(scores)


def part1_get_responses_outcomes(game_rounds: Games) -> Tuple[Games, Games]:
    responses: Games = game_rounds[:, 1]
    outcomes: Games = np.mod(responses - game_rounds[:, 0] + 1, 3)
    return responses, outcomes


def part2_get_responses_outcomes(game_rounds: Games) -> Tuple[Games, Games]:
    outcomes: Games = game_rounds[:, 1]
    responses: Games = np.mod(outcomes + game_rounds[:, 0] - 1, 3)
    return responses, outcomes
