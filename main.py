#!/usr/bin/env python3

from argparse import ArgumentParser
from datetime import datetime
import importlib
import os
import re
import sys
import time

import requests


# For local runs
INPUT_PATH = os.path.join("{year}", "input", "day{day}.txt")
SOLUTION_PATH = os.path.join("{year}", "solution", "day{day}.txt")
# In CI
SOLUTION_URL = "https://adventofcode.com/{year}/day/{day}"
INPUT_URL = SOLUTION_URL + "/input"
SOLUTION_PATTERN = re.compile(r"Your puzzle answer was \<code\>([\w\-\_=,]*)\<\/code\>")

SOLVING_MODULE = "{year}.solver.day{day}"

# Special keyword to handle the unspecified part 2 of day 25's puzzle
UNSPECIFIED = "unspecified"


class NotSolvedException(RuntimeError):
    def __init__(self, year, day):
        super().__init__(f"Year {year}: day {day} has not been solved yet.")


def load_input(input_path):
    with open(input_path, "r") as input_file:  # pylint: disable=unspecified-encoding
        input_lines = input_file.read().splitlines()
    return input_lines


def load_solutions(solution_path):
    part1_solution, part2_solution = None, None
    if os.path.isfile(solution_path):
        # pylint: disable=unspecified-encoding
        with open(solution_path, "r") as input_file:
            input_lines = input_file.read().splitlines()
        # pylint: enable=unspecified-encoding
        part1_solution, part2_solution = input_lines[0], input_lines[1]
    return part1_solution, part2_solution


def load_server_input_and_solutions(year, day, session):
    with requests.Session() as sess:
        # Get the input
        input_url = INPUT_URL.format(year=year, day=day)
        res = sess.get(input_url, cookies={"session": session})
        content = res.content.decode("utf-8")
        if res.status_code != 200:
            raise RuntimeError(f"Failed to get input from: {input_url}\n{content}")
        input_lines = content.splitlines()
        if len(input_lines[-1]) == 0:
            input_lines.pop()

        # Get the solutions
        solution_url = SOLUTION_URL.format(year=year, day=day)
        res = sess.get(solution_url, cookies={"session": session})
        content = res.content.decode("utf-8")
        if res.status_code != 200:
            raise RuntimeError(
                f"Failed to get solutions from: {solution_url}\n{content}"
            )
        solutions = SOLUTION_PATTERN.findall(content)
        if len(solutions) == 0:
            raise NotSolvedException(year, day)
        if len(solutions) == 1:
            # Let it fail the day if part 2 should have been solved but isn't yet
            solutions.append(UNSPECIFIED)
        elif len(solutions) > 2:
            raise RuntimeError(
                f"Cannot identify solutions: too many candidates {solutions}"
            )

    return input_lines, solutions


def get_input_and_solutions(year, day, mode_ci, session):
    if not mode_ci:
        # Locally: when solving the puzzles
        # Read the input and solutions from local files
        try:
            # Get the input
            input_lines = load_input(INPUT_PATH.format(year=year, day=day))
            # Get the solutions
            solutions = load_solutions(SOLUTION_PATH.format(year=year, day=day))
        except FileNotFoundError as exc:
            raise NotSolvedException(year, day) from exc

    else:
        # In CI: when checking the answers
        # Get the input and solutions from the advent_of_code server
        input_lines, solutions = load_server_input_and_solutions(year, day, session)

    return input_lines, solutions


def solve_puzzle(year, day, input_lines, *additional_args, always_print=False):
    try:
        solving_module = importlib.import_module(
            SOLVING_MODULE.format(year=year, day=day)
        )
    except ModuleNotFoundError as exc:
        raise NotSolvedException(year, day) from exc

    tic = time.time()
    part1_answer, part2_answer = solving_module.main(input_lines, *additional_args)
    toc = time.time()
    if always_print:
        print("Day {} was solved in {:.1f} ms !".format(day, (toc - tic) * 1000))
    return part1_answer, part2_answer


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
        help="Always print the expected solutions VS the actual answers.",
    )
    parser.add_argument(
        "-c",
        "--mode_ci",
        action="store_true",
        help="Enable the CI mode which gets inputs and solutions from advent_of_code server. "
        "Instead of using local files.",
    )
    parser.add_argument(
        "-s",
        "--session",
        type=str,
        help="Your advent of code session cookie (must be provided when running with 'mode_ci'. "
        "(See: https://cookie-script.com/documentation/how-to-check-cookies-on-chrome-and-firefox)",
    )

    args = parser.parse_args()
    if args.year is None:
        args.year = datetime.now().year
    if args.days is None:
        args.days = range(1, 26)
    if args.additional_params is None:
        args.additional_params = []

    if args.mode_ci and args.session is None:
        raise RuntimeError(
            "The session cookie must be provided when running with 'mode_ci'"
        )

    return args


def main():
    args = get_args()

    result = True
    for day in args.days:
        try:
            input_lines, solutions = get_input_and_solutions(
                args.year,
                day,
                args.mode_ci,
                args.session,
            )
            part1_solution, part2_solution = solutions
            part1_answer, part2_answer = solve_puzzle(
                args.year,
                day,
                input_lines,
                *args.additional_params,
                always_print=args.always_print,
            )
        except NotSolvedException as exc:
            print(exc)
            continue

        for i, (answer, solution) in enumerate(
            ((part1_answer, part1_solution), (part2_answer, part2_solution)), start=1
        ):
            result = (
                check_answer(day, i, answer, solution, always_print=args.always_print)
                and result
            )

    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
