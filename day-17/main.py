# https://adventofcode.com/2021/day/17

import sys
import logging
from dataclasses import dataclass
from itertools import product

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
    v_x = probe_state.velocity.x - 1 if probe_state.velocity.x > 0 else probe_state.velocity.x + 1

    # Due to gravity, the probe's y velocity decreases by 1.
    v_y = probe_state.velocity.y - 1

    return ProbeState(position=Position(x=r_x, y=r_y), velocity=Velocity(x=v_x, y=v_y))

def init_probe_state(init_velocity: Velocity) -> ProbeState:
    return ProbeState(position=Position(x=0, y=0), velocity=init_velocity)


@dataclass
class SimulationState:
    probe_state: ProbeState
    target_area: TargetArea

    def has_probe_within_target_area(self):
        return self.probe_state.position.x >= self.target_area.x_range[0] and \
            self.probe_state.position.x <= self.target_area.x_range[1] and \
            self.probe_state.position.y >= self.target_area.y_range[0] and \
            self.probe_state.position.y <= self.target_area.y_range[1]

class Simulation:
    def __init__(self, init_state: SimulationState, steps: list = []):
        self.init_state = init_state
        self.steps = steps

    def add_step(self, step: SimulationState):
        self.steps.append(step)

    def last_state(self):
        return self.steps[-1] if len(self.steps) != 0 else self.init_state

    def initialized(self):
        return len(self.steps) != 0

def simulate_trajectory(init_velocity: Velocity, target_area: TargetArea, step_count: int = 100) -> Simulation:
    logging.debug(f'simulate_trajectory called with init_velocity={init_velocity}, target_area={target_area}, step_count={step_count}')
    probe_state = init_probe_state(init_velocity)
    logging.debug(f'in simulate_trajectory, initial probe state: {probe_state}')
    sim = Simulation(init_state=SimulationState(probe_state=probe_state, target_area=target_area))

    # todo -> need to find a better condition for evaluation whether or not to keep stepping sim
    for i in range(step_count):
        probe_state = step_probe_state(sim.last_state().probe_state)
        logging.debug(f'in simulate_trajectory, probe_state: {probe_state} for sim step: {i}')
        new_sim_state = SimulationState(probe_state=probe_state, target_area=target_area)
        sim.add_step(new_sim_state)
        if new_sim_state.has_probe_within_target_area():
            logging.debug(f'in simulate trajectory, found init velocity that hits target area at step: {i} with state: {new_sim_state}')
            return sim


    logging.debug(f'in simulate trajectory, did not find init velocity that hits target area after {step_count} steps')
    return sim


def find_sim_in_target_area(target_area: TargetArea):
    for x_vel, y_vel in product(range(1,10), range(1,10)):
        sim = simulate_trajectory(init_velocity=Velocity(x_vel, y_vel), target_area=target_area)
        if sim.last_state().has_probe_within_target_area():
            return sim

def part_one(input_file_name):
    '''
    Find the initial velocity that causes the probe to reach the highest y position and still eventually be 
    within the target area after any step. What is the highest y position it reaches on this trajectory?
    '''
    target_area = parse_file(input_file_name)
    logging.debug(f'in part_one, target_area={target_area}')

    sim = find_sim_in_target_area(target_area)

    return max([step.position.y for step in sim.steps]) if sim else -1


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
