# https://adventofcode.com/2021/day/5

import sys
from enum import Enum
import numpy as np
import matplotlib.pyplot as plt

class Point:
    def __init__(self, elements:list):
        self.x = int(elements[0])
        self.y = int(elements[1])

    def __repr__(self):
        return f'Point: x: {self.x}, y: {self.y}'

class LineType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    DIAGONAL = 2

class LineSegment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f'LineSegment: p1: {self.p1}, p2: {self.p2}, type: {self.type()}'
    
    def type(self):
        return LineType.HORIZONTAL if self.p1.y == self.p2.y else (LineType.VERTICAL if self.p1.x == self.p2.x else LineType.DIAGONAL)

    @staticmethod
    def create_from_file_line(line):
        line_elements = line.strip().split(' ')
        return LineSegment(p1=Point(line_elements[0].split(',')), p2=Point(line_elements[2].split(',')))

def parse_line_segments(file_name):
    with open(file_name) as f:
        return [LineSegment.create_from_file_line(line) for line in f.readlines()]

def init_board(line_segments):
    max_x = max_y = 0
    for segment in line_segments:
        max_x = segment.p1.x if segment.p1.x > max_x else max_x
        max_x = segment.p2.x if segment.p2.x > max_x else max_x
        max_y = segment.p1.y if segment.p1.y > max_y else max_y
        max_y = segment.p2.y if segment.p2.y > max_y else max_y

    return np.zeros((max_y+1, max_x+1))

def populate_board_with_segments(board, line_segments, ignore=[]):
    populated_board = np.copy(board)
    for segment in line_segments:
        if segment.type() in ignore:
            continue

        if segment.p1.x == segment.p2.x and segment.p1.y == segment.p2.y:
            print('oh jeez')

        if segment.type() == LineType.HORIZONTAL:
            start_x = segment.p1.x if segment.p1.x < segment.p2.x else segment.p2.x
            end_x = segment.p1.x if segment.p1.x > segment.p2.x else segment.p2.x
            for x in range(start_x, end_x+1):
                populated_board[x][segment.p1.y]+=1
            continue

        if segment.type() == LineType.VERTICAL:
            start_y = segment.p1.y if segment.p1.y < segment.p2.y else segment.p2.y
            end_y = segment.p1.y if segment.p1.y > segment.p2.y else segment.p2.y
            for y in range(start_y, end_y+1):
                populated_board[segment.p1.x][y]+=1
            continue

        if segment.type() == LineType.DIAGONAL:
            populated = False
            start_x = segment.p1.x if segment.p1.x < segment.p2.x else segment.p2.x
            end_x = segment.p1.x if segment.p1.x > segment.p2.x else segment.p2.x
            x_range = range(start_x, end_x+1)
            start_y = segment.p1.y if segment.p1.x == start_x else segment.p2.y
            end_y = segment.p1.y if segment.p1.x == end_x else segment.p2.y
            y_range = range(start_y, end_y+1 if start_y < end_y else end_y-1, 1 if start_y < end_y else -1)
            for x,y in zip(x_range, y_range):
                populated = True
                populated_board[x][y]+=1
            if not populated:
                print(segment)
            continue

        print('oh no this shouldn\'t have happened')
    
    return populated_board

def dangerous_points_count(board):
    # any point with 2 or more is where 2 or more lines of vents overlap, these are dangerous points
    return np.count_nonzero(board >= 2)

def main(args):
    if len(args) != 2:
        print('Need to provide input file.')
        return

    line_segments = parse_line_segments(args[1])

    # part one, only populate horizontal and vertical
    print('Part One: Get number of dangerous points where two or more line segments overlap (ignore diagonal)')
    board = populate_board_with_segments(init_board(line_segments), line_segments, ignore=[LineType.DIAGONAL])
    print(f'Dangerous point count: {dangerous_points_count(board)}')

    # part two, same as part one, but also consider diagonal
    print('Part Two: Same as above, but consider diagonal as well')
    board = populate_board_with_segments(init_board(line_segments), line_segments)
    print(f'Dangerous point count: {dangerous_points_count(board)}')

    plt.imshow(board, cmap='hot', interpolation='nearest')
    plt.show()

if __name__ == '__main__':
    main(sys.argv)