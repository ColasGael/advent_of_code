import re
from typing import Dict, List, Tuple

import numpy as np
import numpy.typing as npt


FlowRates = Dict[str, int]
RawGraph = Dict[str, List[str]]
SimplifiedGraph = Dict[str, Dict[str, int]]
CacheKey = Tuple[str, Tuple[str, ...], int, int]

NODE_INFO_PATTERN = re.compile(
    r"^Valve (?P<node_name>[A-Z][A-Z]) has flow rate=(?P<flow_rate>\d+); "
    r"tunnel(s)* lead(s)* to valve(s)* (?P<neighbor_nodes>[A-Z][A-Z](, [A-Z][A-Z])*)$"
)


def main(
    input_lines: List[str], start_node: str = "AA", end_t: int = 30
) -> Tuple[int, int]:
    graph: RawGraph
    flow_rates: FlowRates
    graph, flow_rates = build_graph(input_lines)

    assert start_node in graph, f"Start node {start_node} not in graph"

    simplified_graph = simplify_graph(graph, flow_rates, start_node)

    part1_answer: int = find_best_pressure(
        simplified_graph, flow_rates, start_node, end_t
    )
    # After spending 4 min to teach the elephant how to open valves
    part2_answer: int = find_best_pressure(
        simplified_graph, flow_rates, start_node, end_t - 4, num_players=2
    )

    return part1_answer, part2_answer


def build_graph(input_lines: List[str]) -> Tuple[RawGraph, FlowRates]:
    graph: RawGraph = {}
    flow_rates: Dict[str, int] = {}
    for input_line in input_lines:
        match = NODE_INFO_PATTERN.match(input_line)
        if match is None:
            raise RuntimeError(f"Cannot parse input line: {input_line}")
        node_name = match.group("node_name")
        neighbor_nodes = match.group("neighbor_nodes")
        graph[node_name] = neighbor_nodes.split(", ")
        flow_rates[node_name] = int(match.group("flow_rate"))
    return graph, flow_rates


def simplify_graph(
    graph: RawGraph, flow_rates: FlowRates, start_node: str
) -> SimplifiedGraph:
    """Relies on the following observation.

    For nodes with a flow rate of 0, there is no point in opening their valves.
    Which means these nodes are just passing nodes.

    So the graph can be simplified as a graph only between nodes with flow rates > 0.
    Let's call these nodes vertices.
    BUT this time, each of the vertex is linked to all the other vertices by an edge of weight >= 1.

    The weight is the minimum number of nodes you have to pass to go from one vertex to the other.
    Ie the shortest path between the two vertices in the initial graph.
    It can be computed by running the Floyd-Warshall algorithm on the initial graph.
    """
    # Floyd-Warshall algorithm
    nodes_to_idxs: Dict[str, int] = {node: i for i, node in enumerate(graph)}

    n_nodes: int = len(graph)
    dists: npt.NDArray[np.int64] = np.full((n_nodes, n_nodes), -1, dtype=np.int64)
    for node, neighbor_nodes in graph.items():
        k = nodes_to_idxs[node]
        dists[k, k] = 0
        for neighbor_node in neighbor_nodes:
            i = nodes_to_idxs[neighbor_node]
            dists[k, i] = 1

    for k in range(n_nodes):
        for i in range(n_nodes):
            if dists[i, k] < 0:
                continue
            for j in range(n_nodes):
                if dists[k, j] < 0:
                    continue
                if dists[i, j] < 0 or dists[i, j] >= dists[i, k] + dists[k, j]:
                    dists[i, j] = dists[i, k] + dists[k, j]

    # Build the simplified graph
    vertices: List[str] = [
        node for node, flow_rate in flow_rates.items() if flow_rate > 0
    ]
    simplified_graph: SimplifiedGraph = {
        this_vertex: {
            other_vertex: dists[nodes_to_idxs[this_vertex], nodes_to_idxs[other_vertex]]
            for other_vertex in vertices
            if other_vertex != this_vertex
        }
        for this_vertex in vertices
    }
    # keep the start node for convenience
    simplified_graph[start_node] = {
        other_vertex: dists[nodes_to_idxs[start_node], nodes_to_idxs[other_vertex]]
        for other_vertex in vertices
        if other_vertex != start_node
    }

    return simplified_graph


def find_best_pressure(
    simplified_graph: SimplifiedGraph,
    flow_rates: FlowRates,
    start_node: str,
    end_t: int,
    num_players: int = 1,
) -> int:
    visited_states: Dict[CacheKey, int] = {}

    def dfs(
        current_node: str, open_valves: List[str], current_t: int, num_players: int
    ) -> int:
        key = (current_node, tuple(sorted(open_valves)), current_t, num_players)
        if key in visited_states:
            return visited_states[key]

        best_pressure = 0

        for neighbor_node, dist in simplified_graph[current_node].items():
            if neighbor_node in open_valves:
                # Valve already opened
                continue
            remaining_t = current_t - dist - 1
            if remaining_t <= 0:
                # No time to open the valve
                continue
            # Open the valve
            valve_pressure = flow_rates[neighbor_node] * remaining_t
            new_open_valves = open_valves + [neighbor_node]
            next_pressure = dfs(
                neighbor_node, new_open_valves, remaining_t, num_players
            )
            best_pressure = max(best_pressure, next_pressure + valve_pressure)

        # Add option to not do anything and let the other player open valves
        if num_players >= 2:
            best_pressure = max(
                best_pressure, dfs(start_node, open_valves, end_t, num_players - 1)
            )

        visited_states[key] = best_pressure

        return best_pressure

    return dfs(start_node, [], end_t, num_players)
