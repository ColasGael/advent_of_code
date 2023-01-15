def main(input_lines):
    start_positions = parse_start_positions(input_lines)

    scores, num_dice_roll = play_deterministic(start_positions)
    part1_answer = min(scores) * num_dice_roll

    num_wins = play_quantic(*start_positions)
    part2_answer = max(num_wins)

    return part1_answer, part2_answer


def parse_start_positions(input_lines):
    start_positions = [int(input_line.split(" ")[-1]) for input_line in input_lines]
    return start_positions


def play_deterministic(start_positions, win_score=1000, num_dice_roll_per_turn=3):
    positions = list(start_positions)
    scores = [0] * len(start_positions)

    num_dice_roll = 0
    while max(scores) < win_score:
        for player_idx, position in enumerate(positions):
            num_steps = int(
                (2 * num_dice_roll + num_dice_roll_per_turn + 1)
                * num_dice_roll_per_turn
                / 2
            )
            num_dice_roll += num_dice_roll_per_turn

            positions[player_idx] = (position + num_steps - 1) % 10 + 1

            scores[player_idx] += positions[player_idx]
            if scores[player_idx] >= win_score:
                break

    return scores, num_dice_roll


def play_quantic(player1_start_position, player2_start_position, win_score=21):
    num_wins = [0, 0]

    open_games = [(1, player1_start_position, player2_start_position, 0, 0)]
    while len(open_games) > 0:
        (
            total_count,
            player1_position,
            player2_position,
            player1_score,
            player2_score,
        ) = open_games.pop()

        num_steps = ((1, 3), (3, 4), (6, 5), (7, 6), (6, 7), (3, 8), (1, 9))
        for player1_count_games, player1_num_step in num_steps:
            player1_total_count = total_count * player1_count_games
            player1_new_position = (player1_position + player1_num_step - 1) % 10 + 1
            player1_new_score = player1_score + player1_new_position
            if player1_new_score >= win_score:
                num_wins[0] += player1_total_count
                continue

            for player2_count_games, player2_num_step in num_steps:
                player2_total_count = player1_total_count * player2_count_games
                player2_new_position = (
                    player2_position + player2_num_step - 1
                ) % 10 + 1
                player2_new_score = player2_score + player2_new_position
                if player2_new_score >= win_score:
                    num_wins[1] += player2_total_count
                    continue

                open_games.append(
                    (
                        player2_total_count,
                        player1_new_position,
                        player2_new_position,
                        player1_new_score,
                        player2_new_score,
                    )
                )

    return num_wins
