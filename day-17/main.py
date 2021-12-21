# https://adventofcode.com/2021/day/17

import sys
import logging
from dataclasses import dataclass
from itertools import product
from multiprocessing import Pool
from enum import Enum

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


@dataclass
class Position:
    x : int
    y : int

@dataclass
class Velocity:
    x : int
    y : int

@dataclass
class ProbeState:
    position : Position
    velocity : Velocity


def step_probe_state(probe_state : ProbeState) -> ProbeState :
    # The probe's x position increases by its x velocity.
    r_x = probe_state.position.x + probe_state.velocity.x

    # The probe's y position increases by its y velocity.
    r_y = probe_state.position.y + probe_state.velocity.y

    # Due to drag, the probe's x velocity changes by 1 toward the value 0; 
    # that is, it decreases by 1 if it is greater than 0, 
    # increases by 1 if it is less than 0, or does not change if it is already 0.
    # v_x = probe_state.velocity.x - 1 if probe_state.velocity.x > 0 else (probe_state.velocity.x + 1 if probe_state.velocity.x < 0 else 0)
    v_x = max(0, probe_state.velocity.x - 1)

    # Due to gravity, the probe's y velocity decreases by 1.
    v_y = probe_state.velocity.y - 1

    logging.debug(f'in step_probe_state, r_x:{r_x}, r_y:{r_y}, v_x:{v_x}, v_y:{v_y}')

    return ProbeState(position=Position(x=r_x, y=r_y), velocity=Velocity(x=v_x, y=v_y))

def init_probe_state(init_velocity: Velocity) -> ProbeState:
    return ProbeState(position=Position(x=0, y=0), velocity=init_velocity)

class SimulationFailure(Enum):
    NONE = 0
    STOPPED_MOVING_AND_FELL_SHORT = 1
    MOVED_PAST_TARGET_AREA_X_RANGE = 2
    FELL_BELOW_TARGET_AREA_Y_RANGE = 3

@dataclass
class SimulationState:
    probe_state: ProbeState
    target_area: TargetArea

    def has_probe_within_target_area(self):
        return self.target_area.x_range[0] <= self.probe_state.position.x <= self.target_area.x_range[1] and \
               self.target_area.y_range[0] <= self.probe_state.position.y <= self.target_area.y_range[1]

    def failure_to_hit_target_area(self):
        if self.probe_state.velocity.x == 0 and self.probe_state.position.x < self.target_area.x_range[0]:
            # stopped moving +x (to the right) and will not reach x_range of target_area
            return SimulationFailure.STOPPED_MOVING_AND_FELL_SHORT
        
        if self.probe_state.position.x > self.target_area.x_range[1]:
            # is to the right of the target's x range and can only travel right
            return SimulationFailure.MOVED_PAST_TARGET_AREA_X_RANGE

        if self.probe_state.velocity.y < 0 and self.probe_state.position.y < self.target_area.y_range[1]:
            # is falling below the target area and will continue to fall
            return SimulationFailure.FELL_BELOW_TARGET_AREA_Y_RANGE

        return SimulationFailure.NONE

    def possible_to_hit_target(self):
        return self.failure_to_hit_target_area() == SimulationFailure.NONE

    def dist_from_target_area(self):
        '''Rough calc of distance from center of target area'''
        center_x = (self.target_area.x_range[0] + self.target_area.x_range[1]) / 2
        center_y = (self.target_area.y_range[0] + self.target_area.y_range[1]) / 2
        return ((self.probe_state.position.x - center_x)**2 + (self.probe_state.position.y - center_y)**2) ** 1/2

class Simulation:
    def __init__(self, init_state: SimulationState):
        logging.debug(f'Simulation initialized with init_state={init_state}')
        self.init_state = init_state
        self.steps = [] 
        self.failure = None

    def add_step(self, step: SimulationState):
        self.steps.append(step)

    def last_state(self):
        return self.steps[-1] if len(self.steps) != 0 else self.init_state

    def initialized(self):
        return len(self.steps) != 0

    def simulate_trajectory(self):
        logging.debug(f'simulate_trajectory called with init_state={self.init_state}')

        for step in range(2*abs(self.init_state.target_area.y_range[0])):
            probe_state = step_probe_state(self.last_state().probe_state)
            new_sim_state = SimulationState(probe_state=probe_state, target_area=self.init_state.target_area)
            self.add_step(new_sim_state)
            logging.debug(f'in simulate_trajectory, probe_state: {probe_state} for sim step: {len(self.steps)}')
            if new_sim_state.has_probe_within_target_area():
                logging.info(f'in simulate trajectory, init_velocity={self.init_state.probe_state.velocity} hits target area at step: {len(self.steps)} with state: {new_sim_state}')
                return


def generate_sims(target_area):
    sims = []
    for x_vel, y_vel in product(range(target_area.x_range[1]+1), range(target_area.y_range[0], -target_area.y_range[0])):
        init_velocity = Velocity(x_vel, y_vel)
        init_sim_state = SimulationState(init_probe_state(init_velocity), target_area)
        sims.append(Simulation(init_sim_state))

    return sims

def run_sim(sim: Simulation):
    sim.simulate_trajectory()
    return sim

def find_sims_in_target_area(target_area: TargetArea):
    executed_sims = None
    sims = generate_sims(target_area)
    with Pool(processes=15) as pool:
        executed_sims = pool.map(run_sim, sims)

    return [sim for sim in executed_sims if sim.last_state().has_probe_within_target_area()] 

def part_one(input_file_name):
    '''
    Find the initial velocity that causes the probe to reach the highest y position and still eventually be 
    within the target area after any step. What is the highest y position it reaches on this trajectory?
    '''
    target_area = parse_file(input_file_name)
    logging.info(f'in part_one, target_area={target_area}')

    sims = find_sims_in_target_area(target_area)
    highest_y_of_each_sim = [max([step.probe_state.position.y for step in sim.steps]) for sim in sims]
    return max(highest_y_of_each_sim)

def part_two(input_file_name):
    '''
    Find number of initial velocities that can hit target area 
    '''
    target_area = parse_file(input_file_name)
    logging.info(f'in part_one, target_area={target_area}')

    sims = find_sims_in_target_area(target_area)
    return len(sims)

def test_part_one():
    assert part_one('./sample_input.txt') == 45


def test_part_two():
    assert part_two('./sample_input.txt') == 112
        

def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return

    logging.basicConfig(filename='debug_main.log', level=logging.DEBUG)

    # print(f'part_one: {part_one(args[1])}')
    print(f'part_two: {part_two(args[1])}')

if __name__ == '__main__':
    main(sys.argv)
