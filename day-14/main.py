# https://adventofcode.com/2021/day/14

import sys
import logging

def test_part_one():
    assert part_one('./sample_input.txt') == 1588

def test_part_two():
    assert part_two('./sample_input.txt') == 2188189693529

def test_4_steps():
    assert apply_steps('./sample_input.txt', 4) == 18

def test_20_steps():
    assert apply_steps('./sample_input.txt', 20) == 1961318

def parse_file(input_file_name):
    with open(input_file_name) as f:
        lines = [line.split() for line in f.readlines()]
        template = lines[0][0]
        pair_insertion_rules = {line[0]: line[0][0]+line[2] for line in lines[2:]}
        return (template, pair_insertion_rules)

# nn -> nc, cn -> nb, bc, cc, cn

# Template:     NNCB
# After step 1: NCNBCHB
# After step 2: NBCCNBBBCBHCB

def apply_steps(input_file_name, step_count):
    '''
    Apply step_count steps of pair insertion rules and subtract the quantity of the least common element 
    from the quantity of the most common element
    '''
    template, pair_insertion_rules = parse_file(input_file_name)

    pair_counts = {}
    for i in range(len(template)-1):
        pair = template[i:i+2]
        pair_counts[pair] = 1 if pair not in pair_counts else pair_counts[pair]+1

    for _ in range(step_count):
        updated_pair_counts = {}
        for pair, count in pair_counts.items():
            pair_a = pair_insertion_rules[pair]
            pair_b = pair_a[1]+pair[1]
            updated_pair_counts[pair_a] = count if pair_a not in updated_pair_counts else updated_pair_counts[pair_a]+count
            updated_pair_counts[pair_b] = count if pair_b not in updated_pair_counts else updated_pair_counts[pair_b]+count
        pair_counts = updated_pair_counts
    logging.debug(f'pair_counts: {pair_counts}')

    char_counts = {}
    for pair, count in pair_counts.items():
        char_counts[pair[0]] = int(count) if pair[0] not in char_counts else char_counts[pair[0]]+int(count)

    # Need to account for final character in the template string
    char_counts[template[-1]] += 1
    logging.debug(f'char_counts: {char_counts}')
    
    return max(char_counts.values()) - min(char_counts.values())

def part_one(input_file_name):
    '''
    Apply 10 steps of pair insertion rules and subtract the quantity of the least common element 
    from the quantity of the most common element
    '''
    return apply_steps(input_file_name, 10)

def part_two(input_file_name):
    '''Same as part_one, except 40 steps'''
    return apply_steps(input_file_name, 40)

def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return
    print(f'Part One: {part_one(args[1])}')
    print(f'Part Two: {part_two(args[1])}')

if __name__ == '__main__':
    main(sys.argv)
