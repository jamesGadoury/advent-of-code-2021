import sys

# note I'm keeping this file, but the cpp file basically replaces it because it is faster
# and keep up w/ performance reqs
class LanternFish:
    def __init__(self, timer):
        self.timer = int(timer)
    
    def __repr__(self):
        return f'{self.timer}'

class LanternFishSim:
    def __init__(self, fish_timers: list):
        self.fishes = [LanternFish(timer) for timer in fish_timers]
        self.days = 0

    @staticmethod
    def init_from_file(file_name):
        with open(file_name) as f:
            # file input should only be one line
            return LanternFishSim(f.readline().split(','))

    def simulate_day(self):
        fishes_to_add = 0
        for fish in self.fishes:
            if fish.timer == 0:
                fish.timer = 6
                fishes_to_add += 1
            else:
                fish.timer -= 1
        for i in range(fishes_to_add):
            self.fishes.append(LanternFish(8))
        self.days += 1
        return self.fishes

    def simulate_days(self, days):
        for _ in range(days):
            self.simulate_day()
        return self.fishes

def part_one(file_name):
    sim = LanternFishSim.init_from_file(file_name)
    # print(f'Initial State: {sim.state(0)}')

    # for day in range(1,18):
    #     print(f'After {day} day{"s" if day>1 else ""}: {sim.state(day)}')
    print(f'Part One: Number of fish after 80 days: {len(sim.simulate_days(80))}')

def part_two(file_name):
    sim = LanternFishSim.init_from_file(file_name)
    print(f'Part Two: Number of fish after 256 days: {len(sim.simulate_days(256))}')
                

def main(args):
    if len(args) != 2:
        print('need file input provided as cli arg')
        return
    
    part_one(args[1])
    part_two(args[1])

if __name__ == '__main__':
    main(sys.argv)