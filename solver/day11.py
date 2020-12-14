import numpy as np


def main(input_lines, floor_char='.', empty_seat_char='L', occupied_seat_char='#'):
    seat_layout = np.array([[(char != floor_char) for char in line.strip('\n')] for line in input_lines])

    part1_final_occupancy_grid = converge(seat_layout, part1_transition_vectorized, 4)
    # visualize_occupied_seats(seat_layout, part1_final_occupancy_grid, floor_char, empty_seat_char, occupied_seat_char)

    part2_final_occupancy_grid = converge(seat_layout, part2_transition_naive, 5)
    # visualize_occupied_seats(seat_layout, part2_final_occupancy_grid, floor_char, empty_seat_char, occupied_seat_char)

    return np.sum(part1_final_occupancy_grid), np.sum(part2_final_occupancy_grid)


def visualize_occupied_seats(seat_layout, occupancy_grid, floor_char, empty_seat_char, occupied_seat_char):
    viz_seat_layout = np.where(seat_layout, empty_seat_char, floor_char)
    viz_occupied_seats = np.where(occupancy_grid, occupied_seat_char, viz_seat_layout)
    print(viz_occupied_seats)


def rule_empty_to_occupied(n_occupied_neighbors):
    return (n_occupied_neighbors == 0)


def rule_occupied_to_empty(n_occupied_neighbors, max_neighbors=4):
    return (n_occupied_neighbors >= max_neighbors)


def converge(seat_layout, transition_method, max_neighbors):
    occupancy_grid = np.full(seat_layout.shape, False)
    while True:
        new_occupancy_grid = transition_method(seat_layout, occupancy_grid)
        if np.all(new_occupancy_grid == occupancy_grid):
            break
        occupancy_grid = new_occupancy_grid
    return occupancy_grid


def transition_naive(seat_layout, occupancy_grid, get_n_neighbors_method, max_neighbors):
    neighbor_directions = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if not (x == y == 0)]

    n_rows, n_columns = seat_layout.shape
    new_occupancy_grid = np.full(seat_layout.shape, False)
    for row in range(n_rows):
        for column in range(n_columns):
            if not seat_layout[row, column]:
                continue
            n_occupied_neighbors = get_n_neighbors_method(seat_layout, occupancy_grid, row, column, neighbor_directions)
            if not occupancy_grid[row, column]:
                new_occupancy_grid[row, column] = rule_empty_to_occupied(n_occupied_neighbors)
            else:
                new_occupancy_grid[row, column] = not rule_occupied_to_empty(n_occupied_neighbors, max_neighbors=max_neighbors)
    return new_occupancy_grid


def part1_transition_naive(seat_layout, occupancy_grid):
    return transition_naive(seat_layout, occupancy_grid, get_n_adjacent_neighbors, 4)


def part2_transition_naive(seat_layout, occupancy_grid):
    return transition_naive(seat_layout, occupancy_grid, get_n_visible_neighbors, 5)


def get_n_adjacent_neighbors(seat_layout, occupancy_grid, seat_row, seat_column, neighbor_directions):
    n_rows, n_columns = seat_layout.shape
    n_occupied_neighbors = 0
    for neighbor_direction in neighbor_directions:
        neighbor_row = seat_row + neighbor_direction[0]
        neighbor_column = seat_column + neighbor_direction[1]
        if not ((0 <= neighbor_row < n_rows) and (0 <= neighbor_column < n_columns)):
            continue
        n_occupied_neighbors += occupancy_grid[neighbor_row, neighbor_column]
    return n_occupied_neighbors


def get_n_visible_neighbors(seat_layout, occupancy_grid, seat_row, seat_column, neighbor_directions):
    n_rows, n_columns = seat_layout.shape
    n_occupied_neighbors = 0
    for neighbor_direction in neighbor_directions:
        neighbor_row, neighbor_column = seat_row, seat_column
        while True:
            neighbor_row = neighbor_row + neighbor_direction[0]
            neighbor_column = neighbor_column + neighbor_direction[1]
            if not ((0 <= neighbor_row < n_rows) and (0 <= neighbor_column < n_columns)):
                break
            if seat_layout[neighbor_row, neighbor_column]:
                n_occupied_neighbors += occupancy_grid[neighbor_row, neighbor_column]
                break
    return n_occupied_neighbors


def part1_transition_vectorized(seat_layout, occupancy_grid):
    neighbor_kernel = np.array([[True, True, True], [True, False, True], [True, True, True]])
    n_occupied_neighbours = convolution2D(occupancy_grid, neighbor_kernel)
    transition_empty_to_occupied = np.logical_and(np.logical_and(seat_layout, np.logical_not(occupancy_grid)), rule_empty_to_occupied(n_occupied_neighbours))
    transition_occupied_to_empty = np.logical_and(occupancy_grid, rule_occupied_to_empty(n_occupied_neighbours))
    new_occupancy_grid = np.logical_or(np.logical_and(occupancy_grid, np.logical_not(transition_occupied_to_empty)), transition_empty_to_occupied)
    return new_occupancy_grid


def convolution2D(input_matrix, square_kernel):
    n_rows, n_columns = input_matrix.shape
    kernel_size = square_kernel.shape[0]
    padding = (kernel_size - 1) // 2
    input_matrix_padded = np.full((n_rows + 2*padding, n_columns + 2*padding), 0)
    input_matrix_padded[padding:n_rows+padding, padding:n_columns+padding] = input_matrix
    output_matrix = np.full(input_matrix.shape, 0.)
    for i in range(n_rows):
        for j in range(n_columns):
            output_matrix[i, j] = np.sum(square_kernel * input_matrix_padded[i:i+kernel_size, j:j+kernel_size])
    return output_matrix
