import numpy as np


def main(input_lines, target_expense=2020):
    expenses = [int(line) for line in input_lines]

    # Complexity: N*log(N)
    expenses.sort()

    part1_answer = np.prod(is_sum_of_2(target_expense, expenses))
    part2_answer = np.prod(is_sum_of_3(target_expense, expenses))
    return part1_answer, part2_answer


def is_sum_of_2(target_expense, expenses):
    # Complexity: N^2
    # for i, this_expense in enumerate(expenses):
    #     for other_expense in expenses[i+1:]:
    #         if (this_expense + other_expense == target_expense):
    #             return (this_expense * other_expense)

    # Assumption: 'expenses' sorted in increasing order
    # Complexity: N
    i, j = 0, len(expenses) - 1
    while (i != j):
        sum_expense = expenses[i] + expenses[j]
        if (sum_expense == target_expense):
            return (expenses[i], expenses[j])
        elif (sum_expense > target_expense):
            j -= 1
        else:
            i += 1


def is_sum_of_3(target_expense, expenses):
    # Complexity: N^3
    # for i, this_expense in enumerate(expenses):
    #     for j, other_expense in enumerate(expenses[i+1:]):
    #         for another_expense in expenses[i+1+j+1:]:
    #             if (this_expense + other_expense + another_expense == target_expense):
    #                 return (this_expense * other_expense * another_expense)

    # Assumption: 'expenses' sorted in increasing order
    # Complexity: N^2
    for i, expense in enumerate(expenses):
        revised_target_expense = target_expense - expense
        result = is_sum_of_2(revised_target_expense, expenses[i+1:])
        if result:
            return (result[0], result[1], expense)
