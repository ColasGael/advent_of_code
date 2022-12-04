def main(input_lines):
    part1_answer, part2_answer = parse_message(input_lines)
    return part1_answer, part2_answer


def parse_message(input_lines):
    # 1. Convert from hexadecimal to binary
    bin_message = []
    for hex_char in input_lines[0]:
        bin_message.extend(hexadecimal_to_binary(hex_char))

    # 2. Parse the hierarchy of the packets
    _packet_len, packet_version_sum, output_value = parse_packet(bin_message, 0)
    return packet_version_sum, output_value


def hexadecimal_to_binary(hex_char):
    hex2bin = {
        "0": [0, 0, 0, 0],
        "1": [0, 0, 0, 1],
        "2": [0, 0, 1, 0],
        "3": [0, 0, 1, 1],
        "4": [0, 1, 0, 0],
        "5": [0, 1, 0, 1],
        "6": [0, 1, 1, 0],
        "7": [0, 1, 1, 1],
        "8": [1, 0, 0, 0],
        "9": [1, 0, 0, 1],
        "A": [1, 0, 1, 0],
        "B": [1, 0, 1, 1],
        "C": [1, 1, 0, 0],
        "D": [1, 1, 0, 1],
        "E": [1, 1, 1, 0],
        "F": [1, 1, 1, 1],
    }
    return hex2bin[hex_char]


def binary2decimal(bin_num):
    decimal_num = 0
    for bin_char in bin_num:
        decimal_num = decimal_num * 2 + bin_char
    return decimal_num


def get_operator(packet_type_id):
    packet_type_id_to_operator = {
        0: lambda prev_output_value, output_value: prev_output_value + output_value,
        1: lambda prev_output_value, output_value: prev_output_value * output_value,
        2: min,
        3: max,
        5: lambda prev_output_value, output_value: 1
        * (prev_output_value > output_value),
        6: lambda prev_output_value, output_value: 1
        * (prev_output_value < output_value),
        7: lambda prev_output_value, output_value: 1
        * (prev_output_value == output_value),
    }
    return packet_type_id_to_operator[packet_type_id]


def parse_packet(message, start_index):
    packet_len = 0

    version_num = binary2decimal(message[start_index : start_index + 3])
    packet_version_sum = version_num
    packet_len += 3

    packet_type_id = binary2decimal(
        message[start_index + packet_len : start_index + packet_len + 3]
    )
    packet_len += 3

    if packet_type_id == 4:
        subpacket_len, output_value = parse_literal(message, start_index + packet_len)
    else:
        operator_func = get_operator(packet_type_id)
        subpacket_len, subpacket_version_sum, output_value = parse_operator(
            message, start_index + packet_len, operator_func
        )
        packet_version_sum += subpacket_version_sum

    packet_len += subpacket_len

    return packet_len, packet_version_sum, output_value


def parse_literal(message, start_index):
    packet_len = 0
    literal_bin_num = []

    while message[start_index + packet_len] != 0:
        literal_bin_num.extend(
            message[start_index + packet_len + 1 : start_index + packet_len + 5]
        )
        packet_len += 5
    literal_bin_num.extend(
        message[start_index + packet_len + 1 : start_index + packet_len + 5]
    )
    packet_len += 5

    return packet_len, binary2decimal(literal_bin_num)


def parse_operator(message, start_index, operator_func):
    packet_len = 0
    total_subpackets_len = total_subpackets_count = -1

    length_id_type = message[start_index]
    packet_len += 1
    if length_id_type == 0:
        total_subpackets_len = binary2decimal(
            message[start_index + packet_len : start_index + packet_len + 15]
        )
        packet_len += 15
    else:
        total_subpackets_count = binary2decimal(
            message[start_index + packet_len : start_index + packet_len + 11]
        )
        packet_len += 11

    prev_output_value = None
    packet_version_sum = 0
    subpackets_len = subpackets_count = 0
    while (subpackets_len < total_subpackets_len) or (
        subpackets_count < total_subpackets_count
    ):
        subpacket_len, subpacket_version_sum, output_value = parse_packet(
            message, start_index + packet_len + subpackets_len
        )
        subpackets_len += subpacket_len
        subpackets_count += 1
        packet_version_sum += subpacket_version_sum

        if prev_output_value is None:
            prev_output_value = output_value
        else:
            prev_output_value = operator_func(prev_output_value, output_value)

    packet_len += subpackets_len

    return packet_len, packet_version_sum, prev_output_value
