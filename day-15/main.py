# https://adventofcode.com/2021/day/15

import sys
import logging
import networkx as nx
from dataclasses import dataclass, field
from typing import Any
from queue import PriorityQueue
from itertools import product

SAMPLE_FILE = './sample_input.txt'

def test_part_one():
    assert part_one(SAMPLE_FILE) == 40

def test_part_one_b():
    assert part_one('./sample_input_b.txt') == 8

def test_part_two():
    assert part_two(SAMPLE_FILE) == 315

def parse_input_file(input_file_name):
    with open(input_file_name) as f:
        return [[int(level) for level in list(line.strip())] for line in f.readlines()]

def create_graph(risk_level_map):
    dim = (len(risk_level_map[0]), len(risk_level_map))
    graph = nx.DiGraph()
    for x,y in product(range(dim[0]), range(dim[1])):
        # note that x,y is flipped when accessing row,col
        weight = risk_level_map[y][x]
        # note that we can only travel up,left,down,right
        if x - 1 > -1:
            graph.add_edge((x-1,y), (x,y), weight=weight)
        if x + 1 < dim[0]:
            graph.add_edge((x+1,y), (x,y), weight=weight)
        if y - 1 > -1:
            graph.add_edge((x,y-1), (x,y), weight=weight)
        if y + 1 < dim[1]:
            graph.add_edge((x,y+1), (x,y), weight=weight)
    return graph

@dataclass(order=True)
class LeastCostNode:
    cost: int
    path_to: Any=field(compare=False)

def least_cost_search(graph, source, target):
    node = LeastCostNode(0, [source])
    queue = PriorityQueue() 
    queue.put(node)

    # Note that starting position's risk is not counted since it isn't entered
    discovered = {node.path_to[-1]: node.cost}

    while queue.qsize() > 0:
        node = queue.get()
        node_state = node.path_to[-1]
        
        if node_state == target:
            return node
       
        for child_state, child_attr in graph[node_state].items():
            child_cost = node.cost + child_attr['weight']
            child_node = LeastCostNode(child_cost, [*node.path_to, child_state])
            if child_state not in discovered or child_node.cost < discovered[child_state]:
                discovered[child_state] = child_node.cost
                queue.put(child_node)
    return LeastCostNode(-1, [])


def part_one(input_file_name):
    '''What is the lowest total risk of any path from the top left to the bottom right?'''
    risk_level_map = parse_input_file(input_file_name)

    graph = create_graph(risk_level_map)

    target = (len(risk_level_map[0])-1, len(risk_level_map)-1)
    least_cost_node = least_cost_search(graph, (0,0), target)

    logging.debug(f'part_one: least_cost_node.path_to: {least_cost_node.path_to}')
    return least_cost_node.cost

def expand(risk_level_map):
    '''
    The entire cave is actually five times larger in both dimensions than you thought; 
    the area you originally scanned is just one tile in a 5x5 tile area that forms the full map. 
    Your original map tile repeats to the right and downward; 
    each time the tile repeats to the right or downward, 
    all of its risk levels are 1 higher than the tile immediately up or left of it. 
    However, risk levels above 9 wrap back around to 1.
    '''

    expanded_map = []
    tile_rows = len(risk_level_map)
    tile_cols = len(risk_level_map[0])
    map_rows = tile_rows * 5
    map_cols = tile_cols * 5
    # +i is down, +j is right
    for i in range(map_rows):
        expanded_map.append([])
    for i,j in product(range(map_rows), range(map_cols)):
        expanded_map[i].append(0)
    for i,j in product(range(tile_rows), range(tile_cols)):
        expanded_map[i][j] = risk_level_map[i][j]
    
    for i,j in product(range(map_rows), range(map_cols - tile_cols)):
        offset_i = i + tile_rows
        offset_j = j + tile_cols

        risk_level = expanded_map[i][j] + 1 if expanded_map[i][j] < 9 else 1

        expanded_map[i][offset_j] = risk_level

        if offset_i < map_rows:
            expanded_map[offset_i][j] = risk_level
    
    return expanded_map

def part_two(input_file_name):
    '''Same as part_one but expand the risk_level_map five times larger and apply rules from problem'''
    risk_level_map = expand(parse_input_file(input_file_name))
    graph = create_graph(risk_level_map)

    target = (len(risk_level_map[0])-1, len(risk_level_map)-1)
    least_cost_node = least_cost_search(graph, (0,0), target)

    logging.debug(f'part_two: least_cost_node.path_to: {least_cost_node.path_to}')
    return least_cost_node.cost
    
def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return
    print(f'Part One: {part_one(args[1])}')

    print(f'Part Two: {part_two(args[1])}')

if __name__ == '__main__':
    main(sys.argv)
