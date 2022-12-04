import numpy as np


def main(input_lines, active_char="#", inactive_char=".", n_cycles=6):
    initial_state = parse_input(input_lines, active_char, inactive_char)

    neighbor_mask_3d, state_3d = get_state_3d(initial_state, n_cycles)
    neighbor_mask_4d, state_4d = get_state_4d(initial_state, n_cycles)

    for _i in range(n_cycles):
        state_3d = step(state_3d, neighbor_mask_3d, convolution_3d)
        state_4d = step(state_4d, neighbor_mask_4d, convolution_4d)
    part1_answer = np.sum(state_3d)
    part2_answer = np.sum(state_4d)

    return part1_answer, part2_answer


def parse_input(input_lines, active_char, inactive_char):
    initial_state = []
    for input_line in input_lines:
        initial_state_row = []
        for char in input_line:
            if char == active_char:
                initial_state_row.append(True)
            elif char == inactive_char:
                initial_state_row.append(False)
            else:
                raise RuntimeError("Input character {} not supported!".format(char))
        initial_state.append(initial_state_row)
    return np.array(initial_state)


def get_state_3d(initial_state, n_cycles):
    neighbor_mask = np.full((3, 3, 3), 1)
    neighbor_mask[1, 1, 1] = 0
    final_shape = (
        initial_state.shape[0] + 2 * (n_cycles + 1),
        initial_state.shape[1] + 2 * (n_cycles + 1),
        1 + 2 * (n_cycles + 1),
    )
    state = np.full(final_shape, False)
    state[
        n_cycles + 1 : n_cycles + 1 + initial_state.shape[0],
        n_cycles + 1 : n_cycles + 1 + initial_state.shape[1],
        n_cycles + 1,
    ] = initial_state
    return neighbor_mask, state


def get_state_4d(initial_state, n_cycles):
    neighbor_mask = np.full((3, 3, 3, 3), 1)
    neighbor_mask[1, 1, 1, 1] = 0
    final_shape = (
        initial_state.shape[0] + 2 * (n_cycles + 1),
        initial_state.shape[1] + 2 * (n_cycles + 1),
        1 + 2 * (n_cycles + 1),
        1 + 2 * (n_cycles + 1),
    )
    state = np.full(final_shape, False)
    state[
        n_cycles + 1 : n_cycles + 1 + initial_state.shape[0],
        n_cycles + 1 : n_cycles + 1 + initial_state.shape[1],
        n_cycles + 1,
        n_cycles + 1,
    ] = initial_state
    return neighbor_mask, state


def step(state, neighbor_mask, conv_method):
    n_neighbors = conv_method(state, neighbor_mask)
    next_state = np.logical_or(
        n_neighbors == 3, np.logical_and(state, n_neighbors == 2)
    )
    return next_state


def convolution_3d(input_matrix, square_kernel):
    n_x, n_y, n_z = input_matrix.shape
    kernel_size = (square_kernel.shape[0] - 1) // 2
    output_matrix = np.full(input_matrix.shape, 0.0)
    for i in range(kernel_size, n_x - kernel_size):
        for j in range(kernel_size, n_y - kernel_size):
            for k in range(kernel_size, n_z - kernel_size):
                output_matrix[i, j, k] = np.sum(
                    square_kernel
                    * input_matrix[
                        i - kernel_size : i + 1 + kernel_size,
                        j - kernel_size : j + 1 + kernel_size,
                        k - kernel_size : k + 1 + kernel_size,
                    ]
                )
    return output_matrix


def convolution_4d(input_matrix, square_kernel):
    n_x, n_y, n_z, n_w = input_matrix.shape
    kernel_size = (square_kernel.shape[0] - 1) // 2
    output_matrix = np.full(input_matrix.shape, 0.0)
    for i in range(kernel_size, n_x - kernel_size):
        for j in range(kernel_size, n_y - kernel_size):
            for k in range(kernel_size, n_z - kernel_size):
                for l in range(  # pylint: disable=invalid-name
                    kernel_size, n_w - kernel_size
                ):
                    output_matrix[i, j, k, l] = np.sum(
                        square_kernel
                        * input_matrix[
                            i - kernel_size : i + 1 + kernel_size,
                            j - kernel_size : j + 1 + kernel_size,
                            k - kernel_size : k + 1 + kernel_size,
                            l - kernel_size : l + 1 + kernel_size,
                        ]
                    )
    return output_matrix
