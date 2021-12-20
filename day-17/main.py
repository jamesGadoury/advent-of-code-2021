# https://adventofcode.com/2021/day/17

import sys
from dataclasses import dataclass
import logging

@dataclass
class TargetArea:
    x_range : tuple
    y_range : tuple

def parse_file(input_file_name):
    with open(input_file_name) as f:
        # input should be a single line
        input = f.readlines()
        assert len(input) == 1

        logging.debug(f'in parse_file, input={input}')

        elements = input[0].strip().split(' ')
        logging.debug(f'in parse_file, elements={elements}')
        assert len(elements) == 4

        x_section = elements[2]
        x_rng_start_idx = int(x_section.index('=') + 1)
        x_rng_end_idx = int(x_section.index(','))
        x_range = [int(value) for value in x_section[x_rng_start_idx:x_rng_end_idx].split('..')]

        y_section = elements[3]
        y_rng_start_idx = int(y_section.index('=') + 1)
        y_range = [int(value) for value in y_section[y_rng_start_idx:].split('..')]

        return TargetArea(x_range=x_range, y_range=y_range)

def part_one(input_file_name):
    '''
    Find the initial velocity that causes the probe to reach the highest y position and still eventually be 
    within the target area after any step. What is the highest y position it reaches on this trajectory?
    '''
    target_area = parse_file(input_file_name)
    logging.debug(f'in part_one, target_area={target_area}')

    return -1


def test_part_one():
    assert part_one('./sample_input.txt') == 45
        

def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return

    logging.basicConfig(filename='debug_main.log', level=logging.DEBUG)

    print(f'part_one: {part_one(args[1])}')

if __name__ == '__main__':
    main(sys.argv)
