# https://adventofcode.com/2021/day/19

import sys
from dataclasses import dataclass
import numpy as np


@dataclass
class ScannerReport:
    scanner_id: int
    readings: np.array


def part_file(input_file_name):
    '''Read input_file_name file and return scanner readings'''
    with open(input_file_name) as f:
        lines = [line.strip() for line in f.readlines()]
        for i in range(len(lines)):
            pass


def part_one(input_file_name):
    '''
    Assemble the full map of beacons. How many beacons are there?
    '''
    pass


def test_part_one():
    assert part_one('./sample_input.txt') == 79


def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return


if __name__ == '__main__':
    main(sys.argv)
