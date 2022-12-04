#!/usr/bin/env python

from argparse import ArgumentParser
from datetime import datetime
import importlib
import os
import time


INPUT_PATH = os.path.join("{year}", "input", "day{day}.txt")
SOLUTION_PATH = os.path.join("{year}", "solution", "day{day}.txt")
SOLVING_MODULE = "{year}.solver.day{day}"


def load_input(input_path):
    with open(input_path, "r") as input_file:  # pylint: disable=unspecified-encoding
        input_lines = input_file.read().splitlines()
    return input_lines


def solve_puzzle(year, day_number, input_lines, *additional_args):
    solving_module = importlib.import_module(
        SOLVING_MODULE.format(year=year, day=day_number)
    )
    tic = time.time()
    part1_answer, part2_answer = solving_module.main(input_lines, *additional_args)
    toc = time.time()
    print("Day {} was solved in {:.1f} ms !".format(day_number, (toc - tic) * 1000))
    return part1_answer, part2_answer


def load_solution(solution_path):
    part1_solution, part2_solution = None, None
    if os.path.isfile(solution_path):
        # pylint: disable=unspecified-encoding
        with open(solution_path, "r") as input_file:
            input_lines = input_file.read().splitlines()
        # pylint: enable=unspecified-encoding
        part1_solution, part2_solution = input_lines[0], input_lines[1]
    return part1_solution, part2_solution


def check_answers(
    day_number, part1_answer, part2_answer, part1_solution=None, part2_solution=None
):
    print(
        "Day {} Part 1: expected = {} ; answered = {}".format(
            day_number, part1_solution, part1_answer
        )
    )
    print(
        "Day {} Part 2: expected = {} ; answered = {}".format(
            day_number, part2_solution, part2_answer
        )
    )


def get_args():
    parser = ArgumentParser("Solver for the Advent of Code puzzles.")
    parser.add_argument(
        "-y",
        "--year",
        type=int,
        help="Year of the puzzle(s) to solve (default: current year).",
    )
    parser.add_argument(
        "-d",
        "--days",
        type=int,
        nargs="+",
        help="Day(s) of the puzzle(s) to solve (default: all).",
    )
    parser.add_argument(
        "-a",
        "--additional_params",
        type=str,
        nargs="+",
        help="Additional parameters to pass to the solver (when a single day is being solved).",
    )

    args = parser.parse_args()
    if args.year is None:
        args.year = datetime.now().year
    if args.days is None:
        args.days = range(1, 26)
    if args.additional_params is None:
        args.additional_params = []

    return args


def main():
    args = get_args()

    for day in args.days:
        input_lines = load_input(INPUT_PATH.format(year=args.year, day=day))
        part1_answer, part2_answer = solve_puzzle(
            args.year, day, input_lines, *args.additional_params
        )
        part1_solution, part2_solution = load_solution(
            SOLUTION_PATH.format(year=args.year, day=day)
        )
        check_answers(day, part1_answer, part2_answer, part1_solution, part2_solution)


if __name__ == "__main__":
    main()
