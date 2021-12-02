import sys

def part_one():
    file_name = sys.argv[1]

    with open(file_name) as f:
        lines = f.readlines()
        prev_measurement = None
        increased_depth_count = 0
        for line in lines:
            current_measurement = int(line)
            if prev_measurement and prev_measurement < current_measurement:
                increased_depth_count += 1
            prev_measurement = current_measurement

    print(f'Number of depth increases using basic calculation: {increased_depth_count}')

def part_two():
    '''Use sliding window calculation to help remove noise from input data'''
    file_name = sys.argv[1]

    with open(file_name) as f:
        measurements = [int(line) for line in f.readlines()]
        prev_measurement_window = None
        increased_depth_count = 0
        for i in range(len(measurements)):
            if (i + 2 == len(measurements)):
                break

            current_measurement_window = measurements[i] + measurements[i+1] + measurements[i+2]
            if prev_measurement_window and prev_measurement_window < current_measurement_window:
                increased_depth_count += 1

            prev_measurement_window = current_measurement_window

    print(f'Number of depth increases using sliding window calculation: {increased_depth_count}')


if __name__ == '__main__':
    part_one()
    part_two()
