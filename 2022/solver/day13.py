import json
from typing import List, Tuple, Union


Packet = List[Union[int, "Packet"]]


def main(input_lines: List[str]) -> Tuple[int, int]:
    packet_pairs: List[Tuple[Packet, Packet]] = parse_packets(input_lines)

    part1_answer: int = count_correct_order_packets(packet_pairs)
    part2_answer: int = get_decoder_key(packet_pairs)

    return part1_answer, part2_answer


def parse_packets(input_lines: List[str]) -> List[Tuple[Packet, Packet]]:
    input_lines.append("")
    assert len(input_lines) % 3 == 0

    packet_pairs: List[Tuple[Packet, Packet]] = []
    for i in range(0, len(input_lines), 3):
        left_packet: Packet = json.loads(input_lines[i])
        right_packet: Packet = json.loads(input_lines[i + 1])
        assert (
            len(input_lines[i + 2]) == 0
        ), "Missing separator line between packet pairs at line {i + 3}"

        packet_pairs.append((left_packet, right_packet))

    return packet_pairs


def compare_packets(left_packet: Packet, right_packet: Packet) -> int:
    max_len: int = max(len(left_packet), len(right_packet))
    for i in range(max_len):
        if i >= len(left_packet):
            return 1
        if i >= len(right_packet):
            return -1
        left_el = left_packet[i]
        right_el = right_packet[i]
        if isinstance(left_el, int) and isinstance(right_el, int):
            if left_el < right_el:
                return 1
            if left_el > right_el:
                return -1
        else:
            left_el_packet: Packet
            if isinstance(left_el, list):
                left_el_packet = left_el
            else:
                left_el_packet = [left_el]
            right_el_packet: Packet
            if isinstance(right_el, list):
                right_el_packet = right_el
            else:
                right_el_packet = [right_el]
            result = compare_packets(left_el_packet, right_el_packet)
            if result != 0:
                return result
    return 0


def less_than_packet(packet_1: Packet, packet_2):
    return compare_packets(packet_1, packet_2) in (0, 1)


def count_correct_order_packets(packet_pairs: List[Tuple[Packet, Packet]]) -> int:
    num_right_order_packets: int = 0
    for i, packet_pair in enumerate(packet_pairs, start=1):
        assert (
            len(packet_pair) == 2
        ), f"Packet pair should be of len 2, got {len(packet_pair)} insted"
        if less_than_packet(*packet_pair):
            num_right_order_packets += i
    return num_right_order_packets


def get_decoder_key(packet_pairs: List[Tuple[Packet, Packet]]) -> int:
    # Divider packets
    divider_packet_1: Packet = [[2]]
    divider_packet_2: Packet = [[6]]
    if less_than_packet(divider_packet_2, divider_packet_1):
        divider_packet_2, divider_packet_1 = divider_packet_1, divider_packet_2

    # Find the index of the divider packets in the sorted packets
    divider_packet_1_idx: int = 1
    divider_packet_2_idx: int = 1

    packets: List[Packet] = [
        packet for packet_pair in packet_pairs for packet in packet_pair
    ]
    for packet in packets:
        if less_than_packet(packet, divider_packet_1):
            divider_packet_1_idx += 1
        elif less_than_packet(packet, divider_packet_2):
            divider_packet_2_idx += 1
    divider_packet_2_idx += divider_packet_1_idx

    return divider_packet_1_idx * divider_packet_2_idx
