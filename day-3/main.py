# https://adventofcode.com/2021/day/3

import sys

def process_input_file(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        return [line.strip() for line in lines]

def calc_bit_frequencies(diagnostics):
    binary_length = len(diagnostics[0])
    bit_frequencies = [{'0': 0, '1': 0} for _ in range(binary_length)]
    for binary in diagnostics:
        for i in range(binary_length):
            bit_frequencies[i][binary[i]] += 1
    return bit_frequencies

def most_common_bits(diagnostics, value_if_equal='0'):
    bit_frequencies = calc_bit_frequencies(diagnostics)
    return [value_if_equal if bit_frequency['0'] == bit_frequency['1'] else '0' if bit_frequency['0'] > bit_frequency['1'] else '1' for bit_frequency in bit_frequencies]

def least_common_bits(diagnostics, value_if_equal='0'):
    bit_frequencies = calc_bit_frequencies(diagnostics)
    return [value_if_equal if bit_frequency['0'] == bit_frequency['1'] else '1' if bit_frequency['0'] > bit_frequency['1'] else '0' for bit_frequency in bit_frequencies]

def part_one_process(diagnostics):
    print('Processing part one:')

    gamma_binary = ''.join(most_common_bits(diagnostics))
    gamma_rate = int(gamma_binary, 2)

    epsilon_binary = ''.join(least_common_bits(diagnostics))
    epsilon_rate = int(epsilon_binary, 2)

    power_consumption = gamma_rate * epsilon_rate
    print(f'The Power consumption is {power_consumption}') 

def rating_binary(diagnostics, bit_criteria, equivalence_value):
    copy_diagnostics = [binary for binary in diagnostics]
    binary_length = len(copy_diagnostics[0])
    for i in range(binary_length):
        if (len(copy_diagnostics) == 1):
            break
        bit_criteria_bits = bit_criteria(copy_diagnostics, equivalence_value)
        copy_diagnostics = list(filter(lambda binary: binary[i] == bit_criteria_bits[i], copy_diagnostics))

    return copy_diagnostics[0]

def part_two_process(diagnostics):
    print('Processing part two:')
    
    oxygen_gen_rating_bin = rating_binary(diagnostics, most_common_bits, '1')
    oxygen_gen_rating = int(oxygen_gen_rating_bin, 2)
    print(f'Oxygen generation rating is {oxygen_gen_rating}')

    co2_scrubber_rating_bin = rating_binary(diagnostics, least_common_bits, '0')
    co2_scrubber_rating = int(co2_scrubber_rating_bin, 2)
    print(f'CO2 Scrubber rating is {co2_scrubber_rating}')

    life_support_rating = oxygen_gen_rating * co2_scrubber_rating
    print(f'The Life support rating is {life_support_rating}')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        diagnostics = process_input_file(sys.argv[1])
        part_one_process(diagnostics)
        part_two_process(diagnostics)