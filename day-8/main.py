# https://adventofcode.com/2021/day/8

import sys

def parse_file(file_name):
    with open(file_name) as f:
        lines = [line.split('|') for line in f.readlines()]
        return [(components[0].strip().split(' '), components[1].strip().split(' ')) for components in lines]

def count_unique_digits(outputs):
	return len([segment for output in outputs for segment in output if is_known_digit(segment)])

def is_known_digit(segments):
    return True if len(segments) in [2,3,4,7] else False

def calculate_value(note, match_criteria):
	coded_outputs = set(''.join(sorted(output)) for output in note[0])
	coded_digits = [''.join(sorted(digit)) for digit in note[1]]
	solution = find_coded_digits(coded_outputs, match_criteria)
	decoded_values = [solution[code] for code in coded_digits]
	return int(''.join([str(value) for value in decoded_values]))

def find_coded_digits(outputs, match_criteria):
	solution = {}
	digits = {}
	remaining = set(outputs)
	for digit, length, subset, superset in match_criteria:
		segments = next(
			segments for segments in remaining
			if matches(segments, length, subset, superset, digits))
		solution[segments] = digit
		digits[digit] = segments
		remaining.remove(segments)
	return solution

def matches(segments, length, subset, superset, digits):
	if len(segments) != length:
		return False
	if subset is not None:
		return set(segments).issuperset(digits[subset])
	if superset is not None:
		return set(segments).issubset(digits[superset])
	return True

def main(args):
    if len(args) != 2:
        print('Need to provide file input')
        return

    notes = parse_file(args[1])
    outputs = [note[1] for note in notes]
    unique_digits = count_unique_digits(outputs)
    print(f"Part 1: {unique_digits}")

    # Array of (digit, length, index_of_subset, index_of_superset)
    match_criteria = [
        (1, 2, None, None),
        (7, 3, None, None),
        (4, 4, None, None), 
        (8, 7, None, None),
        (9, 6, 4, None),
        (0, 6, 7, None),
        (6, 6, None, None),
        (3, 5, 7, None),
        (5, 5, None, 6),
        (2, 5, None, None)
    ]

    total = sum(calculate_value(note, match_criteria) for note in notes)
    print(f"Part 2: {total}")

if __name__ == '__main__':
    main(sys.argv)
