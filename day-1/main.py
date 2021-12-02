import sys

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

print(f'Number of depth increases: {increased_depth_count}')
