# https://adventofcode.com/2021/day/4

from dataclasses import dataclass
import numpy as np
import sys

@dataclass
class BingoSquare:
    number: int
    marked: bool = False

class BingoBoard:
    def __init__(self, board_numbers):
        self.squares = np.array([[BingoSquare(int(number)) for number in board_numbers[i]] for i in range(len(board_numbers))])
        self.winning_number = None

    def __str__(self):
        representation = '\n'
        for row in self.squares:
            representation += f'{"".join([f"{square.number}:X".rjust(7, " ") if square.marked else f"{square.number}: ".rjust(7, " ") for square in row])}'
            representation += '\n'
        return representation

    def mark_if_match(self, drawn_number):
        for row in self.squares:
            for square in row:
                if square.number == drawn_number:
                    square.marked = True
                    if self.won():
                        self.winning_number = drawn_number

    def won(self):
        '''Returns True if board has won'''
        for row in self.squares:
            if all([square.marked for square in row]):
                return True

        for col in self.squares.T:
            if all([square.marked for square in col]):
                return True

        return False

    def score(self):
        '''Returns the score of this board (0 if board has not won yet)'''
        if not self.won():
            return 0

        # there is a dev error if this has not been set
        assert self.winning_number != None

        # Note that this isn't traditional Bingo, it is a variant that is defined
        # by the above link, which is why there is this weird scoring system

        sum_of_unmarked = sum(np.apply_along_axis(lambda row: sum([square.number if not square.marked else 0 for square in row]), 1, self.squares))

        return sum_of_unmarked * self.winning_number
        

class BingoGame:
    def __init__(self, draws, boards):
        self.draws = draws
        self.playing_boards = [BingoBoard(board) for board in boards]
        # completed means won
        self.completed_boards = []

    def play(self):
        print('Playing Bingo')
        for draw in self.draws:
            print(f'Number {draw} was drawn!')
            for i, board in enumerate(self.playing_boards):
                board.mark_if_match(draw)

                if board.won():
                    self.completed_boards.append(board)
                    print(f'There is a winner for the drawn number: {draw}! Winner {len(self.completed_boards)} board: {board}') 
            self.playing_boards = list(filter(lambda board: not board.won(), self.playing_boards))

    @staticmethod
    def create_from_file_input(file_name):
        with open(file_name) as f:
            lines = [line.strip() for line in f.readlines()]
            draws = [int(draw) for draw in lines[0].split(',')]
            boards = [[line.split() for line in [lines[i+j] for j in range(5)]] for i in range(2, len(lines), 6)]
            return BingoGame(draws, boards)


def main(args):
    if len(args) != 2:
        print('Need file to use as input provided as arg')
        return

    file_name = args[1]

    bingo = BingoGame.create_from_file_input(file_name)

    bingo.play()

    for i,completed_board in enumerate(bingo.completed_boards):
        print(f'Score of completed board {i+1}: {completed_board.score()}')

if __name__ == '__main__':
    main(sys.argv)