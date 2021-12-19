// https://adventofcode.com/2021/day/14
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <fstream>
#include <algorithm>
#include <chrono>
#include <tbb/flow_graph.h>

// LOOK HERE: Compile with below:
// intelCompile main.cpp -ltbb --std=c++17 -O3 -o run
// where intelCompile=~/intel/oneapi/compiler/2022.0.1/linux/bin/icpx
// NOTE THAT THIS IS A FAILED ATTEMPT AT A SOLUTION, AND THAT THE PYTHON
// SCRIPT IS THE CORRECT SOLUTION
// I ONLY KEPT THIS BECAUSE IT IS AN INTERESTING REFERENCE FOR USING ONE TBB FLOW GRAPHS WITH RECURSIVE FUNCTIONS
struct UserInput
{
    std::string template_str;
    std::unordered_map<std::string, std::string> pair_insertion_rules;
};

void display_user_input(const UserInput &user_input) {
    std::cout << user_input.template_str << std::endl;

    for (const auto &[src_pair, dest_pair] : user_input.pair_insertion_rules) {
        std::cout << src_pair << " " << dest_pair << std::endl;
    }
}

UserInput parse_file(const std::string &input_file_name) {
    std::ifstream input { input_file_name, std::ios::binary };
    if (!input.is_open()) {
        std::cout << "Failed to parse input file" << std::endl;
        return {};
    }

    std::string line;
    // first line is the template_str
    std::getline(input, line);
    const std::string template_str { line };

    // next line is empty
    std::getline(input, line);

    // rest of lines are the pair insertion rules
    std::unordered_map<std::string, std::string> pair_insertion_rules;
    while (std::getline(input, line)) {
        pair_insertion_rules[line.substr(0,2)] = line.substr(0,1) + line.substr(line.size()-1);
    }
    return { template_str, pair_insertion_rules };
}

struct RecursiveInsertInput {
    const std::string pair;
    const std::unordered_map<std::string,std::string> pair_insertion_rules;
    const int step_count;
    const int depth;
    RecursiveInsertInput(const std::string &pair, 
                         const std::unordered_map<std::string, std::string> pair_insertion_rules,
                         const int step_count,
                         const int depth=1)
        : pair { pair }, pair_insertion_rules { pair_insertion_rules }, step_count { step_count }, depth { depth }
    {}
};

struct RecursiveInsertNodeInput {
    std::shared_ptr<RecursiveInsertInput> recursive_insert_input;
    std::shared_ptr<std::string> section;
    RecursiveInsertNodeInput() = default;
    RecursiveInsertNodeInput(const std::shared_ptr<RecursiveInsertInput> &insert_input, 
                             const std::shared_ptr<std::string> &section)
        : recursive_insert_input { insert_input }, section { section }
    {}
};

std::string recurse_insert(const RecursiveInsertInput& input) {
    
    if (input.pair_insertion_rules.find(input.pair) == input.pair_insertion_rules.end()) {
        std::cout << "No insertion rules for pair " << input.pair << "!" << std::endl;
        return "";
    }

    const std::string pair_a { input.pair_insertion_rules.at(input.pair) };
    const std::string pair_b { pair_a.substr(pair_a.size()-1) + input.pair.substr(input.pair.size()-1) };

    // std::cout << "recurse_insert: depth: " << depth << " pair_a: " << pair_a << " pair_b: " << pair_b << std::endl;

    if (input.depth == input.step_count) {
        return pair_a;
    }

    tbb::flow::graph graph;

    tbb::flow::function_node<RecursiveInsertNodeInput> recurse_insert_node {
        graph, 2, [](RecursiveInsertNodeInput input){
            *input.section = recurse_insert(*input.recursive_insert_input);
        }
    };

    std::shared_ptr<RecursiveInsertInput> recursive_insert_input_a { 
        std::make_shared<RecursiveInsertInput>(pair_a, input.pair_insertion_rules, input.step_count, input.depth+1)
    };

    std::shared_ptr<std::string> section_a { std::make_shared<std::string>() };
    recurse_insert_node.try_put( {recursive_insert_input_a, section_a} );

    std::shared_ptr<RecursiveInsertInput> recursive_insert_input_b { 
        std::make_shared<RecursiveInsertInput>(pair_b, input.pair_insertion_rules, input.step_count, input.depth+1)
    };

    std::shared_ptr<std::string> section_b { std::make_shared<std::string>() };
    recurse_insert_node.try_put( {recursive_insert_input_b, section_b} );

    graph.wait_for_all();

    return section_a->append(*section_b);
}


std::string apply_insertion_rules(const std::string &template_str, 
                                  const std::unordered_map<std::string,std::string> &pair_insertion_rules, 
                                  const int step_count) {
    std::string new_template = "";

    // NNCB -> NN, NC, CB
    std::vector<std::shared_ptr<std::string>> template_sections { template_str.size() -1 };
    for (int i { 0 }; i < template_sections.size(); ++i) {
        template_sections[i] = std::make_shared<std::string>();
    }

    tbb::flow::graph graph;

    tbb::flow::function_node<RecursiveInsertNodeInput> recurse_insert_node {
        graph, tbb::flow::unlimited, [](RecursiveInsertNodeInput input){
            *input.section = recurse_insert(*input.recursive_insert_input);
        }
    };

    for (int i { 0 }; i < template_str.size()-1; ++i) {
        std::cout << "apply_insertion_rules: calling recurse_insert with pair: " << template_str.substr(i,2) << std::endl;
        std::shared_ptr<RecursiveInsertInput> recursive_insert_input { 
            std::make_shared<RecursiveInsertInput>(template_str.substr(i,2), pair_insertion_rules, step_count)
        };
        recurse_insert_node.try_put( {recursive_insert_input, template_sections[i]} );
    }

    graph.wait_for_all();

    for (const auto& section : template_sections) {
        new_template = new_template.append(*section);
    }

    new_template = new_template.append(template_str.substr(template_str.size()-1));

    return new_template;
}

std::vector<int> char_counts(const std::string &template_str) {
    std::unordered_set<char> unique_chars;
    for (const auto character : template_str) {
        unique_chars.insert(character);
    }

    std::vector<int> char_counts;
    for (const auto character : unique_chars) {
        char_counts.push_back(std::count(template_str.begin(), template_str.end(), character));
    }
    return char_counts;
}

int apply_steps(const std::string &input_file_name, const int step_count) {
    const auto user_input { parse_file(input_file_name) };

    auto start { std::chrono::high_resolution_clock::now() };
    const auto template_str { 
        apply_insertion_rules(user_input.template_str, user_input.pair_insertion_rules, step_count) 
    };
    auto stop { std::chrono::high_resolution_clock::now() };
    auto duration { std::chrono::duration_cast<std::chrono::milliseconds>(stop-start).count() };
    std::cout << "execution time for apply_insertion_rules: " << duration << " ms" << std::endl;

    if (step_count < 5) {
        std::cout << "template str after rules are applied: " << template_str << std::endl;
    }

    const auto counts { char_counts(template_str) };

    auto max_count { counts[0] };
    auto min_count { counts[0] };

    for (const auto& count : counts) {
        max_count = std::max(max_count, count);
        min_count = std::min(min_count, count);
    }
    return max_count - min_count;
}

int part_one(const std::string &input_file_name) {
    return apply_steps(input_file_name, 10);
}

int part_two(const std::string &input_file_name) {
    return apply_steps(input_file_name, 40);
}

int main(int argc, char **argv) {
    if (argc < 2) {
        std::cout << "Need to provide file input!" << std::endl;
        return 0;
    }

    apply_steps(argv[1], 4);

    int part_one_result { part_one(argv[1]) };

    std::cout << "Part One: " << part_one_result << std::endl;

    int result_20 { apply_steps(argv[1], 20) };
    std::cout << "20 steps: " << result_20 << std::endl;

    // int part_two_result { part_two(argv[1]) };
    // when run with ./sample_input.txt = 2188189693529
    // std::cout << "Part Two: " << part_two_result << std::endl;
}