def main(input_lines, min_num_matching_beacons=12):
    sensors = parse_beacons(input_lines)

    beacons, scanners = find_all_beacons(sensors, min_num_matching_beacons)
    part1_answer = len(beacons)

    all_scanners_manhattan_dists = [
        manhattan_dist(scanner_1, scanner_2)
        for i, scanner_1 in enumerate(scanners)
        for scanner_2 in scanners[i + 1:]
    ]
    part2_answer = max(all_scanners_manhattan_dists)

    return part1_answer, part2_answer


def parse_beacons(input_lines):
    sensors = []
    for input_line in input_lines:
        input_line = input_line.strip()
        if len(input_line) == 0:
            continue
        elif "scanner" in input_line:
            sensors.append(set())
        else:
            (x, y, z) = input_line.split(",")
            beacon = (int(x), int(y), int(z))
            sensors[-1].add(beacon)
    return sensors


COORDINATE_TRANSFORMS = [
    # Rotation around x
    lambda (x, y, z): (x, y, z),    # 0
    lambda (x, y, z): (x, z, -y),   # 90
    lambda (x, y, z): (x, -y, -z),  # 180
    lambda (x, y, z): (x, -z, y),   # 270
    # Flipping then rotation around -x
    lambda (x, y, z): (-x, -y, z),  # 0
    lambda (x, y, z): (-x, z, y),   # 90
    lambda (x, y, z): (-x, y, -z),  # 180
    lambda (x, y, z): (-x, -z, -y), # 270
    # Rotation around y
    lambda (x, y, z): (y, z, x),    # 0
    lambda (x, y, z): (y, x, -z),   # 90
    lambda (x, y, z): (y, -z, -x),  # 180
    lambda (x, y, z): (y, -x, z),   # 270
    # Flipping then rotation around -y
    lambda (x, y, z): (-y, -z, x),  # 0
    lambda (x, y, z): (-y, x, z),   # 90
    lambda (x, y, z): (-y, z, -x),  # 180
    lambda (x, y, z): (-y, -x, -z), # 270
    # Rotation around z
    lambda (x, y, z): (z, x, y),    # 0
    lambda (x, y, z): (z, y, -x),   # 90
    lambda (x, y, z): (z, -x, -y),  # 180
    lambda (x, y, z): (z, -y, x),   # 270
    # Flipping then rotation around -z
    lambda (x, y, z): (-z, -x, y),  # 0
    lambda (x, y, z): (-z, y, x),   # 90
    lambda (x, y, z): (-z, x, -y),  # 180
    lambda (x, y, z): (-z, -y, -x), # 270
]


def find_all_beacons(sensors, min_num_matching_beacons):
    # Indicate the sensor absolute pose
    sensor_positions = [None] * len(sensors)

    # Store the sensors that have been located, but not yet compared with the unlocated sensors
    open_sensors = []

    # Use first sensor frame as reference frame
    sensor_positions[0] = (0, 0, 0)
    open_sensors.append(0)

    while len(open_sensors) > 0:
        j = open_sensors.pop()
        current_sensor = sensors[j]

        for i, sensor in enumerate(sensors):
            if sensor_positions[i] is not None:
                continue

            for coordinate_transform in COORDINATE_TRANSFORMS:
                rotated_sensor = set(list(map(coordinate_transform, sensor)))

                offset = None
                potential_offset_counts = {}
                for current_beacon in current_sensor:
                    current_x, current_y, current_z = current_beacon
                    for rotated_beacon in rotated_sensor:
                        rotated_x, rotated_y, rotated_z = rotated_beacon
                        potential_offset = (
                            current_x - rotated_x,
                            current_y - rotated_y,
                            current_z - rotated_z,
                        )
                        if potential_offset not in potential_offset_counts:
                            potential_offset_counts[potential_offset] = 0
                        potential_offset_counts[potential_offset] += 1

                        if potential_offset_counts[potential_offset] >= min_num_matching_beacons:
                            offset = potential_offset
                            break

                if offset is not None:
                    sensor_positions[i] = offset
                    translated_sensor = set(list(map(
                        lambda (x, y, z): (x + offset[0], y + offset[1], z + offset[2]),
                        rotated_sensor)
                    ))
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
    x_1, y_1, z_1 = point_1
    x_2, y_2, z_2 = point_2
    return abs(x_2 - x_1) + abs(y_2 - y_1) + abs(z_2 - z_1)
