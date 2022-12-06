from typing import List, Tuple


def main(
    input_lines: List[str], len_packet_marker: int = 4, len_msg_marker: int = 14
) -> Tuple[int, int]:
    assert len(input_lines) == 1
    data_stream_buffer: str = input_lines[0]

    part1_answer: int = find_start_marker(data_stream_buffer, len_packet_marker)

    # Remark: we could simply do:
    # part2_answer: int = find_start_marker(data_stream_buffer, len_msg_marker)

    # But part1 already gave us some information:
    # We know that position 'part1_answer' was the first position
    # where we got 'len_packet_marker' differsnt characters
    assert len_packet_marker <= len_msg_marker
    # Since 'len_packet_marker <= len_msg_marker'
    # We know that at best, the start of the msg coincides with the start of the packet
    # Thus we can warm-start the algorithm
    part2_answer: int = (
        find_start_marker(
            data_stream_buffer[part1_answer - len_packet_marker :], len_msg_marker
        )
        + part1_answer
        - len_packet_marker
    )

    return part1_answer, part2_answer


def find_start_marker(data_stream_buffer: str, len_marker: int):
    idx: int = -1
    marker: List[str] = []
    for idx, char in enumerate(data_stream_buffer):
        if len(marker) == len_marker:
            break
        if char in marker:
            # Duplicated characters, the first one cannot be part of the marker
            start_idx: int = marker.index(char)
            marker = marker[start_idx + 1 :]
        marker.append(char)
    if len(marker) != len_marker:
        idx = -1
    return idx
