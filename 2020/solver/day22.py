from collections import deque
import re


PLAYER_PATTERN = re.compile(r"Player (?P<player_no>\d+):")


def main(input_lines):
    player_1_deck, player_2_deck = parse_input(input_lines)

    combat_winner_deck = play_combat(player_1_deck, player_2_deck, play_round)[1]
    part1_answer = compute_score(combat_winner_deck)

    recursive_combat_winner_deck = play_combat(
        player_1_deck, player_2_deck, play_recursive_round
    )[1]
    part2_answer = compute_score(recursive_combat_winner_deck)

    return part1_answer, part2_answer


def parse_input(input_lines, n_players=2):
    current_player_no = None
    player_decks = [[] for i in range(n_players)]
    for input_line in input_lines:
        if len(input_line) == 0:
            continue
        match = PLAYER_PATTERN.match(input_line)
        if match:
            current_player_no = int(match.group("player_no")) - 1
        else:
            player_decks[current_player_no].append(int(input_line))
    return player_decks


def play_combat(player_1_deck, player_2_deck, play_round_method):
    seen_configurations = set()
    player_1_deck, player_2_deck = deque(player_1_deck), deque(player_2_deck)
    is_game_won_by_player_1 = False
    while (
        (not is_game_won_by_player_1)
        and (len(player_1_deck) != 0)
        and (len(player_2_deck) != 0)
    ):
        current_configuration = hash_configuration(player_1_deck, player_2_deck)
        if current_configuration in seen_configurations:
            is_game_won_by_player_1 = True
        else:
            play_round_method(player_1_deck, player_2_deck)
            seen_configurations.add(current_configuration)
    is_game_won_by_player_1 = is_game_won_by_player_1 or (len(player_1_deck) != 0)
    winner_deck = player_1_deck if is_game_won_by_player_1 else player_2_deck
    return is_game_won_by_player_1, winner_deck


def hash_configuration(player_1_deck, player_2_deck):
    configuration_hash = (
        "1#"
        + "".join([str(player_1_card) for player_1_card in player_1_deck])
        + "2#"
        + "".join([str(player_2_card) for player_2_card in player_2_deck])
    )
    return configuration_hash


def play_round(player_1_deck, player_2_deck):
    player_1_card = player_1_deck.popleft()
    player_2_card = player_2_deck.popleft()
    if player_1_card > player_2_card:
        player_1_deck.extend([player_1_card, player_2_card])
    else:
        player_2_deck.extend([player_2_card, player_1_card])


def play_recursive_round(player_1_deck, player_2_deck):
    player_1_card = player_1_deck.popleft()
    player_2_card = player_2_deck.popleft()
    if (len(player_1_deck) >= player_1_card) and (len(player_2_deck) >= player_2_card):
        player_1_subdeck = list(player_1_deck)[:player_1_card]
        player_2_subdeck = list(player_2_deck)[:player_2_card]
        is_round_won_by_player_1 = play_combat(
            player_1_subdeck, player_2_subdeck, play_recursive_round
        )[0]
    else:
        is_round_won_by_player_1 = player_1_card > player_2_card
    if is_round_won_by_player_1:
        player_1_deck.extend([player_1_card, player_2_card])
    else:
        player_2_deck.extend([player_2_card, player_1_card])


def compute_score(winner_deck):
    score = 0
    winner_deck.reverse()
    for i, player_card in enumerate(winner_deck, start=1):
        score += i * player_card
    return score
