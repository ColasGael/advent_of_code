import re
from typing import cast, List, Optional, Tuple

import intervals as I  # type: ignore
import numpy as np
import numpy.typing as npt


Coord = Tuple[int, int]
CoordRange = npt.NDArray[np.int64]


sensor_beacon_pat = re.compile(
    r"^Sensor at x=(?P<sensor_x>[\d-]+), y=(?P<sensor_y>[\d-]+): "
    r"closest beacon is at x=(?P<beacon_x>[\d-]+), y=(?P<beacon_y>[\d-]+)$"
)


def main(
    input_lines: List[str], row_y: int = 2000000, max_coord: int = 4000000
) -> Tuple[int, int]:
    sensor_beacon_coords = parse_sensor_beacon_coords(input_lines)

    part1_answer: int = compute_coverage(
        check_row_coverage(sensor_beacon_coords, row_y)[0]
    )
    part2_answer: int = compute_tuning_frequency(
        find_distress_beacon_coord(sensor_beacon_coords, max_coord)
    )

    return part1_answer, part2_answer


def compute_manhattan_dist(coord_1: Coord, coord_2: Coord) -> int:
    return abs(coord_1[0] - coord_2[0]) + abs(coord_1[1] - coord_2[1])


def compute_coverage(coverage: I.Interval) -> int:
    coverage_count = 0
    for sensor_coverage in coverage:
        lower_bound = sensor_coverage.lower
        upper_bound = sensor_coverage.upper
        if not sensor_coverage.left:
            lower_bound += 1
        if not sensor_coverage.right:
            upper_bound -= 1
        coverage_count += upper_bound - lower_bound + 1
    return coverage_count


def compute_tuning_frequency(coord: Coord) -> int:
    return coord[0] * 4000000 + coord[1]


def parse_sensor_beacon_coords(input_lines: List[str]) -> List[Tuple[Coord, Coord]]:
    sensor_beacon_coords: List[Tuple[Coord, Coord]] = []
    for input_line in input_lines:
        match = sensor_beacon_pat.match(input_line)
        if match is None:
            raise RuntimeError(f"Cannot parse input_line: {input_line}")
        sensor_x = int(match.group("sensor_x"))
        sensor_y = int(match.group("sensor_y"))
        beacon_x = int(match.group("beacon_x"))
        beacon_y = int(match.group("beacon_y"))
        sensor_beacon_coords.append(((sensor_x, sensor_y), (beacon_x, beacon_y)))
    return sensor_beacon_coords


def check_row_coverage(  # pylint: disable=too-many-locals
    sensor_beacon_coords: List[Tuple[Coord, Coord]], row_y: int, include_beacon=False
) -> Tuple[I.Interval, int]:
    """Compute the portion of the row at y=row_y covered by the sensor.

    Return:
        coverage (I.Interval): the said coverage
        min_overlap (int): the minimum (non-empty) overlap between two sensors' coverages
    """
    coverage: I.Interval = I.empty()
    min_overlap: Optional[int] = None
    sensor_coverages: List[I.Interval] = []
    for sensor_coord, beacon_coord in sensor_beacon_coords:
        min_manhattan_dist = compute_manhattan_dist(sensor_coord, beacon_coord)
        sensor_x, sensor_y = sensor_coord
        # How much manhattan distance "is left" to spend along the x-axis
        x_offset = min_manhattan_dist - abs(sensor_y - row_y)
        # Portion of the row covered by the sensor
        min_covered_x = sensor_x - x_offset
        max_covered_x = sensor_x + x_offset
        sensor_coverage = I.closed(min_covered_x, max_covered_x)
        # Find the minimum (non-empty) overlap between that sensor and the previous ones' coverages
        for prev_sensor_coverage in sensor_coverages:
            coverage_overlap = sensor_coverage.intersection(prev_sensor_coverage)
            if coverage_overlap.is_empty():
                continue
            overlap = coverage_overlap.upper - coverage_overlap.lower
            if overlap == 0:
                continue
            if min_overlap is None or min_overlap > overlap:
                min_overlap = overlap
        # Update the full coverage
        coverage = coverage.union(sensor_coverage)
        sensor_coverages.append(sensor_coverage)

    if not include_beacon:
        # Remove the found beacons from the coverage sensor_coverage
        for _sensor_coord, beacon_coord in sensor_beacon_coords:
            beacon_x, beacon_y = beacon_coord
            if beacon_y == row_y:
                coverage = coverage.difference(I.closed(beacon_x, beacon_x))

    min_overlap = cast(int, min_overlap)
    return coverage, min_overlap


def find_distress_beacon_coord(
    sensor_beacon_coords: List[Tuple[Coord, Coord]], max_coord: int
) -> Coord:
    x_bounds: I.Interval = I.closed(0, max_coord)
    y_coord: int = 0
    while y_coord < max_coord:
        coverage, min_overlap = check_row_coverage(
            sensor_beacon_coords, y_coord, include_beacon=True
        )
        # Check if anypart of the x-sensor_coverage is not covered
        diff = x_bounds.difference(coverage)
        if not diff.is_empty():
            assert (
                diff.upper - diff.lower - 1 == 1
            ), f"There should be exactly one spot not covered, got {diff.upper - diff.lower - 1}"
            x_coord: int = (diff.upper + diff.lower) // 2
            return x_coord, y_coord

        # At most, by going down 1 row, we can decrease the overlap between the coverage
        # of two sensors by 2: 1 on each side
        # So the minimum (non-empty) overlap between two sensors give us a lower bound on how far
        # we are from the position of the undetected distress beacon
        # For a minimum overlap of 2k, we need to go down by at least k + 1 row.
        # to get an uncovered section between the associated two sensors
        y_coord += max(min_overlap // 2 + 1, 1)

    # Should not happen
    raise RuntimeError("Failed to find the coordinates of the distress beacon")
