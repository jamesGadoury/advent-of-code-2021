# https://adventofcode.com/2021/day/13

import sys
import numpy as np
import itertools

class FoldInstruction:
    def __init__(self, instruction_line):
        '''Fold along axis at positions formed at line'''
        self.axis, self.line = instruction_line.strip().split(' ')[2].split('=')
        self.line = int(self.line)

    def __repr__(self):
        return f'(FoldInstruction: axis: {self.axis}, line: {self.line})'

def parse_file(input_file_name):
    with open(input_file_name) as f:
        lines = [line for line in f.readlines()]
        dots_lines = [line.strip().split(',') for line in lines[0:lines.index('\n')]]
        dot_locations = [(int(dots_line[0]),int(dots_line[1])) for dots_line in dots_lines]
        fold_instructions = [FoldInstruction(line) for line in lines[lines.index('\n')+1:]]
        return (dot_locations, fold_instructions)

class TransparentPaper:
    def __init__(self, dot_locations):
        x_locations = [loc[0] for loc in dot_locations]
        y_locations = [loc[1] for loc in dot_locations]
        # kinda confusing but '.' is used in example problem to show empty and '#' is used to show dot
        self.state = np.full((max(y_locations)+1, max(x_locations)+1), '.').astype(np.unicode_)
        for location in dot_locations:
            # '#' is used as a dot for some reason in the example 
            self.state[location[1]][location[0]] = '#'

    def __repr__(self):
        return f'(TransparentPaper state:\n {self.state})'


    def fold_up(self, fold_instruction):
        first_half = self.state[0:fold_instruction.line, :]
        second_half = np.flip(self.state[fold_instruction.line+1:, :], 0)
        if first_half.shape[0] > second_half.shape[0]:
            self.state = first_half
            offset = first_half.shape[0] - second_half.shape[0]
            for i,j in itertools.product(range(second_half.shape[0]), range(second_half.shape[1])):
                if second_half[i][j] == '#':
                    self.state[i+offset][j] = '#'
        elif second_half.shape[0] > first_half.shape[0]:
            self.state = second_half
            offset = second_half.shape[0] - first_half.shape[0]
            for i,j in itertools.product(range(first_half.shape[0]), range(first_half.shape[1])):
                if first_half[i][j] == '#':
                    self.state[i+offset][j] = '#'
        else:
            # equal shapes
            self.state = first_half
            for i,j in itertools.product(range(self.state.shape[0]), range(self.state.shape[1])):
                if second_half[i][j] == '#':
                    self.state[i][j] = '#'

    def fold_left(self, fold_instruction):
        first_half = self.state[:, 0:fold_instruction.line]
        second_half = np.flip(self.state[:, fold_instruction.line+1:], 1)
        if first_half.shape[1] > second_half.shape[1]:
            self.state = first_half
            offset = first_half.shape[1] - second_half.shape[1]
            for i,j in itertools.product(range(second_half.shape[0]), range(second_half.shape[1])):
                if second_half[i][j] == '#':
                    self.state[i+offset][j] = '#'
        elif second_half.shape[1] > first_half.shape[1]:
            self.state = second_half
            offset = second_half.shape[1] - first_half.shape[1]
            for i,j in itertools.product(range(first_half.shape[0]), range(first_half.shape[1])):
                if first_half[i][j] == '#':
                    self.state[i+offset][j] = '#'
        else:
            # equal shapes
            self.state = first_half
            for i,j in itertools.product(range(self.state.shape[0]), range(self.state.shape[1])):
                if second_half[i][j] == '#':
                    self.state[i][j] = '#'

    def fold(self, fold_instruction):
        print(f'Folding for instruction: {fold_instruction}')
        if fold_instruction.axis == 'x':
            return self.fold_left(fold_instruction)
        if fold_instruction.axis == 'y':
            return self.fold_up(fold_instruction)

    def visible_dots(self):
        return (self.state == '#').sum()

def test_part_one():
    assert part_one('./sample_input.txt') == 17

def part_one(input_file_name):
    '''How many dots are visible after completing the first fold instruction on your transparent paper?'''
    dot_locations, fold_instructions = parse_file(input_file_name)
    paper = TransparentPaper(dot_locations)
    paper.fold(fold_instructions[0])
    return paper.visible_dots()

def part_two(input_file_name):
    '''display paper after all folds'''
    dot_locations, fold_instructions = parse_file(input_file_name)
    paper = TransparentPaper(dot_locations)
    for instruction in fold_instructions:
        paper.fold(instruction)

    for line in paper.state:
        print(''.join(line))


def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return

    print(f'Part One: Number of visible dots after one fold: {part_one(args[1])}')
    print('Part Two:')
    part_two(args[1])

if __name__ == '__main__':
    main(sys.argv)
