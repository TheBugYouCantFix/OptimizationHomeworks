"""
SIMPLEX METHOD ALGORITHM IMPLEMENTATION



Input description

1. Number of x values
2. Z expression in the form of coefficients (separated by a space) for every variable
For example, if we have 2 x variables, and z = 5x1 4x2, then the input should be
5 4 
3. Number of constraints (excluding the constraint that every coefficient is non-negative)
4. Coefficients of every constraint on a separte line (x values first, then the right hand side). 
For example, if the constraint is 6x1 + 4x2 <= 24, the input line should be
6 4 24

Input example 1
3
9 10 16
3
18 15 12 360
6 4 8 192
5 3 3 180

Input example 2
2
5 4
4
6 4 24
1 2 6
-1 1 1
0 1 2
"""
n_xs = int(input())
z = list(map(int, input().split()))

# 1, 2. Converting to the standard form and building the table
n_constraints = int(input())
z = list(map(lambda x: -x, z)) + [0 for _ in range(n_constraints + 1)] # slack values are 0, last value is right hand side (solution) which is initailly 0
# also make every coefficient of z negative as we transfer it to the left hand side
constraints = []
basic_vars = [-1 for _ in range(n_xs + n_constraints)]

for i in range(n_constraints):
    slacks = [0 for _ in range(n_constraints)]
    slacks[i] = 1
    c = list(map(int, input().split()))
    c = c[:-1] + slacks + [c[-1]] 
    constraints.append(c)

table = [z] + constraints
while any(map(lambda x: x < 0, table[0])):
    # 3, 4. Find the smallest positive ratio

    # Select the most negative term in the first row
    
    entering_var_index = table[0].index(min(table[0]))

    min_pos_ratio = 10**9
    leaving_var_index = 0

    for i in range(len(table)):
        if table[i][entering_var_index] == 0:
            continue

        ratio = table[i][-1] / table[i][entering_var_index]

        if ratio > 0 and ratio < min_pos_ratio:
            min_pos_ratio = ratio
            leaving_var_index = i

    # 5. dividing the key row by the key element
    key_element = table[leaving_var_index][entering_var_index]
    for i in range(len(table[leaving_var_index])):
        table[leaving_var_index][i] /= key_element

    # 6. Make the key column to zero by substracting key row from other rows
    for i in range(len(table)):
        if i == leaving_var_index:
            continue

        coefficient = -table[i][entering_var_index] / table[leaving_var_index][entering_var_index]
        for j in range(len(z)):
            table[i][j] += coefficient * table[leaving_var_index][j]

    # 7. Change the basic varibale of the key row with the name of key column
    basic_vars[entering_var_index] = leaving_var_index


print(f'z={table[0][-1]}', end='')
for i in range(n_xs):
    if basic_vars[i] != -1:
        print(f', x{i + 1}={table[basic_vars[i]][-1]}', end='')
