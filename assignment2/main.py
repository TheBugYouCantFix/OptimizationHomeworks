import numpy as np

# The number of coefficients of C
coeffNumOfC = int(input())
# A vector of coefficients of objective function - C
C = []
data = input().split()
for i in range(coeffNumOfC):
    C.append(float(data[i]))
C = np.array(C, float)

# The number of constraints of A
constraintsNumOfA = int(input())
# A matrix of coefficients of constraint function - A
A = []
for i in range(constraintsNumOfA):
    row = []
    data = input().split()
    for j in range(coeffNumOfC):
        row.append(float(data[j]))
    A.append(row)
A = np.array(A, float)

x = []
data = input().split()
for i in range(coeffNumOfC):
    x.append(float(data[i]))
x = np.array(x, float)


ones = np.ones(coeffNumOfC, float)

b = []
data = input().split()
for i in range(constraintsNumOfA):
    b.append(float(data[i]))
b = np.array(b, float)

epsilon = float(input())

alpha = 0.5
alpha2 = 0.9

for i in b:
    if i <= 0:
        print("The problem does not have solution!")
        exit(0)

X = x.copy()

while True:
    y = X.copy()
    D = np.diag(X)
    I = np.eye(coeffNumOfC)
    A1 = np.dot(A, D)
    for j in range(coeffNumOfC):
        numOfnegative = 0
        for i in range(constraintsNumOfA):
            if A1[i][j] < 0:
                numOfnegative += 1
        if numOfnegative == constraintsNumOfA:
            print("The method is not applicable!")
            exit(0)

    C1 = np.dot(D, C)
    f = np.dot(A1, np.linalg.matrix_transpose(A1))
    fi = np.linalg.inv(f)
    f = np.dot(fi, A1)
    f = np.dot(np.linalg.matrix_transpose(A1), f)
    P = np.subtract(I, f)
    c_p = np.dot(P, C1)
    nu = np.absolute(np.min(c_p))
    x1 = np.add(ones, (alpha/nu)*c_p)
    X = np.dot(D, x1)
    if np.linalg.norm(np.subtract(X, y), ord = 2) < epsilon:
        print(X)
        res = 0
        for i in range(coeffNumOfC):
            res += C[i]*X[i]
        print(res)
        break


while True:
    y = X.copy()
    D = np.diag(X)
    I = np.eye(coeffNumOfC)
    A1 = np.dot(A, D)
    for j in range(coeffNumOfC):
        numOfnegative = 0
        for i in range(constraintsNumOfA):
            if A1[i][j] < 0:
                numOfnegative += 1
        if numOfnegative == constraintsNumOfA:
            print("The method is not applicable!")
            exit(0)

    C1 = np.dot(D, C)
    f = np.dot(A1, np.linalg.matrix_transpose(A1))
    fi = np.linalg.inv(f)
    f = np.dot(fi, A1)
    f = np.dot(np.linalg.matrix_transpose(A1), f)
    P = np.subtract(I, f)
    c_p = np.dot(P, C1)
    nu = np.absolute(np.min(c_p))
    x1 = np.add(ones, (alpha2/nu)*c_p)
    X = np.dot(D, x1)
    if np.linalg.norm(np.subtract(X, y), ord = 2) < epsilon:
        print(X)
        res = 0
        for i in range(coeffNumOfC):
            res += C[i]*X[i]
        print(res)
        break
