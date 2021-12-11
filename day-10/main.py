# https://adventofcode.com/2021/day/10

import sys

OPENING_CHARS = ['(', '[', '{', '<']
CLOSING_CHARS = [')', ']', '}', '>']
CLOSING_TO_OPENING_CHAR = {CLOSING_CHAR: OPENING_CHAR for OPENING_CHAR, CLOSING_CHAR in zip(OPENING_CHARS, CLOSING_CHARS)}
OPENING_TO_CLOSING_CHAR = {OPENING_CHAR: CLOSING_CHAR for OPENING_CHAR, CLOSING_CHAR in zip(OPENING_CHARS, CLOSING_CHARS)}

ILLEGAL_CHAR_SCORE = {')': 3, ']': 57, '}': 1197, '>': 25137}
INCOMPLETE_CHAR_SCORE = {')': 1, ']': 2, '}': 3, '>': 4}

class Line:
    def __init__(self, data):
        self.data = data
        self.corrupt = False
        self.incomplete = False
        self.score = None
        current_chunk = ''
        for char in data:
            if char in OPENING_CHARS:
                current_chunk += char
            elif char in CLOSING_CHARS:
                if not CLOSING_TO_OPENING_CHAR[char] == current_chunk[-1]:
                    self.corrupt = True
                    self.score = ILLEGAL_CHAR_SCORE[char]
                    break
                current_chunk = current_chunk[:-1]
            else:
                print('illegal char detected - oh no I should be an error but I\'m lazy')

        if not self.corrupt:
            self.incomplete = True
            total_score = 0
            for char in current_chunk[::-1]:
                total_score *= 5
                total_score += INCOMPLETE_CHAR_SCORE[OPENING_TO_CLOSING_CHAR[char]]
            self.score = total_score
        
    def __repr__(self):
        return f'( Line: data:{self.data}, corrupt:{self.corrupt}, score:{self.score} )'
    
def get_lines(file_name):
    with open(file_name) as f:
        return [Line(line.strip()) for line in f.readlines()]

def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return

    lines = get_lines(args[1])
    corrupted_scores = [line.score for line in lines if line.corrupt]
    print(f'Part One: Corrupted line scores: {sum(corrupted_scores)}')

    incomplete_scores = [line.score for line in lines if line.incomplete]
    # Now perform weird task where we are asked so sort the list and take middle score
    incomplete_scores.sort()
    assert len(incomplete_scores) % 2 != 0
    print(f'Part Two: Incomplete line scores: {incomplete_scores[int(len(incomplete_scores)/2)]}')

if __name__ == '__main__':
    main(sys.argv)
