from functools import partial, reduce
import re
from typing import cast, Dict, List, Optional, Tuple


# (# ore, # clay, # obsidian, # geode)
Resources = Tuple[int, int, int]
# (# ore-robot, # clay-robot, # obsidian-robot, # geode-robot)
Robots = Tuple[int, int, int, int]
State = Tuple[Resources, Robots]


BLUEPRINT_PATTERN = re.compile(
    r"Blueprint \d+: "
    r"Each ore robot costs (?P<ore_ore_cost>\d+) ore. "
    r"Each clay robot costs (?P<clay_ore_cost>\d+) ore. "
    r"Each obsidian robot costs (?P<obsidian_ore_cost>\d+) ore "
    r"and (?P<obsidian_clay_cost>\d+) clay. "
    r"Each geode robot costs (?P<geode_ore_cost>\d+) ore and (?P<geode_obsidian_cost>\d+) obsidian."
)


class Factory:
    def __init__(self, robots_resources: List[Resources]):
        self._robots_resources = robots_resources

    def build_robot(self, resources: Resources, robot_idx: int) -> Optional[Resources]:
        new_resources = (
            resources[0] - self._robots_resources[robot_idx][0],
            resources[1] - self._robots_resources[robot_idx][1],
            resources[2] - self._robots_resources[robot_idx][2],
        )
        for new_resource in new_resources:
            if new_resource < 0:
                return None
        return new_resources

    def get_max_resources(self) -> Resources:
        max_resources = tuple(
            max(robot_resources[k] for robot_resources in self._robots_resources)
            for k in range(len(self._robots_resources[0]))
        )
        return cast(Resources, max_resources)


def main(
    input_lines: List[str], part1_t_end: int = 24, part2_t_end: int = 32
) -> Tuple[int, int]:
    factories: List[Factory] = parse_blueprints(input_lines)

    part1_max_geodes = map(partial(find_max_geodes, part1_t_end), factories)
    part1_answer: int = sum(
        k * geodes for k, geodes in enumerate(part1_max_geodes, start=1)
    )

    part2_max_geodes = map(partial(find_max_geodes, part2_t_end), factories[:3])
    part2_answer: int = reduce(lambda a, b: a * b, part2_max_geodes)

    return part1_answer, part2_answer


def parse_blueprints(input_lines: List[str]) -> List[Factory]:
    factories: List[Factory] = []
    for input_line in input_lines:
        match = BLUEPRINT_PATTERN.match(input_line)
        if match is None:
            raise RuntimeError(f"Could not parse blueprint: {input_line}")

        ore_robot_resources = (int(match.group("ore_ore_cost")), 0, 0)
        clay_robot_resources = (int(match.group("clay_ore_cost")), 0, 0)
        obsidian_robot_resources = (
            int(match.group("obsidian_ore_cost")),
            int(match.group("obsidian_clay_cost")),
            0,
        )
        geode_robot_resources = (
            int(match.group("geode_ore_cost")),
            0,
            int(match.group("geode_obsidian_cost")),
        )

        factory = Factory(
            [
                ore_robot_resources,
                clay_robot_resources,
                obsidian_robot_resources,
                geode_robot_resources,
            ]
        )
        factories.append(factory)

    return factories


def find_max_geodes(t_end: int, factory: Factory) -> int:
    visited_states: Dict[Tuple[Resources, Robots, int], int] = {}

    def dfs(resources: Resources, robots: Robots, current_t: int):
        if current_t == 1:
            return robots[-1]

        # Having more resources that you can spend has no influence on the final outcome
        max_resources_consumption = factory.get_max_resources()
        equivalent_resources = (
            min(resources[0], max_resources_consumption[0] * (current_t - 1)),
            min(resources[1], max_resources_consumption[1] * (current_t - 1)),
            min(resources[2], max_resources_consumption[2] * (current_t - 1)),
        )

        key = (equivalent_resources, robots, current_t)

        if key in visited_states:
            return visited_states[key]

        new_resources: Optional[Resources]

        new_resources = (
            resources[0] + robots[0],
            resources[1] + robots[1],
            resources[2] + robots[2],
        )
        max_geodes = dfs(new_resources, robots, current_t - 1)

        for k, robot in enumerate(robots):
            # If you create more resource than you can spend in one round,
            # no need to create another robot to mine that resource
            if (
                k < len(max_resources_consumption)
                and max_resources_consumption[k] <= robot
            ):
                continue

            # If you have more resource than you can spend until the end
            # no need to create another robot to mine that resource
            if (
                k < len(max_resources_consumption)
                and max_resources_consumption[k] * (current_t - 1) <= resources[k]
            ):
                continue

            new_resources = factory.build_robot(resources, k)
            if new_resources is not None:
                new_resources = (
                    new_resources[0] + robots[0],
                    new_resources[1] + robots[1],
                    new_resources[2] + robots[2],
                )
                new_robots = list(robots)
                new_robots[k] += 1
                max_geodes = max(
                    max_geodes,
                    dfs(new_resources, cast(Robots, tuple(new_robots)), current_t - 1),
                )

        max_geodes += robots[-1]

        visited_states[key] = max_geodes

        return max_geodes

    return dfs((0, 0, 0), (1, 0, 0, 0), t_end)
