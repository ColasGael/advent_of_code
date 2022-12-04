#!/usr/bin/env python

from argparse import ArgumentParser
from datetime import datetime
import importlib
import os
import sys
import time


INPUT_PATH = os.path.join("{year}", "input", "day{day}.txt")
SOLUTION_PATH = os.path.join("{year}", "solution", "day{day}.txt")
SOLVING_MODULE = "{year}.solver.day{day}"


def load_input(input_path):
    with open(input_path, "r") as input_file:  # pylint: disable=unspecified-encoding
        input_lines = input_file.read().splitlines()
    return input_lines


def solve_puzzle(year, day_number, input_lines, *additional_args, always_print=False):
    solving_module = importlib.import_module(
        SOLVING_MODULE.format(year=year, day=day_number)
    )
    tic = time.time()
    part1_answer, part2_answer = solving_module.main(input_lines, *additional_args)
    toc = time.time()
    if always_print:
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


def check_answer(day_number, part_number, answer, solution=None, always_print=False):
    if (solution is not None) and (answer is not None):
        try:
            solution = type(answer)(solution)
        except ValueError:
            pass
    debug_msg = "Day {} Part {}: expected = {} ; answered = {}".format(
        day_number, part_number, repr(solution), repr(answer)
    )
    try:
        assert answer == solution, debug_msg
        if always_print:
            print(debug_msg)
    except AssertionError as err:
        print(err)
        return False
    return True


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
    parser.add_argument(
        "-p",
        "--always_print",
        action="store_true",
        help="Always print the expected solutions VS the actual answers .",
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

    result = True
    for day in args.days:
        try:
            input_lines = load_input(INPUT_PATH.format(year=args.year, day=day))
        except FileNotFoundError:
            print("Not solved day {}".format(day))
            continue

        part1_answer, part2_answer = solve_puzzle(
            args.year,
            day,
            input_lines,
            *args.additional_params,
            always_print=args.always_print
        )
        part1_solution, part2_solution = load_solution(
            SOLUTION_PATH.format(year=args.year, day=day)
        )
        for i, (answer, solution) in enumerate(
            ((part1_answer, part1_solution), (part2_answer, part2_solution))
        ):
            result = result and check_answer(
                day, i, answer, solution, always_print=args.always_print
            )

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
