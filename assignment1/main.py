"""
Input description

1. Number of x values
2. Number of slack values
3. Z expression in the form of coefficients (separated by a space) for every variable
For example, if we have 2 x variables, 4 slack variables, and z = 5x1 4x2, then the input should be
5 4 0 0 0 0 
4. Number of constraints (excluding the constraint that every coefficient is non-negative)
5. Coefficients of every constraint on a separte line
For example, if we have 2 x variables, 4 slack variables, 2 constraints 6x1 + 4x2 + s1 = 24, and x1 + x2 + s2 = 6, the input should be
6 4 1 0 0 0 24
1 2 0 1 0 0 6
"""