def main(input_lines, unavailable_char='x'):
    start_ts = int(input_lines[0])
    available_buses = [(i, int(bus_id)) for i, bus_id in enumerate(input_lines[1].split(',')) if (bus_id != unavailable_char)]

    earliest_bus_id = min(available_buses, key=lambda bus: get_next_bus_departure_ts(start_ts, bus[1]))[1]
    wait_time = get_next_bus_departure_ts(start_ts, earliest_bus_id) - start_ts
    part1_answer = earliest_bus_id * wait_time

    earliest_synchronized_departure_ts = find_synchronized_departure_ts_fast(available_buses)

    return part1_answer, earliest_synchronized_departure_ts


def get_next_bus_departure_ts(start_ts, bus_id):
    bus_departure_ts = start_ts + ((bus_id - start_ts) % bus_id)
    return bus_departure_ts


def find_synchronized_departure_ts_naive(available_buses):
    largest_bus = max(available_buses, key=lambda bus: bus[1])
    largest_bus_position, largest_bus_id = largest_bus[0], largest_bus[1]

    start_ts = largest_bus_id - largest_bus_position
    while True:
        is_synchronized = True
        for bus_position, bus_id in available_buses:
            is_synchronized = (get_next_bus_departure_ts(start_ts, bus_id) == start_ts + bus_position)
            if not is_synchronized:
                break
        if is_synchronized:
            break
        start_ts += largest_bus_id
    return start_ts


def find_synchronized_departure_ts_fast(available_buses):
    first_bus_position, first_bus_id = available_buses[0]
    q, r = first_bus_id, -first_bus_position
    for position, bus_id in available_buses[1:]:
        pgcd, x, y = solve_equation_diophantienne(q, bus_id)
        offset = - (r + position)
        x, y = x * offset / pgcd, y * offset / pgcd
        q, r = bus_id * q, x * q + r
        q, r = abs(q), r % abs(q)
    return r


def solve_equation_diophantienne(a, b):
    # Assumption: a > b
    h, h_next = a, b
    q_list = []
    while h_next != 0:
        q = h // h_next
        h, h_next = h_next, h - q * h_next
        q_list.append(q)
    q_list.pop()
    pgcd = h
    x, y = 0, 1
    for q in q_list[::-1]:
        x, y = y, x - y * q
    return pgcd, x, y
