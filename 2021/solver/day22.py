def main(input_lines, init_side=50):
    reboot_steps = parse_reboot_steps(input_lines)

    equivalent_on_cuboids = reboot(reboot_steps)

    part1_answer = sum(
        map(
            lambda cuboid: compute_volume(cuboid, init_side=init_side),
            equivalent_on_cuboids,
        )
    )
    part2_answer = sum(map(compute_volume, equivalent_on_cuboids))

    return part1_answer, part2_answer


def parse_reboot_steps(input_lines):
    reboot_steps = []
    for input_line in input_lines:
        action, ranges_str = input_line.split(" ")
        cuboid = []
        for cuboid_range in ranges_str.split(","):
            start_idx, end_idx = cuboid_range[2:].split("..")
            cuboid.append([int(start_idx), int(end_idx)])
        reboot_steps.append((action == "on", cuboid))
    return reboot_steps


def compute_volume(cuboid, init_side=None):
    volume = 1
    for start_idx, end_idx in cuboid:
        if init_side is not None:
            start_idx = max(
                start_idx, -init_side  # pylint: disable=invalid-unary-operand-type
            )
            end_idx = min(end_idx, init_side)
        if start_idx > end_idx:
            return 0
        volume *= end_idx + 1 - start_idx
    return volume


def is_inside(cuboid_1, cuboid_2):
    """Check if cuboid 1 is inside cuboid 2"""
    for i, cuboid_1_range in enumerate(cuboid_1):
        start_idx_1, end_idx_1 = cuboid_1_range
        start_idx_2, end_idx_2 = cuboid_2[i]
        if not ((start_idx_2 <= start_idx_1) and (end_idx_1 <= end_idx_2)):
            return False
    return True


def is_outside(cuboid_1, cuboid_2):
    """Check if cuboid 1 is outside cuboid 2 (no intersection)"""
    for i, cuboid_1_range in enumerate(cuboid_1):
        start_idx_1, end_idx_1 = cuboid_1_range
        start_idx_2, end_idx_2 = cuboid_2[i]
        if (end_idx_2 < start_idx_1) or (end_idx_1 < start_idx_2):
            return True
    return False


def break_into_pieces(cuboid_1, cuboid_2):
    """Break cuboid 1 into pieces based on cuboid 2
    And remove the piece that is included in cuboid 2

    Assumption: cuboid 1 and 2 intersects
    """
    slices = []
    for i, cuboid_1_range in enumerate(cuboid_1):
        start_idx_1, end_idx_1 = cuboid_1_range
        start_idx_2, end_idx_2 = cuboid_2[i]
        if (start_idx_2 <= start_idx_1) and (end_idx_1 <= end_idx_2):
            range_slices = [(start_idx_1, end_idx_1)]
        elif start_idx_2 <= start_idx_1:  # (end_idx_2 < end_idx_1)
            range_slices = [(start_idx_1, end_idx_2), (end_idx_2 + 1, end_idx_1)]
        elif end_idx_1 <= end_idx_2:  # (start_idx_1 < start_idx_2)
            range_slices = [(start_idx_1, start_idx_2 - 1), (start_idx_2, end_idx_1)]
        else:  # (start_idx_1 < start_idx_2) and (end_idx_2 < end_idx_1)
            range_slices = [
                (start_idx_1, start_idx_2 - 1),
                (start_idx_2, end_idx_2),
                (end_idx_2 + 1, end_idx_1),
            ]
        slices.append(range_slices)

    cuboid_1_pieces = []
    for x_slice in slices[0]:
        for y_slice in slices[1]:
            for z_slice in slices[2]:
                piece = [x_slice, y_slice, z_slice]
                # Remove the intersecting piece
                if is_inside(piece, cuboid_2):
                    continue
                cuboid_1_pieces.append(piece)
    return cuboid_1_pieces


def reboot(reboot_steps):
    # Equivalent representation of the state of the full cuboid
    # as a list of un-intersecting ON cuboids
    equivalent_on_cuboids = []
    for (turn_on, cuboid) in reboot_steps:
        new_equivalent_on_cuboids = []

        if turn_on:
            # Add the new ON cuboid
            new_equivalent_on_cuboids.append(cuboid)

        # Remove the portions of the previous ON cuboids intersecting with the new cuboid
        for on_cuboid in equivalent_on_cuboids:
            # If the previous ON cuboid is inside the new cuboid
            # the previous ON cuboid is completely captured by the new cuboid
            if is_inside(on_cuboid, cuboid):
                continue
            # If the previous ON cuboid is outside the new cuboid
            # the previous ON cuboid is not modified
            if is_outside(on_cuboid, cuboid):
                new_equivalent_on_cuboids.append(on_cuboid)
            # The previous ON cuboid intersects with the new cuboid
            # break it into pieces to remove the intersecting portion
            else:
                new_equivalent_on_cuboids.extend(break_into_pieces(on_cuboid, cuboid))

        # Update the representation of the state of the full cuboid
        equivalent_on_cuboids = new_equivalent_on_cuboids

    return equivalent_on_cuboids
