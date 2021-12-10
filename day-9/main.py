# https://adventofcode.com/2021/day/9

import numpy as np
import sys

def find_low_points(heat_map):
    low_points = []
    for i in range(len(heat_map)):
        for j in range(len(heat_map[0])):
            # Check above element if it exists
            if i - 1 > -1 and heat_map[i][j] >= heat_map[i-1][j]:
                continue
            # Check below element if it exists
            if i + 1 < len(heat_map) and heat_map[i][j] >= heat_map[i+1][j]:
                continue
            # Check left element if it exists
            if j - 1 > -1 and heat_map[i][j] >= heat_map[i][j-1]:
                continue
            # Check right element if it exists
            if j + 1 < len(heat_map[0]) and heat_map[i][j] >= heat_map[i][j+1]:
                continue
            low_points.append((i,j))
    return low_points

def assess_risk_levels(heat_map):
    risk_levels = []
    low_points = find_low_points(heat_map)
    for i,j in low_points:
        risk_levels.append(heat_map[i][j]+1)
    return risk_levels

def generate_heat_map(file):
    with open(file) as f:
        return np.array([[int(point) for point in line.strip()] for line in f.readlines()])

def populate_basin(heat_map, point, last_point, basin):
    i,j = point
    if last_point:
        i_last,j_last = last_point
        if heat_map[i][j] == 9 or heat_map[i][j] <= heat_map[i_last][j_last]:
            return basin

    basin.add(point)
    basin_values = []
    if i-1 >= 0:
        basin_values = set([*basin_values, *populate_basin(heat_map, (i-1,j), point, basin)])
    if i+1 <= len(heat_map)-1:
        basin_values = set([*basin_values, *populate_basin(heat_map, (i+1,j), point, basin)])
    if j-1 >= 0:
        basin_values = set([*basin_values, *populate_basin(heat_map, (i,j-1), point, basin)])
    if j+1 <= len(heat_map[0])-1:
        basin_values = set([*basin_values, *populate_basin(heat_map, (i,j+1), point, basin)])
    return basin_values

def find_basins(heat_map):
    basins = []
    low_points = find_low_points(heat_map)

    for low_point in low_points:
        basins.append(populate_basin(heat_map, low_point, None, set()))

    return basins

def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return

    heat_map = generate_heat_map(args[1])
    risk_levels = assess_risk_levels(heat_map)
    print(f'Part One: Sum of risk levels of low points: {sum(risk_levels)}')

    basins = find_basins(heat_map)
    # get basin sizes and sort greatest to lowest
    basin_sizes = sorted([len(basin) for basin in basins], reverse=True)
    print(f'Part Two: Three largest basin sizes multiplied together: {basin_sizes[0]*basin_sizes[1]*basin_sizes[2]}')

if __name__ == '__main__':
    main(sys.argv)
