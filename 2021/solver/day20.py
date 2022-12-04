def main(input_lines, light_char="#"):
    im_enhance_alg, input_im = parse_im(input_lines, light_char)

    part1_answer = solve(im_enhance_alg, input_im, n_steps=2)
    part2_answer = solve(im_enhance_alg, input_im, n_steps=50)

    return part1_answer, part2_answer


def parse_im(input_lines, light_char):
    im_enhance_alg = [int(c == light_char) for c in input_lines[0]]
    input_im = [
        [int(c == light_char) for c in input_line] for input_line in input_lines[2:]
    ]
    return im_enhance_alg, input_im


def binary_to_int(bin_number):
    # Horner's method for polynomial evaluation
    int_number = 0
    for bit in bin_number:
        int_number = 2 * int_number + bit
    return int_number


def get_enhance_key(input_im, row_idx, col_idx, background_value):
    max_row, max_col = len(input_im), len(input_im[0])
    enhance_key = [background_value] * 9
    if (0 < row_idx) and (0 < col_idx):
        enhance_key[0] = input_im[row_idx - 1][col_idx - 1]
    if (0 < row_idx) and (0 <= col_idx < max_col):
        enhance_key[1] = input_im[row_idx - 1][col_idx]
    if (0 < row_idx) and (col_idx < max_col - 1):
        enhance_key[2] = input_im[row_idx - 1][col_idx + 1]
    if (0 <= row_idx < max_row) and (0 < col_idx):
        enhance_key[3] = input_im[row_idx][col_idx - 1]
    if (0 <= row_idx < max_row) and (0 <= col_idx < max_col):
        enhance_key[4] = input_im[row_idx][col_idx]
    if (0 <= row_idx < max_row) and (col_idx < max_col - 1):
        enhance_key[5] = input_im[row_idx][col_idx + 1]
    if (row_idx < max_row - 1) and (0 < col_idx):
        enhance_key[6] = input_im[row_idx + 1][col_idx - 1]
    if (row_idx < max_row - 1) and (0 <= col_idx < max_col):
        enhance_key[7] = input_im[row_idx + 1][col_idx]
    if (row_idx < max_row - 1) and (col_idx < max_col - 1):
        enhance_key[8] = input_im[row_idx + 1][col_idx + 1]
    return enhance_key


def enhance(im_enhance_alg, input_im, background_value):
    max_row, max_col = len(input_im), len(input_im[0])
    output_im = []
    for row_idx in range(-1, max_row + 1):
        output_im.append([])
        for col_idx in range(-1, max_col + 1):
            enhance_key = get_enhance_key(input_im, row_idx, col_idx, background_value)
            pixel_value = im_enhance_alg[binary_to_int(enhance_key)]
            output_im[-1].append(pixel_value)
    return output_im


def solve(im_enhance_alg, image, n_steps=0):
    background_value = 0
    for _k in range(n_steps):
        image = enhance(im_enhance_alg, image, background_value)
        background_enhance_key = [background_value] * 9
        background_value = im_enhance_alg[binary_to_int(background_enhance_key)]
    num_lit_pixels = sum(map(sum, image))
    return num_lit_pixels
