# https://adventofcode.com/2021/day/6

#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <array>

class LanternFishSim {
public:
    static inline const LanternFishSim init_from_file(const std::string& file_name) {
        std::ifstream file(file_name);
        std::string data = "";
        std::vector<int> fish_timers;
        while(getline(file, data,','))
        {
           fish_timers.push_back(stoi(data)); 
        }
        return LanternFishSim(fish_timers);
    }

    LanternFishSim(const std::vector<int>& fish_timers) {
        for (const auto& fish_timer : fish_timers) {
            fish_timer_counts[fish_timer]+=1;
        }
        display_counts();
    }

    void display_counts() {
        for (size_t i { 0 }; i < 9; ++i) {
            std::cout << "Count for " << i << " timer: " << fish_timer_counts[i] << std::endl;
        }
    }

    void simulate_day() {
        std::cout << "Simulating day " << days << std::endl;
        size_t breeding_fish = fish_timer_counts[0];
        fish_timer_counts[0] = fish_timer_counts[1];
        fish_timer_counts[1] = fish_timer_counts[2];
        fish_timer_counts[2] = fish_timer_counts[3];
        fish_timer_counts[3] = fish_timer_counts[4];
        fish_timer_counts[4] = fish_timer_counts[5];
        fish_timer_counts[5] = fish_timer_counts[6];
        fish_timer_counts[6] = breeding_fish + fish_timer_counts[7];
        fish_timer_counts[7] = fish_timer_counts[8];
        fish_timer_counts[8] = breeding_fish;
        days += 1;
    }

    void simulate_days(const size_t days) {
        for (size_t i { 0 }; i < days; ++i) {
            simulate_day();
        }
    }

    size_t fish_count() { 
        size_t fish_count { 0 };
        for (const auto& count : fish_timer_counts) {
            fish_count += count;
        }
        return fish_count;
    }

private:
    std::array<size_t, 9> fish_timer_counts {0, 0, 0, 0, 0, 0, 0, 0, 0};
    size_t days { 0 };
};

void part_one(const std::string& file_name) {
    LanternFishSim sim { LanternFishSim::init_from_file(file_name) };
    sim.simulate_days(80);
    std::cout << "Part One: Number of fish after 80 days: " << sim.fish_count() << std::endl;
}

void part_two(const std::string& file_name) {
    LanternFishSim sim { LanternFishSim::init_from_file(file_name) };
    sim.simulate_days(256);
    std::cout << "Part One: Number of fish after 256 days: " << sim.fish_count() << std::endl;
}

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cout << "Need to provide file input" << std::endl;
        return 0;
    }
    part_one(argv[1]);
    part_two(argv[1]);
}