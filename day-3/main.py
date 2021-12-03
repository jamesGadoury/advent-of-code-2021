# https://adventofcode.com/2021/day/3

import sys

def process_input_file(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        return [line.strip() for line in lines]

def part_one_process(diagnostics):
    print('Processing part one:')
    bin_length = len(diagnostics[0])
    bin_count = [{'0': 0, '1': 0} for _ in range(len(diagnostics[0]))]
    for binary in diagnostics:
        for i in range(bin_length):
            bin_count[i][binary[i]] += 1

    gamma_bin = ''.join(['0' if bin_count[i]['0'] > bin_count[i]['1'] else '1' for i in range(bin_length)])
    gamma_rate = int(gamma_bin, 2)

    epsilon_bin = ''.join(['1' if bin_count[i]['0'] > bin_count[i]['1'] else '0' for i in range(bin_length)])
    epsilon_rate = int(epsilon_bin, 2)

    power_consumption = gamma_rate * epsilon_rate
    print(f'The Power consumption is {power_consumption}') 

def part_two_process(diagnostics):
    print('Processing part two:')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        diagnostics = process_input_file(sys.argv[1])
        part_one_process(diagnostics)
        part_two_process(diagnostics)