#!/usr/bin/env python

import importlib
import os
import sys
import time


INPUT_PATH = "input/day{}.txt"
SOLUTION_PATH = "solution/day{}.txt"
SOLVING_MODULE = "solver.day{}"


def load_input(input_path):
    with open(input_path, 'r') as input_file:
        input_lines = input_file.readlines()
    return input_lines


def solve_puzzle(day_number, input_lines, *additional_args):
    solving_module = importlib.import_module(SOLVING_MODULE.format(day_number))
    tic = time.time()
    part1_answer, part2_answer = solving_module.main(input_lines, *additional_args)
    toc = time.time()
    print("Day {} was solved in {:.1f} ms !".format(day_number, (toc-tic)*1000))
    return part1_answer, part2_answer


def load_solution(solution_path):
    part1_solution, part2_solution = None, None
    if os.path.isfile(solution_path):
        with open(solution_path, 'r') as input_file:
            input_lines = input_file.readlines()
        part1_solution, part2_solution = input_lines[0].strip(), input_lines[1].strip()
    return part1_solution, part2_solution


def check_answers(day_number, part1_answer, part2_answer, part1_solution=None, part2_solution=None):
    print("Day {} Part 1: expected = {} ; answered = {}".format(day_number, part1_solution, part1_answer))
    print("Day {} Part 2: expected = {} ; answered = {}".format(day_number, part2_solution, part2_answer))


def main():
    today = int(sys.argv[1])
    if today == 0:
        day_numbers = range(1, 25)
    else:
        day_numbers = [today]

    for day_number in day_numbers:
        input_lines = load_input(INPUT_PATH.format(day_number))
        part1_answer, part2_answer = solve_puzzle(day_number, input_lines, *sys.argv[2:])
        part1_solution, part2_solution = load_solution(SOLUTION_PATH.format(day_number))
        check_answers(day_number, part1_answer, part2_answer, part1_solution, part2_solution)


if __name__ == '__main__':
    main()

