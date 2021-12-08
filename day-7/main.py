# https://adventofcode.com/2021/day/7

import sys

def crab_positions(file_input):
    '''Return horizontal positions of crabs from file input'''
    with open(file_input) as f:
        return [int(position) for position in f.readline().split(',')]


def part_one(file_input):
    positions = crab_positions(file_input)

    def fuel_cost_to_align_at_position(crab_positions, position):
        return sum(list(map(lambda crab_position: abs(crab_position-position), crab_positions)))

    fuel_costs = [fuel_cost_to_align_at_position(positions, position) for position in range(max(positions))]

    print(f'Part One: Minimum fuel cost to align all crabs at a position: {min(fuel_costs)}')

def part_two(file_input):
    positions = crab_positions(file_input)

    def fuel_cost(steps):
        return int(steps*(1+steps)/2) if steps > 0 else steps

    def fuel_cost_to_align_at_position(crab_positions, position):
        return sum(list(map(lambda crab_position: fuel_cost(abs(crab_position-position)), crab_positions)))

    fuel_costs = [fuel_cost_to_align_at_position(positions, position) for position in range(max(positions))]

    print(f'Part Two: Minimum fuel cost to align all crabs at a position with accurate fuel estimation: {min(fuel_costs)}')

def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return

    part_one(args[1])
    part_two(args[1])

if __name__ == '__main__':
    main(sys.argv)