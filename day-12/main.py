# https://adventofcode.com/2021/day/12

import sys
import networkx as nx

def test_part_one_a():
    assert part_one('./sample_input_a.txt') == 10

def test_part_two_b():
    assert part_one('./sample_input_b.txt') == 19

def test_part_two_a():
    assert part_two('./sample_input_a.txt') == 36

def test_part_two_b():
    assert part_two('./sample_input_b.txt') == 103

def graph_from_file(file_name):
    G = nx.Graph()
    with open(file_name) as f:
        lines = [line.strip() for line in f.readlines()]
        edges = [line.split('-') for line in lines]
        for edge in edges:
            G.add_edge(edge[0], edge[1])
    return G

class Node:
    def __init__(self, path_to):
        self.path_to = path_to

    def state(self):
        return self.path_to[-1]

def expand(graph, node):
    return [Node([*node.path_to, edge[1]]) for edge in graph.edges(node.state())]

def search(graph, rule):
    node = Node(['start'])
    frontier = [node]
    paths = []
    while len(frontier):
        node = frontier.pop()
        if node.state() == 'end':
            paths.append(node.path_to)
            continue
        for child in expand(graph, node):
            if rule(graph, child):
                frontier.append(child)
    return paths

def no_small_cave_repeats(graph, node):
    small_caves = [node for node in graph.nodes() if node.islower()]
    return not any([node.path_to.count(cave) > 1 for cave in small_caves])

def part_one(file_name):
    graph = graph_from_file(file_name)
    paths = search(graph, no_small_cave_repeats)
    return len(paths)

def part_two_rule(graph, node):
    small_caves = [node for node in graph.nodes() if node.islower()]
    cave_visited_twice = False
    for cave in small_caves:
        cave_visit_count = node.path_to.count(cave)
        if cave_visit_count > 2:
            return False
        if cave_visit_count == 2:
            if cave_visited_twice:
                return False
            cave_visited_twice = True

    start_once = node.path_to.count('start') == 1 
    end_count = node.path_to.count('end')
    end_only_once_and_final = end_count == 0 or (end_count == 1 and node.state() == 'end')
    return start_once and end_only_once_and_final
    

def part_two(file_name):
    graph = graph_from_file(file_name)
    paths = search(graph, part_two_rule)
    return len(paths)

def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return

    print(f'Part One: The number of unique paths that visit small caves at most once is: {part_one(args[1])}')
    print(f'Part Two: The number of paths that satisfy part two\'s rules are: {part_two(args[1])}')

if __name__ == '__main__':
    main(sys.argv)
