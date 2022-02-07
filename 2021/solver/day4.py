def main(input_lines):
    drawn_numbers, boards, board_numbers, visited_boards = parse_bingo(input_lines)

    (
        first_winning_board_last_number,
        first_winning_board_idx,
        last_winning_board_last_number,
        last_winning_board_idx
    ) = play_bingo(drawn_numbers, boards, board_numbers, visited_boards)

    part1_answer = compute_score(
        first_winning_board_last_number, first_winning_board_idx, boards, visited_boards)
    part2_answer = compute_score(
        last_winning_board_last_number, last_winning_board_idx, boards, visited_boards)

    return part1_answer, part2_answer


def parse_bingo(input_lines):
    # The first line indicates the numbers in the order they are drawn
    drawn_numbers = [int(number) for number in input_lines[0].split(",")]

    boards = [[]]
    for input_line in input_lines[2:]:
        if len(input_line) == 0:
            boards.append([])
            continue
        board_row = [int(number) for number in input_line.split() if len(number) > 0]
        boards[-1].append(board_row)

    # Map each number to the boards where it can be found and where (row, column)
    board_numbers = {}
    for board_idx, board in enumerate(boards):
        for row_idx, row in enumerate(board):
            for column_idx, number in enumerate(row):
                if number not in board_numbers:
                    board_numbers[number] = []
                board_numbers[number].append((board_idx, row_idx, column_idx))

    line_length = len(boards[0][0])
    # key: board index
    # value: (count of marked numbers for each row, for each column, total sum of marked numbers)
    visited_boards = {
        board_idx: [[0] * line_length, [0] * line_length, 0] for board_idx in range(len(boards))
    }

    return drawn_numbers, boards, board_numbers, visited_boards


def play_bingo(drawn_numbers, boards, board_numbers, visited_boards):
    '''
    Assumptions:
      - The boards are square: same number of rows and columns
      - The drawn numbers are all different.
      - The numbers on a given board are all different.
      - All the boards are winning when all the numbers have been drawn.
    '''
    first_winning_board_last_number = None
    winning_boards = []
    line_length = len(boards[0][0])
    for number in drawn_numbers:
        check_number(line_length, number, board_numbers, visited_boards, winning_boards)
        if (first_winning_board_last_number is None) and (len(winning_boards) > 0):
            first_winning_board_last_number = number
        if len(winning_boards) == len(boards):
            break

    first_winning_board_idx = winning_boards[0]
    last_winning_board_last_number = number
    last_winning_board_idx = winning_boards[-1]
    return (
        first_winning_board_last_number,
        first_winning_board_idx,
        last_winning_board_last_number,
        last_winning_board_idx
    )


def check_number(line_length, number, board_numbers, visited_boards, winning_boards):
    for board_idx, row_idx, column_idx in board_numbers.get(number):
        # Do not update already winning boards
        if board_idx in winning_boards:
            continue
        visited_boards[board_idx][0][row_idx] += 1
        visited_boards[board_idx][1][column_idx] += 1
        visited_boards[board_idx][2] += number
        for marked_numbers_count in (visited_boards[board_idx][0][row_idx],
                                     visited_boards[board_idx][1][column_idx]):
            if marked_numbers_count == line_length:
                winning_boards.append(board_idx)
                break


def compute_score(last_number, winning_board_idx, boards, visited_boards):
    winning_board = boards[winning_board_idx]
    board_sum = sum([sum(board_row) for board_row in winning_board])
    non_marked_numbers_sum = board_sum - visited_boards[winning_board_idx][2]
    score = last_number * non_marked_numbers_sum
    return score
