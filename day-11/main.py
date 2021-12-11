# https://adventofcode.com/2021/day/11

import sys
import numpy as np
import itertools

class Octopus:
    def __init__(self, energy_level, flashed=False):
        self.energy_level = energy_level
        self.flashed = flashed

    def __repr__(self):
        return f'Octopus: energy_level:{self.energy_level}, flashed:{self.flashed}'

    def __str__(self):
        return f'{self.energy_level}, {self.flashed}'

    def __add__(self, number):
        return Octopus(self.energy_level+1, self.flashed)

class OctoSim:
    def __init__(self, file_name):
        with open(file_name) as f:
            energy_levels = np.array([[int(level) for level in line.strip()] for line in f.readlines()])
            self.octi = np.apply_along_axis(lambda row: [Octopus(energy_level) for energy_level in row], 0, energy_levels)
        self.step_count = 0
        self.flash_count = 0
        # steps where all octi flash
        self.synchronized_steps = []

    def __str__(self):
        return f'{self.octi}'

    def rows(self):
        return len(self.octi)

    def cols(self):
        return len(self.octi[0])

    def can_flash_at(self, i, j):
        return not self.octi[i][j].flashed and self.octi[i][j].energy_level > 9

    def increment_and_apply_flash(self, i, j):
        self.octi[i][j].energy_level += 1
        if self.can_flash_at(i, j):
            self.apply_flash(i,j)

    def apply_flash(self, i, j):
        self.flash_count += 1
        self.octi[i][j].flashed = True
        if i - 1 >= 0:
            self.increment_and_apply_flash(i-1, j)
            if j - 1 >= 0:
                self.increment_and_apply_flash(i-1, j-1)
            if j + 1 < self.cols():
                self.increment_and_apply_flash(i-1, j+1)
        if j - 1 >= 0:
            self.increment_and_apply_flash(i, j-1)
        if j + 1 < self.cols():
            self.increment_and_apply_flash(i, j+1)
        if i + 1 < self.rows():
            self.increment_and_apply_flash(i+1, j)
            if j - 1 >= 0:
                self.increment_and_apply_flash(i+1, j-1)
            if j + 1 < self.cols():
                self.increment_and_apply_flash(i+1, j+1)

    def step(self):
        '''Step the simulation forward'''
        self.step_count += 1
        # First, the energy level of each octopus increases by 1.
        self.octi += 1

        # Then, any octopus with an energy level greater than 9 flashes. 
        # This increases the energy level of all adjacent octopuses by 1, including octopuses that are diagonally adjacent. 
        # If this causes an octopus to have an energy level greater than 9, it also flashes. 
        # This process continues as long as new octopuses keep having their energy level increased beyond 9. 
        # (An octopus can only flash at most once per step.)
        for i,j in itertools.product(range(self.rows()), range(self.cols())):
            if self.can_flash_at(i, j):
                self.apply_flash(i, j) 

        # Check if this is a 'synchronized step' where all octi flashed at once
        if np.all(np.apply_along_axis(lambda row: [octopus.flashed for octopus in row], 0, self.octi)):
            self.synchronized_steps.append(self.step_count)

        # Finally, any octopus that flashed during this step has its energy level set to 0, 
        # as it used all of its energy to flash.
        for i,j in itertools.product(range(self.rows()), range(self.cols())):
            if self.octi[i][j].flashed:
                self.octi[i][j].energy_level = 0
                self.octi[i][j].flashed = False

def test_part_one():
    assert part_one('./sample_input.txt') == 1656

def part_one(file_name):
    '''Given the starting energy levels of the dumbo octopuses in your cavern, simulate 100 steps. 
    Return total number of flashes after 100 steps
    '''
    sim = OctoSim(file_name)
    for _ in range(100):
        sim.step()
    return sim.flash_count

def test_part_two():
    assert part_two('./sample_input.txt') == 195

def part_two(file_name):
    '''What is the first step where all octopuses flash at once?'''
    sim = OctoSim(file_name)
    while len(sim.synchronized_steps) == 0:
        sim.step()
    return sim.synchronized_steps[0]

def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return
    print(f'Part One: Total number of flashes after 100 simulated steps: {part_one(args[1])}')
    print(f'Part Two: First step where all octopuses flash at once: {part_two(args[1])}')

if __name__ == '__main__':
    main(sys.argv)
