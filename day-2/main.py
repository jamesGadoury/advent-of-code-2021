# https://adventofcode.com/2021/day/2
import sys

def process_input_file(input_file):
    with open(input_file) as f:
        return f.readlines() 

def process_commands(commands):
    horizontal_position = 0
    depth = 0
    for command in commands:
        direction, value = command.split(' ')
        value = int(value)
        if direction == 'forward':
            horizontal_position += value
        elif direction == 'down':
            depth += value
        elif direction == 'up':
            depth -= value
        else:
            print(f'error parsing command: {command}')
            return
    print (f'After processing commands, final horizontal_position*depth = {horizontal_position*depth}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Need argument for input!')
    else:
        process_commands(process_input_file(sys.argv[1]))