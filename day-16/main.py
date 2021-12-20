# https://adventofcode.com/2021/day/16

import sys
from dataclasses import dataclass
import logging

# this follows the hex to binary table for the problem
HEX_TO_BINARY = {
    '0' : '0000',
    '1' : '0001',
    '2' : '0010',
    '3' : '0011',
    '4' : '0100',
    '5' : '0101',
    '6' : '0110',
    '7' : '0111',
    '8' : '1000',
    '9' : '1001',
    'A' : '1010',
    'B' : '1011',
    'C' : '1100',
    'D' : '1101',
    'E' : '1110',
    'F' : '1111',
}


def hex_to_binary_string(hex_string):
    return ''.join([HEX_TO_BINARY[hex_value] for hex_value in hex_string])


def test_hex_to_binary_a():
    assert hex_to_binary_string('D2FE28') == '110100101111111000101000'


def test_hex_to_binary_b():
    assert hex_to_binary_string('38006F45291200') == '00111000000000000110111101000101001010010001001000000000'


def parse_file(input_file_name):
    with open(input_file_name) as f:
        # input likely will be one line, but we will group them together anyways
        return hex_to_binary_string(''.join([line.strip() for line in f.readlines()]))


def test_parse_file():
    assert parse_file('./sample_input.txt') == '00111000000000000110111101000101001010010001001000000000'


def bin_to_int(binary_string):
    return int(binary_string, 2)


def test_bin_to_int():
    assert bin_to_int('100') == 4


GARBAGE = -1


def parse_binary(binary):
    '''Returns value of binary and number of bits'''
    if binary == '':
        return GARBAGE, GARBAGE

    return bin_to_int(binary), len(binary)


def padding_for_length(length_of_packet):
    '''calculate the number of padded bits to fit the length of a packet into hexadecimal representation'''
    return int(-length_of_packet % 4)


def test_padding_for_length():
    assert padding_for_length(21) == 3


@dataclass
class PacketHeader:
    version: int
    type_id: int
    length: int = 6


def create_packet_header(binary_string, i):
    logging.debug(f'create_packet_header called with binary_string={binary_string}')
    i = int(i)
    logging.debug(f'create_packet_header called with i={i}')
    packet_version, version_bits = parse_binary(binary_string[i:i+3])
    type_id, type_id_bits = parse_binary(binary_string[i+3:i+6])

    if packet_version == GARBAGE or type_id == GARBAGE:
        return GARBAGE, GARBAGE
    return PacketHeader(version=packet_version, type_id=type_id), i+version_bits+type_id_bits


LITERAL_VALUE_PACKET = 4

@dataclass
class LiteralValuePacket:
    header: PacketHeader
    value_: int

    def value(self):
        '''Used to satisfy interface req for processing operator packet'''
        return self.value_


def create_literal_value_packet(binary_string, i, header):
    logging.debug(f'create_literal_value_packet called with binary_string={binary_string}, ' \
                  f'i={i}, header={header}')

    assert header.type_id == LITERAL_VALUE_PACKET
    
    parsing_value = True
    value_binary = ''
    while parsing_value:
        if binary_string[i] == '0':
            # this is the last group, stop parsing after we are done with this one
                parsing_value = False
        # add this group to the value binary, remember to ignore first bit
        value_binary +=  binary_string[i+1:i+5]
        i = i + 5
    logging.debug(f'in create_literal_value_packet: value_binary={value_binary}')
    
    value, _ = parse_binary(value_binary)
    if value == GARBAGE:
        return GARBAGE, GARBAGE
    return LiteralValuePacket(header=header, value_=value), i


def test_create_literal_value_packet():
    binary = hex_to_binary_string('D2FE28')
    header, i = create_packet_header(binary, 0)
    packet, i = create_literal_value_packet(binary, i, header)
    assert packet.header.version == 6
    assert packet.header.type_id == LITERAL_VALUE_PACKET
    assert packet.value() == 2021
    assert i == 21


SUM_ID = 0
PRODUCT_ID = 1
MIN_ID = 2
MAX_ID = 3
GREATER_THAN_ID = 5
LESS_THAN_ID = 6
EQUAL_TO_ID = 7

def sum_packet_values(packets):
    logging.debug(f'sum_packet_values called with packets={packets}')
    assert len(packets) > 0
    sum = packets[0].value()
    for i in range(1, len(packets)):
        sum += packets[i].value()
    return sum

def multiply_packet_values(packets):
    logging.debug(f'multiply_packet_values called with packets={packets}')
    assert len(packets) > 0
    product = packets[0].value()
    for i in range(1, len(packets)):
        product *= packets[i].value()
    return product

def min_packet_values(packets):
    logging.debug(f'min_packet_values called with packets={packets}')
    assert len(packets) > 0
    return min([packet.value() for packet in packets])


def max_packet_values(packets):
    logging.debug(f'max_packet_values called with packets={packets}')
    assert len(packets) > 0
    return max([packet.value() for packet in packets])

def greater_than_packet_values(packets):
    logging.debug(f'greater_than_packet_values called with packets={packets}')
    # condition provided by code problem
    assert len(packets) == 2
    return 1 if packets[0].value() > packets[1].value() else 0


def less_than_packet_values(packets):
    logging.debug(f'less_than_packet_values called with packets={packets}')
    # condition provided by code problem
    assert len(packets) == 2
    return 1 if packets[0].value() < packets[1].value() else 0


def equal_packet_values(packets):
    logging.debug(f'equal_packet_values called with packets={packets}')
    # condition provided by code problem
    assert len(packets) == 2
    return 1 if packets[0].value() == packets[1].value() else 0


@dataclass
class OperatorPacket:
    header: PacketHeader
    length_type_id: int
    sub_packets: list

    def value(self):
        if self.header.type_id == SUM_ID:
            return sum_packet_values(self.sub_packets)
        if self.header.type_id == PRODUCT_ID:
            return multiply_packet_values(self.sub_packets)
        if self.header.type_id ==  MIN_ID:
            return min_packet_values(self.sub_packets)
        if self.header.type_id == MAX_ID:
            return max_packet_values(self.sub_packets)
        if self.header.type_id == GREATER_THAN_ID:
            return greater_than_packet_values(self.sub_packets)
        if self.header.type_id == LESS_THAN_ID:
            return less_than_packet_values(self.sub_packets)
        if self.header.type_id == EQUAL_TO_ID:
            return equal_packet_values(self.sub_packets)

TOTAL_LENGTH_IN_BITS_TYPE = 0
NUMBER_OF_SUB_PACKETS_TYPE = 1


def parse_total_length_in_bits_type(binary_string, i, header):
    logging.debug(f'parse_total_length_in_bits_type called with binary_string={binary_string}, ' \
                  f'i={i}, header={header}')

    total_length_in_bits, tlib_bit_count = parse_binary(binary_string[i:i+15])
    if total_length_in_bits == GARBAGE:
        return GARBAGE, GARBAGE

    i = i + tlib_bit_count
    logging.debug(f'in parse_total_length_in_bits_type, total_length_in_bits={total_length_in_bits}') 
    sub_packets, i = parse_packets(binary_string, i, lambda i_start, i_current, packets : i_current - i_start < total_length_in_bits)

    return OperatorPacket(header=header, length_type_id=TOTAL_LENGTH_IN_BITS_TYPE, sub_packets=sub_packets), i


def parse_number_of_sub_packets_type(binary_string, i, header):
    logging.debug(f'parse_number_of_sub_packets_type called with binary_string={binary_string}, ' \
                  f'i={i}, header={header}')

    number_of_sub_packets, nosp_bit_count = parse_binary(binary_string[i:i+11])
    if number_of_sub_packets == GARBAGE:
        return GARBAGE, GARBAGE

    i = i + nosp_bit_count 

    logging.debug(f'in parse_number_of_sub_packets_type, number_of_sub_packets={number_of_sub_packets}') 
    sub_packets, i = parse_packets(binary_string, i, lambda i_start, i_current, packets : len(packets) < number_of_sub_packets)

    return OperatorPacket(header=header, length_type_id=NUMBER_OF_SUB_PACKETS_TYPE, sub_packets=sub_packets), i


def create_operator_packet(binary_string, i, header):
    logging.debug(f'create_operator_packet called with binary_string={binary_string}, ' \
                  f'i={i}, header={header}')
    assert header.type_id != LITERAL_VALUE_PACKET

    length_type_id, lti_bit_count = parse_binary(binary_string[i])
    if length_type_id == GARBAGE:
        return GARBAGE, GARBAGE

    i = i + lti_bit_count

    if length_type_id == TOTAL_LENGTH_IN_BITS_TYPE:
        return parse_total_length_in_bits_type(binary_string, i, header)

    if length_type_id == NUMBER_OF_SUB_PACKETS_TYPE:
        return parse_number_of_sub_packets_type(binary_string, i, header)

    raise ValueError(f'input binary_string: {binary_string} has unsupported length_type_id!')


def test_create_operator_packet_total_length_type():
    binary = hex_to_binary_string('38006F45291200')
    header, i = create_packet_header(binary, 0)
    packet, i = create_operator_packet(binary, i, header)
    assert packet.header.version == 1
    assert packet.header.type_id == 6
    assert packet.length_type_id == TOTAL_LENGTH_IN_BITS_TYPE
    assert packet.sub_packets[0].value() == 10
    assert packet.sub_packets[1].value() == 20


def test_create_operator_packet_number_of_sub_packets_type():
    binary = hex_to_binary_string('EE00D40C823060')
    header, i = create_packet_header(binary, 0)
    packet, i = create_operator_packet(binary, i, header)
    assert packet.header.version == 7
    assert packet.header.type_id == 3
    assert packet.length_type_id == NUMBER_OF_SUB_PACKETS_TYPE
    assert packet.sub_packets[0].value() == 1
    assert packet.sub_packets[1].value() == 2
    assert packet.sub_packets[2].value() == 3

def test_operator_packet_value_a():
    binary = hex_to_binary_string('C200B40A82')
    header, i = create_packet_header(binary, 0)
    packet, i = create_operator_packet(binary, i, header)
    assert packet.value() == 3


def test_operator_packet_value_b():
    binary = hex_to_binary_string('04005AC33890')
    header, i = create_packet_header(binary, 0)
    packet, i = create_operator_packet(binary, i, header)
    assert packet.value() == 54


def test_operator_packet_value_c():
    binary = hex_to_binary_string('880086C3E88112')
    header, i = create_packet_header(binary, 0)
    packet, i = create_operator_packet(binary, i, header)
    assert packet.value() == 7


def test_operator_packet_value_d():
    binary = hex_to_binary_string('CE00C43D881120')
    header, i = create_packet_header(binary, 0)
    packet, i = create_operator_packet(binary, i, header)
    assert packet.value() == 9


def test_operator_packet_value_e():
    binary = hex_to_binary_string('D8005AC2A8F0')
    header, i = create_packet_header(binary, 0)
    packet, i = create_operator_packet(binary, i, header)
    assert packet.value() == 1


def test_operator_packet_value_f():
    binary = hex_to_binary_string('F600BC2D8F')
    header, i = create_packet_header(binary, 0)
    packet, i = create_operator_packet(binary, i, header)
    assert packet.value() == 0


def test_operator_packet_value_g():
    binary = hex_to_binary_string('9C005AC2F8F0')
    header, i = create_packet_header(binary, 0)
    packet, i = create_operator_packet(binary, i, header)
    assert packet.value() == 0


def test_operator_packet_value_h():
    binary = hex_to_binary_string('9C0141080250320F1802104A08')
    header, i = create_packet_header(binary, 0)
    packet, i = create_operator_packet(binary, i, header)
    assert packet.value() == 1


def parse_packets(binary_string, i=0, keep_looping=None):
    logging.debug(f'parse_packets called with binary_string={binary_string} w/ length:{len(binary_string)}, ' \
                  f'i={i}, keep_looping={keep_looping}')

    i_start = i
    if keep_looping is None:
        keep_looping = lambda i_start, i_current, packets : i_current < len(binary_string)

    packets = []

    while (keep_looping(i_start, i, packets)):
        logging.debug(f'in parse_packets, i-start_i={i-i_start}')
        # start parsing packet
        header, i = create_packet_header(binary_string, i)
        if header == GARBAGE:
            break
        logging.debug(f'in parse_packets, header={header}, i={i}')
        if header.type_id == LITERAL_VALUE_PACKET:
            packet, i = create_literal_value_packet(binary_string, i, header)
            logging.debug(f'in parse_packets, packet={packet}, i={i} after create_literal_value_packet is called')
            if packet == GARBAGE:
                break

            packets.append(packet)
            continue

        packet, i = create_operator_packet(binary_string, i, header)
        if packet == GARBAGE:
            break
        logging.debug(f'in parse_packets, packet={packet}, i={i} after create_operator_packet is called')
        packets.append(packet)

    return packets, i


def recurse_retrieve_versions(packets):
    logging.debug(f'recurse_retrieve_versions called with packets={packets}')
    versions = []
    for packet in packets:
        versions.append(packet.header.version)
        if packet.header.type_id == LITERAL_VALUE_PACKET:
            continue
        # not a literal value packet, this is an operator, recurse through its sub_packets
        sub_packet_versions = recurse_retrieve_versions(packet.sub_packets)
        for version in sub_packet_versions:
            versions.append(version)
    return versions 


def part_one(input_file_name):
    '''
    Decode the structure of your hexadecimal-encoded BITS transmission; 
    what do you get if you add up the version numbers in all packets?
    '''

    binary = parse_file(input_file_name)
    packets, _ = parse_packets(binary)
    logging.debug(f'in part_one, packets={packets}')
    version_numbers = recurse_retrieve_versions(packets)
    logging.debug(f'in part_one, version_numbers={version_numbers}')
    return sum(version_numbers)

def part_two(input_file_name):
    '''
    Using the operator rules, you can now work out the value of the outermost packet in your BITS transmission.
    What do you get if you evaluate the expression represented by your hexadecimal-encoded BITS transmission?
    '''
    binary = parse_file(input_file_name)
    packets, _ = parse_packets(binary)
    logging.debug(f'in part_two, packets={packets}')
    # when parse_packets is called to parse an entire hex, it will return a list with a single packet in it
    # either it will be a literal value packet or a operator packet (which will have sub packets)
    assert len(packets) == 1
    value = packets[0].value()
    logging.debug(f'in part_one, value={value}')
    return value

def test_part_one():
    assert part_one('./sample_input.txt') == 9


def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return

    logging.basicConfig(filename='main_debug.log', level=logging.DEBUG)
    print(f'part_one: {part_one(args[1])}')
    print(f'part_two: {part_two(args[1])}')

if __name__ == '__main__':
    main(sys.argv)
