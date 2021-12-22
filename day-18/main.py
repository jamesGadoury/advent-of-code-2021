# https://adventofcode.com/2021/day/18

import sys
import logging
import json
from dataclasses import dataclass
from math import floor, ceil
from itertools import permutations
from multiprocessing import Pool
from copy import deepcopy

SAMPLE_INPUT='./sample_input.txt'

def parse_file(input_file_name):
    with open(input_file_name) as f:
        return [json.loads(line.strip()) for line in f.readlines()]


def add_snail_numbers(a, b):
    return [a, b] 


def test_add_snail_numbers():
    assert add_snail_numbers([1,2], [[3,4],5]) == [[1,2],[[3,4],5]]


@dataclass 
class SnailNumberData:
    number: list
    pair_indices: list
    nat_indices: list

    def can_explode(self):
        logging.debug(f'in can_explode, pair_indices={self.pair_indices}')
        for indices in self.pair_indices:
            # by default how the recurse function works, the first tuple of indices that
            # access a pair that has length of 4, is the left most pair that is nested inside four pairs
            if len(indices) == 4:
                logging.debug(f'in can_explode, found indices that can explode={indices}')
                return indices
        return False

    def can_split(self):
        logging.debug(f'in can_split, nat_indices={self.nat_indices}')
        for indices in self.nat_indices:
            if self.number_at_index_tuple(indices) == 10:
                logging.debug(f'in can_explode, found indices that can explode={indices}')
                return indices
        return False

    def number_at_index_tuple(self, index_tuple):
        assert type(index_tuple) == tuple
        assert len(index_tuple) > 0
        number = self.number
        for index in index_tuple:
            number = number[index]
        assert type(number) == int
        return number

    def update_element(self, index_tuple, value):
        assert type(index_tuple) == tuple
        assert len(index_tuple) > 1
        logging.debug(f'update_element called with index_tuple={index_tuple}, value={value}')
        # taking advantage of fact that returning a list from list gives it by reference, so 
        # we can update it and mutate the original list
        pair = self.number
        for i in range(len(index_tuple)-1):
            pair = pair[index_tuple[i]]

        pair[index_tuple[-1]] = value
        # we might have changed a natural number to a pair or vice-versa, re-populate our indices members:
        self.pair_indices, self.nat_indices = recurse_snail(self.number)


    def explode(self):
        logging.debug(f'explode called with {self}')
        for i in range(len(self.nat_indices)):
            if len(self.nat_indices[i]) == 5:
                logging.debug(f'in explode, entered the condition for processing left natural' \
                    f' number of pair within 4 pairs with nat_indices[i]={self.nat_indices[i]}')
                # this is left most natural number that is within 4 pairs
                if i - 1 >= 0:
                    # nat number to left will be at index of indices to left of this one
                    # if it exists, add this one to it
                    logging.debug(f'in explode, nat_indices[i-1]={self.nat_indices[i-1]}')
                    new_number = self.number_at_index_tuple(self.nat_indices[i-1]) + \
                                self.number_at_index_tuple(self.nat_indices[i])
                    logging.debug(f'in explode, new_number for left element={new_number}')
                    self.update_element(self.nat_indices[i-1], new_number)

                if i + 2 < len(self.nat_indices):
                    # nat number to right of the nat number this is in pair with is 1 index to right 
                    # if number exists to right of that, add the number to right of this to that
                    logging.debug(f'in explode, nat_indices[i+1]={self.nat_indices[i+1]}')
                    logging.debug(f'in explode, nat_indices[i+2]={self.nat_indices[i+2]}')
                    new_number = self.number_at_index_tuple(self.nat_indices[i+1]) + \
                                self.number_at_index_tuple(self.nat_indices[i+2])
                    
                    logging.debug(f'in explode, new_number for right element={new_number}')
                    self.update_element(self.nat_indices[i+2], new_number)

                # now update the pair at this indices entry with 0
                self.update_element(self.nat_indices[i][0:-1], 0)

                return True
        return False

    def split(self):
        logging.debug(f'in split, {self}')
        for indices in self.nat_indices:
            number = self.number_at_index_tuple(indices)
            if  number >= 10:
                logging.debug(f'in split, found indices that can split={indices}')
                self.update_element(indices, [floor(number/2.0), ceil(number/2.0)])
                return True
        return False


def recurse_snail(snail_number, curr_indices=()):
    '''Returns list of indices that can be entered into original snail number to access a pair'''
    assert type(snail_number) == list
    pair_indices = []
    nat_indices = []
    for i in range(len(snail_number)):
        if type(snail_number[i]) == list:
            pair_indices.append((*curr_indices, i))
            deeper_pair_indices, deeper_nat_indices = recurse_snail(snail_number[i], (*curr_indices, i))
            pair_indices = [*pair_indices, *deeper_pair_indices]
            nat_indices = [*nat_indices, *deeper_nat_indices]
        elif type(snail_number[i]) == int:
            nat_indices.append((*curr_indices, i))
    return pair_indices, nat_indices


def create_snail_data(snail_number):
    pair_indices, nat_indices = recurse_snail(snail_number)
    return SnailNumberData(deepcopy(snail_number), pair_indices, nat_indices)


def test_explode():
    snail_number_data = create_snail_data([[[[[9,8],1],2],3],4])
    assert snail_number_data.explode()
    assert  snail_number_data.number == [[[[0,9],2],3],4]
    for indices in snail_number_data.nat_indices:
        # this will call asserts and ensure our indices were properly updated
        snail_number_data.number_at_index_tuple(indices)


def test_create_snail_data_pair_indices():
    assert create_snail_data([[[[10, 8], 1], 12], [15, 17]]).pair_indices == [(0,), (0, 0), (0, 0, 0), (1,)]


def test_can_explode():
    assert create_snail_data([[[[[9,8],1],2],3],4]).can_explode() == (0, 0, 0, 0)


def reduce(snail_number):
    logging.debug(f'reduce called with snail_number={snail_number}')
    snail_number_data = create_snail_data(snail_number) 
    logging.debug(f'in reduce, created snail_number_data={snail_number_data}')
    while True:
        if snail_number_data.explode():
            logging.debug(f'in reduce, after explode was called successfully, snail_number_data={snail_number_data}')
            continue
        if snail_number_data.split():
            logging.debug(f'in reduce, after split was called successfully, snail_number_data={snail_number_data}')
            continue
        break 
    logging.debug(f'exiting reduce with snail_number={snail_number_data.number}')
    return snail_number_data.number


def final_sum(snail_number_list):
    assert len(snail_number_list) > 0
    final_sum = snail_number_list[0]
    for i in range(1, len(snail_number_list)):
        final_sum = reduce(add_snail_numbers(final_sum, snail_number_list[i]))
    return final_sum


def test_final_sum_a():
    assert final_sum([[1,1], [2,2], [3,3], [4,4]]) == [[[[1,1],[2,2]],[3,3]],[4,4]]


def test_final_sum_b():
    assert final_sum([[1,1], [2,2], [3,3], [4,4], [5,5]]) == [[[[3,0],[5,3]],[4,4]],[5,5]]


def test_final_sum_c():
    assert final_sum([[1,1], [2,2], [3,3], [4,4], [5,5], [6,6]]) == [[[[5,0],[7,4]],[5,5]],[6,6]]


def test_final_sum_d():
    numbers = [[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
                [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
                [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
                [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
                [7,[5,[[3,8],[1,4]]]],
                [[2,[2,2]],[8,[8,1]]],
                [2,9],
                [1,[[[9,3],9],[[9,0],[0,7]]]],
                [[[5,[7,4]],7],1],
                [[[[4,2],2],6],[8,7]]]

    assert final_sum(numbers) == [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]


def test_final_sum_sample():
    numbers = [[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
                [[[5,[2,8]],4],[5,[[9,9],0]]],
                [6,[[[6,2],[5,6]],[[7,6],[4,7]]]],
                [[[6,[0,7]],[0,9]],[4,[9,[9,0]]]],
                [[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]],
                [[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]],
                [[[[5,4],[7,7]],8],[[8,3],8]],
                [[9,3],[[9,9],[6,[4,9]]]],
                [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
                [[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]]
    assert final_sum(numbers) == [[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]


def calc_magnitude(snailfish_number):
    assert type(snailfish_number) == list
    left_mag = 3 * (snailfish_number[0] if type(snailfish_number[0]) == int else calc_magnitude(snailfish_number[0]))
    right_mag = 2 * (snailfish_number[1] if type(snailfish_number[1]) == int else calc_magnitude(snailfish_number[1]))
    return left_mag + right_mag


def test_calc_magnitude_a():
    assert calc_magnitude([9,1]) == 29


def test_calc_magnitude_b():
    assert calc_magnitude([[9,1],[1,9]]) == 129


def test_calc_magnitude_c():
    assert calc_magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]) == 3488


def test_calc_magnitude_d():
    assert calc_magnitude([[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]) == 4140


def magnitude_of_sum(numbers):
    return calc_magnitude(final_sum(numbers))


def part_one(input_file_name):
    '''
    Add up all of the snailfish numbers from the homework assignment in the order they appear. 
    What is the magnitude of the final sum?
    '''
    snailfish_numbers = parse_file(input_file_name)
    logging.debug(f'in part_one: snailfish_numbers={snailfish_numbers}')
    # return calc_magnitude(final_sum(snailfish_numbers))
    return magnitude_of_sum(snailfish_numbers)


def test_part_one():
    assert part_one(SAMPLE_INPUT) == 4140 


def part_two(input_file_name):
    '''
    What is the largest magnitude of any sum of two different snailfish numbers from the homework assignment?
    '''
    snailfish_numbers = parse_file(input_file_name)

    logging.debug(f'in part_two: snailfish_numbers={snailfish_numbers}')
    
    # need to deepcopy so that we don't mutate shared lists
    add_permutations = [(deepcopy(number_a), deepcopy(number_b)) for number_a, number_b in permutations(snailfish_numbers, 2)]
    logging.debug(f'in part_two, add_permutations={add_permutations}')
     
    with Pool(15) as pool:
        magnitudes = pool.map(magnitude_of_sum, add_permutations)

    logging.info(f'in part_two: magnitudes={magnitudes}')

    return max(magnitudes)


def test_part_two():
    assert part_two(SAMPLE_INPUT) == 3993
    

def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return

    logging.basicConfig(filename='debug_main.log', level=logging.DEBUG)
    print(f'part_one: {part_one(args[1])}')
    print(f'part_two: {part_two(args[1])}')


if __name__ == '__main__':
    main(sys.argv)