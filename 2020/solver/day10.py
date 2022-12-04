def main(
    input_lines,
    charging_outlet=0,
    device_adapter_jolt_increase=3,
    max_jolt_difference=3,
):
    adapters_chain = [int(line) for line in input_lines]
    adapters_chain.sort()
    device_adapter = adapters_chain[-1] + device_adapter_jolt_increase

    adapters_chain = [charging_outlet] + adapters_chain + [device_adapter]

    jolt_differences = compute_jolt_differences(adapters_chain, max_jolt_difference)
    part1_answer = jolt_differences[1] * jolt_differences[3]

    edges = build_graph(adapters_chain, max_jolt_difference)
    n_arrangements = find_all_paths(edges)

    return part1_answer, n_arrangements


def compute_jolt_differences(adapters_chain, max_jolt_difference):
    jolt_differences = [0] * (max_jolt_difference + 1)
    for i, adapter in enumerate(adapters_chain[:-1]):
        jolt_difference = adapters_chain[i + 1] - adapter
        jolt_differences[jolt_difference] += 1
    return jolt_differences


def build_graph(x_coordinates, max_distance):
    edges = [[] for i in range(len(x_coordinates))]
    for i, x_1 in enumerate(x_coordinates):
        for j, x_2 in enumerate(x_coordinates[i + 1 :]):
            if x_2 - x_1 <= max_distance:
                edges[i].append(i + j + 1)
    return edges


def find_all_paths(edges):
    # n_paths[i] : number of paths starting in node 'i' and finishing in the last node
    n_paths = [0] * len(edges)
    n_paths[-1] = 1
    for i in range(len(edges) - 1, -1, -1):
        for j in edges[i]:
            n_paths[i] += n_paths[j]
    return n_paths[0]
