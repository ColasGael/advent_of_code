def main(input_lines, min_num_matching_beacons=12):
    sensors = parse_beacons(input_lines)

    beacons, scanners = find_all_beacons(sensors, min_num_matching_beacons)
    part1_answer = len(beacons)

    all_scanners_manhattan_dists = [
        manhattan_dist(scanner_1, scanner_2)
        for i, scanner_1 in enumerate(scanners)
        for scanner_2 in scanners[i + 1 :]
    ]
    part2_answer = max(all_scanners_manhattan_dists)

    return part1_answer, part2_answer


def parse_beacons(input_lines):
    sensors = []
    for input_line in input_lines:
        if len(input_line) == 0:
            continue
        if "scanner" in input_line:
            sensors.append(set())
        else:
            coords = input_line.split(",")
            beacon = (int(coords[0]), int(coords[1]), int(coords[2]))
            sensors[-1].add(beacon)
    return sensors


COORDINATE_TRANSFORMS = [
    # Rotation around coords[0]
    lambda coords: (coords[0], coords[1], coords[2]),  # 0
    lambda coords: (coords[0], coords[2], -coords[1]),  # 90
    lambda coords: (coords[0], -coords[1], -coords[2]),  # 180
    lambda coords: (coords[0], -coords[2], coords[1]),  # 270
    # Flipping then rotation around -coords[0]
    lambda coords: (-coords[0], -coords[1], coords[2]),  # 0
    lambda coords: (-coords[0], coords[2], coords[1]),  # 90
    lambda coords: (-coords[0], coords[1], -coords[2]),  # 180
    lambda coords: (-coords[0], -coords[2], -coords[1]),  # 270
    # Rotation around coords[1]
    lambda coords: (coords[1], coords[2], coords[0]),  # 0
    lambda coords: (coords[1], coords[0], -coords[2]),  # 90
    lambda coords: (coords[1], -coords[2], -coords[0]),  # 180
    lambda coords: (coords[1], -coords[0], coords[2]),  # 270
    # Flipping then rotation around -coords[1]
    lambda coords: (-coords[1], -coords[2], coords[0]),  # 0
    lambda coords: (-coords[1], coords[0], coords[2]),  # 90
    lambda coords: (-coords[1], coords[2], -coords[0]),  # 180
    lambda coords: (-coords[1], -coords[0], -coords[2]),  # 270
    # Rotation around coords[2]
    lambda coords: (coords[2], coords[0], coords[1]),  # 0
    lambda coords: (coords[2], coords[1], -coords[0]),  # 90
    lambda coords: (coords[2], -coords[0], -coords[1]),  # 180
    lambda coords: (coords[2], -coords[1], coords[0]),  # 270
    # Flipping then rotation around -coords[2]
    lambda coords: (-coords[2], -coords[0], coords[1]),  # 0
    lambda coords: (-coords[2], coords[1], coords[0]),  # 90
    lambda coords: (-coords[2], coords[0], -coords[1]),  # 180
    lambda coords: (-coords[2], -coords[1], -coords[0]),  # 270
]


def find_all_beacons(
    sensors, min_num_matching_beacons
):  # pylint: disable=too-many-locals
    # Indicate the sensor absolute pose
    sensor_positions = [None] * len(sensors)

    # Store the sensors that have been located, but not yet compared with the unlocated sensors
    open_sensors = []

    # Use first sensor frame as reference frame
    sensor_positions[0] = (0, 0, 0)
    open_sensors.append(0)

    while len(open_sensors) > 0:  # pylint: disable=too-many-nested-blocks
        j = open_sensors.pop()
        current_sensor = sensors[j]

        for i, sensor in enumerate(sensors):
            if sensor_positions[i] is not None:
                continue

            for coordinate_transform in COORDINATE_TRANSFORMS:
                rotated_sensor = set(list(map(coordinate_transform, sensor)))

                offset = None
                potential_offset_counts = {}
                for current_coords in current_sensor:
                    for rotated_coords in rotated_sensor:
                        potential_offset = (
                            current_coords[0] - rotated_coords[0],
                            current_coords[1] - rotated_coords[1],
                            current_coords[2] - rotated_coords[2],
                        )
                        if potential_offset not in potential_offset_counts:
                            potential_offset_counts[potential_offset] = 0
                        potential_offset_counts[potential_offset] += 1

                        if (
                            potential_offset_counts[potential_offset]
                            >= min_num_matching_beacons
                        ):
                            offset = potential_offset
                            break

                if offset is not None:
                    sensor_positions[i] = offset
                    # pylint: disable=cell-var-from-loop
                    translated_sensor = set(
                        list(
                            map(
                                lambda coords: (
                                    coords[0] + offset[0],
                                    coords[1] + offset[1],
                                    coords[2] + offset[2],
                                ),
                                rotated_sensor,
                            )
                        )
                    )
                    # pylint: enable=cell-var-from-loop
                    sensors[i] = translated_sensor
                    open_sensors.append(i)
                    break

    all_beacons = sensors[0]
    for i, beacons in enumerate(sensors[1:], start=1):
        if sensor_positions[i] is None:
            raise RuntimeError("Could not find absolute pose of sensor %i" % i)
        all_beacons = all_beacons.union(beacons)

    return all_beacons, sensor_positions


def manhattan_dist(point_1, point_2):
    return (
        abs(point_2[0] - point_1[0])
        + abs(point_2[1] - point_1[1])
        + abs(point_2[2] - point_1[2])
    )
