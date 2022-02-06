'''This problem is a bit different.

Instead of solving it:
- algorithmically
- for all possible MONAD programs
I solved it:
- analytically
- for the specific MONAD program given as input


I will explain my reasoning:


1. Re-writing the MONAD program in pseudo-code.

The MONAD program is composed of 14 blocks following the same structure.
1 block for each digit of a model number.

A block structure is as follows:
1     inp w
2     mul x 0
3     add x z
4     mod x 26
5     div z DIV_Z
6     add x ADD_X
7     eql x w
8     eql x 0
9     mul y 0
10    add y 25
11    mul y x
12    add y 1
13    mul z y
14    mul y 0
15    add y w
16    add y ADD_Y
17    mul y x
18    add z y

The blocks are identical except for the parameters: DIV_Z (with values in: 1 ; 26) ; ADD_X ; ADD_Y.

We can first identify that the values of the variables: w ; x ; y from the previous block have no
influence on the next block.
Since they are resetted in the next block at the respective lines:
- w: 1
- x: 2
- y: 9

By analyzing the operations that a block is running, we can re-write it as a short function:
With inputs:
- w : the current digit of the model number (i-th digit for the i-th block)
- z : the output of the previous block (0 for the first block)
With parameters (read from the input MONAD program):
- do_div : (DIV_Z == 26)
- add_x : ADD_X
- add_y : ADD_Y

This equivalent function is given below in Python:

    def block(w, z, do_div, add_x, add_y):
        condition = (z % 26 + add_x == w)
        if do_div:
            z = z // 26
        if condition:
            z = z
        else:
            z = 26 * z + w + add_y


2. Understanding the impact of a single block.

We can distinguish two types of blocks:

    a. 7 blocks which satisfy: do_div == False (DIV_Z == 1)

For all these blocks, we can remark that they satisfy:
    add_x >= 10
And for any number z:
    z % 26 >= 0
In summary:
    z % 26 + add_x >= 10
Because each input digit w is between: 1 - 9
    z % 26 + add_x >= 10 > w
The following condition can never be met:
    z % 26 + add_x == w
In the end, all these blocks are simply applying the operation
    z <- 26 * z + w + add_y
With:
    0 <= add_y < 16
So:
    0 < w + add_y < 26


    b. 7 blocks which satisfy: do_div == True (DIV_Z == 26)

These blocks apply one of the following two operations, based on the value of the condition:
    z % 26 + add_x == w
- if true:
    z <- z // 26
- if false:
    z <- 26 * (z // 26) + w + add_y


3. Identifying the constraints on valid model numbers.

For a model number to be valid, the final block needs to return:
    z == 0

Let's take a closer at how each block type impacts the value of z.
If we write z in a 26-basis:

a. A block of this type increases the index of the first non-zero bits by 1.

b. The effect of this block depends on the value of the condition:
- if true: it decreases the index of the first non-zero bits by 1.
- if false: it does not change the index of the first non-zero bits by 1.

Since:
- the initial value of z is 0: index of the first non-zero bits is -1.
- to have a valid model number, the final value of z must be 0.
- there are the same number of a. and b. blocks.
The b. blocks need to compensate exactly for the a. blocks.
Which means that all the a. blocks' conditions must be satisfied.

For such a valid model number, let's re-write:
- the operations performed by each block: what is the updated value of z?
- for b. blocks: the satisfied conditions.

0.  i. : z = 0
1.  a. : z = (w1 + 6)
2.  a. : z = 26 * (w1 + 6) + (w2 + 7)
3.  a. : z = 26 ^ 2 * (w1 + 6) + 26 * (w2 + 7) + (w3 + 10)
4.  a. : z = 26 ^ 3 * (w1 + 6) + 26 ^ 2 (w2 + 7) + 26 * (w3 + 10) + (w4 + 2)
5.  b. : z = 26 ^ 2 * (w1 + 6) + 26 * (w2 + 7) + (w3 + 10)
Satisfied condition: -5 + w4 = w5
6.  a. : z = 26 ^ 3 * (w1 + 6) + 26 ^ 2 (w2 + 7) + 26 * (w3 + 10) + (w6 + 8)
7.  a. : z = 26 ^ 4 * (w1 + 6) + 26 ^ 3 * (w2 + 7) + 26 ^ 2 * (w3 + 10) + 26 * (w6 + 8) + (w7 + 1)
8.  b. : z = 26 ^ 3 * (w1 + 6) + 26 ^ 2 * (w2 + 7) + 26 * (w3 + 10) + (w6 + 8)
Satisfied condition: -4 + w7 = w8
9.  a. : z = 26 ^ 4 * (w1 + 6) + 26 ^ 3 * (w2 + 7) + 26 ^ 2 * (w3 + 10) + 26 * (w6 + 8) + (w9 + 5)
10. b. : z = 26 ^ 3 * (w1 + 6) + 26 ^ 2 * (w2 + 7) + 26 * (w3 + 10) + (w6 + 8)
Satisfied condition: 2 + w9 = w10
11. b. : z = 26 ^ 2 * (w1 + 6) + 26 * (w2 + 7) + (w3 + 10)
Satisfied condition: 8 + w6 = w11
12. b. : z = 26 * (w1 + 6) + (w2 + 7)
Satisfied condition: 5 + w3 = w12
13. b. : z = (w1 + 6)
Satisfied condition: -2 + w2 = w13
14. b. : z = 0
Satisfied condition: 6 + w1 = w14

The system of conditions on the model number digits is:
     6 + w1 = w14
    -2 + w2 = w13
     5 + w3 = w12
    -5 + w4 = w5
     8 + w6 = w11
    -4 + w7 = w8
     2 + w9 = w10


4. Finding the extremum valid model numbers.

Remark:
- Each digit w of a model number is between 1 - 9.
- From the constraints: increasing wX increases the associated wY.

a. Find the largest valid model number
We take each digit as close to 9 as possible while satisfying the conditions.

If we re-write the conditions as:
    w14 = w1  + 6
    w2  = w13 + 2
    w12 = w3  + 5
    w4  = w5  + 5
    w11 = w6  + 8
    w7  = w8  + 4
    w10 = w9  + 2

To get the largest valid model number:
- we take the left-hand sides equal to 9
- and compute the right-hand sides of the constraints.


b. Find the smallest valid model number
We take each digit as close to 1 as possible while satisfying the conditions.

If we re-write the conditions as:
    w1  = w14 - 6
    w13 = w2  - 2
    w3  = w12 - 5
    w5  = w4  - 5
    w6  = w11 - 8
    w8  = w7  - 4
    w9  = w10 - 2

To get the largest valid model number:
- we take the left-hand sides equal to 1
- and compute the right-hand sides of the constraints.
- and compute the right-hand sides of the constraints.


Remark: You cand find below the function to apply any NOMAD program on a model number.
This was used to check that the model numbers found above where valid.
'''

def main(input_lines):
    part1_answer = 39494195799979
    part2_answer = 13161151139617
    return part1_answer, part2_answer


def is_valid_model_num(program_lines, model_num):
    # Convert to a list representation easier to process
    model_num_l = [int(c) for c in str(model_num)]
    # A valid model number should not contain 0
    if 0 in model_num_l:
        return -1

    variables = {
        "w": 0,
        "x": 0,
        "y": 0,
        "z": 0,
    }
    input_idx = 0
    for program_line in program_lines:
        instructions = program_line.strip().split(" ")
        operation = instructions[0]
        variable_name = instructions[1]
        if operation == "inp":
            variables[variable_name] = model_num[input_idx]
            input_idx += 1
            continue
        variable_value = variables[variable_name]
        other_variable_name = instructions[2]
        if other_variable_name in variables:
            other_variable_value = variables[other_variable_name]
        else:
            other_variable_value = int(other_variable_name)
        if operation == "add":
            new_variable_value = variable_value + other_variable_value
        elif operation == "mul":
            new_variable_value = variable_value * other_variable_value
        elif operation == "div":
            new_variable_value = int(variable_value / other_variable_value)
        elif operation == "mod":
            new_variable_value = variable_value % other_variable_value
        elif operation == "eql":
            new_variable_value = variable_value == other_variable_value
        variables[variable_name] = new_variable_value

    return variables["z"]
