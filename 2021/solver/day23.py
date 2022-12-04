def main(input_lines):
    part1_initial_state = parse_burrow(input_lines)
    part1_answer = a_star(part1_initial_state)

    part2_initial_state = parse_burrow(part2_update_input(input_lines))
    part2_answer = a_star(part2_initial_state)

    return part1_answer, part2_answer


def parse_burrow(input_lines):
    burrow = Burrow(room_size=len(input_lines) - 3)
    amphipod_a_types = {"A": 0, "B": 1, "C": 2, "D": 3}
    amphipod_counts = {amphipod_a_type: 0 for amphipod_a_type in amphipod_a_types}
    # Check if the burrow matches the expected layout
    is_expected_layout = True
    for i, input_line in enumerate(input_lines):
        input_line = input_line.strip()
        if 0 <= i <= 2:
            expected_len = 13
        else:
            expected_len = 9

        if len(input_line) != expected_len:
            is_expected_layout = False
            break

        if i == 0:
            is_expected_layout = input_line == "#" * expected_len
        elif i == 1:
            is_expected_layout = input_line == "#" + "." * (expected_len - 2) + "#"

        elif 2 <= i < len(input_lines) - 1:
            expected_line = ["#"] * expected_len
            for room_id, c_idx in enumerate(
                range(1 + 2 * (i == 2), expected_len - 1, 2)
            ):
                char = input_line[c_idx]
                if char not in amphipod_a_types:
                    is_expected_layout = False
                    break
                expected_line[c_idx] = char

                amphipod = Amphipod(amphipod_a_types[char], amphipod_counts[char])
                burrow.add_amphipod(amphipod, i - 2, in_hallway=False, room_id=room_id)
                amphipod_counts[char] += 1

            is_expected_layout = "".join(expected_line) == input_line

        else:  # (i == len(input_lines) - 1)
            is_expected_layout = input_line == "#" * expected_len

        if not is_expected_layout:
            raise RuntimeError("Input burrow does not match the expected layout")

    return burrow


def part2_update_input(input_lines):
    missing_lines = [
        "#D#C#B#A#",
        "#D#B#A#C#",
    ]
    updated_input_lines = input_lines[:-2] + missing_lines + input_lines[-2:]
    return updated_input_lines


def a_star(initial_state):
    cost_to_states = {initial_state: 0}
    cost_to_goal_estimates = {initial_state: initial_state.cost_to_goal_heuristic()}

    while len(cost_to_goal_estimates) > 0:
        # Find the open state with the smallest estimated cost to goal
        current_state, _current_cost_to_goal_estimate = min(
            cost_to_goal_estimates.items(), key=lambda open_state: open_state[1]
        )
        cost_to_goal_estimates.pop(current_state)

        # Close this state
        cost_to_current_state = cost_to_states[current_state]
        if current_state.is_end_state():
            return cost_to_current_state

        # Find the neighboring states
        for cost, transition in current_state.get_potential_transitions():
            new_state = current_state.copy()
            new_state.move(*transition)
            new_cost_to_state = cost_to_current_state + cost
            # Add the new state to the list of open states
            # and update the cost estimate to get to the new state (if needed)
            if (new_state not in cost_to_states) or (
                cost_to_states[new_state] > new_cost_to_state
            ):
                cost_to_states[new_state] = new_cost_to_state
                cost_to_goal_estimates[new_state] = (
                    new_cost_to_state + new_state.cost_to_goal_heuristic()
                )

    raise RuntimeError("Could not find a path to the end state")


class Amphipod(object):  # pylint: disable=useless-object-inheritance
    def __init__(self, a_type, num):
        self.a_type = a_type
        self.num = num
        self.energy_per_step = 10**a_type

    def __repr__(self):
        return str((self.a_type, self.num))

    def __hash__(self):
        return hash((self.a_type, self.num))


class Burrow(object):  # pylint: disable=useless-object-inheritance
    def __init__(self, room_size=2):
        self.hallway = [None] * 11
        self.rooms = [[None] * room_size for i in range(4)]
        self.positions_to_rooms = {2: 0, 4: 1, 6: 2, 8: 3}
        self.rooms_to_positions = {v: k for k, v in self.positions_to_rooms.items()}
        self.amphipods_positions = {}

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        # Two burrows are considered identical if they have the same amphipods in the same spots
        # To make the resulting state independent on the order of the steps that led to it, we need:
        # - to discard the amphipods' numbers
        # For the same type, we do not care whether its the amphipod 1 or 2 which is in a given spot
        # - to check the positions in the same order:
        # First, the hallway from left to right.
        # Then, the rooms from left to right, and each room from top to bottom
        all_positions = []
        for amphipod in self.hallway:
            if amphipod is not None:
                all_positions.append(amphipod.a_type)
            else:
                all_positions.append(None)
        for room in self.rooms:
            for amphipod in room:
                if amphipod is not None:
                    all_positions.append(amphipod.a_type)
                else:
                    all_positions.append(None)
        return hash(tuple(all_positions))

    # Remark: could be achieved with copy.deepcopy(self)
    def copy(self):
        self_copy = Burrow(room_size=len(self.rooms[0]))
        for room_id in self.positions_to_rooms.values():
            for position, amphipod in enumerate(self.rooms[room_id]):
                if amphipod is not None:
                    self_copy.add_amphipod(
                        amphipod, position, in_hallway=False, room_id=room_id
                    )
        for position, amphipod in enumerate(self.hallway):
            if amphipod is not None:
                self_copy.add_amphipod(amphipod, position, in_hallway=True)
        return self_copy

    def add_amphipod(self, amphipod, position, in_hallway=True, room_id=None):
        if (not in_hallway) and (room_id is None):
            raise RuntimeError(
                "A room id must be specified when adding an amphipod to a room"
            )

        if in_hallway:
            self.hallway[position] = amphipod
        else:
            self.rooms[room_id][position] = amphipod
        self.amphipods_positions[amphipod] = (position, in_hallway, room_id)

    def move(self, amphipod, new_position, new_in_hallway=True, new_room_id=None):
        # Remove the amphipod from the current position
        position, in_hallway, room_id = self.amphipods_positions[amphipod]
        if in_hallway:
            self.hallway[position] = None
        else:
            self.rooms[room_id][position] = None
        # Add the amphipod to the new position
        self.add_amphipod(
            amphipod, new_position, in_hallway=new_in_hallway, room_id=new_room_id
        )

    def is_final(self, amphipod):
        position, in_hallway, room_id = self.amphipods_positions[amphipod]
        # amphipod is still in the hallway
        if in_hallway:
            return False
        # amphipod is in the wrong room
        if amphipod.a_type != room_id:
            return False
        # amphipod is in the correct room
        # but above another amphipod of a different type (which needs to get out)
        for other_amphipod in self.rooms[room_id][position + 1 :]:
            if other_amphipod.a_type != amphipod.a_type:
                return False
        return True

    def is_end_state(self):
        for amphipod in self.amphipods_positions:
            if not self.is_final(amphipod):
                return False
        return True

    def get_valid_transition(self, amphipod, in_hallway, new_position, n_steps):
        valid_transition = None
        # Check if the amphipod is above a room
        if new_position in self.positions_to_rooms:
            # Check if it can enter the room
            room_id = self.positions_to_rooms[new_position]
            # room is of the wrong type
            if room_id != amphipod.a_type:
                return None
            room = self.rooms[room_id]
            first_empty_position = None
            for other_position, other_amphipod in enumerate(room):
                if other_amphipod is None:
                    first_empty_position = other_position
                # room is already occupied by an amphipod of a different type which needs to get out
                elif other_amphipod.a_type != amphipod.a_type:
                    return None
            # room is full
            if first_empty_position is None:
                return None
            valid_transition = (
                n_steps + 1 + first_empty_position,
                (first_empty_position, False, room_id),
            )
        # Stop in the hallway if the amphipod was not in the hallway initially
        elif not in_hallway:
            valid_transition = (n_steps, (new_position, True, None))
        return valid_transition

    def get_potential_amphipod_transitions(self, amphipod):
        position, in_hallway, room_id = self.amphipods_positions[amphipod]

        # Check if the amphipod is stuck under other amphipods
        if (
            (not in_hallway)
            and (position > 0)
            and (self.rooms[room_id][position - 1] is not None)
        ):
            return []

        potential_transitions = []

        n_steps = 0
        if in_hallway:
            hallway_position = position
        else:
            n_steps += 1 + position
            hallway_position = self.rooms_to_positions[room_id]

        # Try to go right
        for new_position in range(hallway_position + 1, len(self.hallway)):
            # Check if the spot is already occupied
            if self.hallway[new_position] is not None:
                break
            new_n_steps = n_steps + new_position - hallway_position
            valid_transition = self.get_valid_transition(
                amphipod, in_hallway, new_position, new_n_steps
            )
            if valid_transition is not None:
                potential_transitions.append(valid_transition)

        # Try to go left
        for new_position in range(hallway_position - 1, -1, -1):
            # Check if the spot is already occupied
            if self.hallway[new_position] is not None:
                break
            new_n_steps = n_steps + hallway_position - new_position
            valid_transition = self.get_valid_transition(
                amphipod, in_hallway, new_position, new_n_steps
            )
            if valid_transition is not None:
                potential_transitions.append(valid_transition)

        return potential_transitions

    def get_potential_transitions(self):
        potential_transitions = []
        for amphipod in self.amphipods_positions:
            if self.is_final(amphipod):
                continue
            for potential_transition in self.get_potential_amphipod_transitions(
                amphipod
            ):
                n_steps, (position, in_hallway, room_id) = potential_transition
                cost = n_steps * amphipod.energy_per_step
                potential_transitions.append(
                    (cost, (amphipod, position, in_hallway, room_id))
                )
        return potential_transitions

    def cost_to_goal_heuristic(self):
        # Assuming that all the non-final amphipods can move freely without hitting any amphipods
        # It gives a lower bound on the cost to reach the goal
        total_cost = 0
        for amphipod, full_position in self.amphipods_positions.items():
            if self.is_final(amphipod):
                continue

            position, in_hallway, room_id = full_position

            min_n_steps = 0
            if in_hallway:
                hallway_position = position
            else:
                min_n_steps += 1 + position
                hallway_position = self.rooms_to_positions[room_id]

            goal_hallway_position = self.rooms_to_positions[amphipod.a_type]
            min_n_steps += abs(goal_hallway_position - hallway_position) + 1

            total_cost += min_n_steps * amphipod.energy_per_step

        return total_cost
