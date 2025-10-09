#1:
def printMatrix(A, starting_index, rows, columns):
    start_row, start_col = starting_index

    for i in range(start_row, start_row + rows):
        for j in range(start_col, start_col + columns):
            print(A[i][j], end=' ')
        print()  


A = [
    [1, 2, 3, 4, 5, 6],
    [7, 8, 9, 10, 11, 12],
    [13, 14, 15, 16, 17, 18],
    [19, 20, 21, 22, 23, 24]
]

printMatrix(A, (2, 3), 2, 3)
print("---------------------------------------------------------------------")

#2:
def MatAdd(A, B):
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        print("Error: Matrices must have the same dimensions!")
        return None

    result = []
    for i in range(len(A)):
        row = []
        for j in range(len(A[0])):
            row.append(A[i][j] + B[i][j])  # element-wise addition
        result.append(row)
    
    return result


A = [
    [1, 2, 3],
    [4, 5, 6]
]

B = [
    [7, 9],
    [1, 2, 3]
]

C = MatAdd(A, B)

if C is not None:
    for row in C:
        print(row)
print("---------------------------------------------------------------------")

#3:
def MatAddPartial(A, B, start, size):
    x, y = start
    result = []

    for i in range(size):
        row = []
        for j in range(size):
            sum_val = A[x + i][y + j] + B[x + i][y + j]
            row.append(sum_val)
        result.append(row)

    return result


A = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20]
]

B = [
    [5, 4, 3, 2, 1],
    [10, 9, 8, 7, 6],
    [15, 14, 13, 12, 11],
    [20, 19, 18, 17, 16]
]

C = MatAddPartial(A, B, (2, 3), 2)

for row in C:
    print(row)

print("---------------------------------------------------------------------")
#4:
def MatMul(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        print("Error: Number of columns in A must equal number of rows in B")
        return None

    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]

    return C


A = [
    [1, 2, 3],
    [4, 5, 6]
]

B = [
    [7, 8],
    [9, 10],
    [11, 12]
]

C = MatMul(A, B)

for row in C:
    print(row)

print("---------------------------------------------------------------------")
#5:

def MatAdd(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def MatSub(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C


def MatMulRecursive(A, B):
    n = len(A)

    if n == 1:
        return [[A[0][0] * B[0][0]]]

    mid = n // 2

    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    C11 = MatAdd(MatMulRecursive(A11, B11), MatMulRecursive(A12, B21))
    C12 = MatAdd(MatMulRecursive(A11, B12), MatMulRecursive(A12, B22))
    C21 = MatAdd(MatMulRecursive(A21, B11), MatMulRecursive(A22, B21))
    C22 = MatAdd(MatMulRecursive(A21, B12), MatMulRecursive(A22, B22))

    new_matrix = []
    for i in range(mid):
        new_matrix.append(C11[i] + C12[i])
    for i in range(mid):
        new_matrix.append(C21[i] + C22[i])

    return new_matrix


A = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

B = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

C = MatMulRecursive(A, B)
for row in C:
    print(row)

print("---------------------------------------------------------------------")
#6:
def MatAdd(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] + B[i][j]
    return C

def MatSub(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = A[i][j] - B[i][j]
    return C


def MatMulStrassen(A, B):
    n = len(A)

    if n == 1:
        return [[A[0][0] * B[0][0]]]

    mid = n // 2

    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    M1 = MatMulStrassen(MatAdd(A11, A22), MatAdd(B11, B22))
    M2 = MatMulStrassen(MatAdd(A21, A22), B11)
    M3 = MatMulStrassen(A11, MatSub(B12, B22))
    M4 = MatMulStrassen(A22, MatSub(B21, B11))
    M5 = MatMulStrassen(MatAdd(A11, A12), B22)
    M6 = MatMulStrassen(MatSub(A21, A11), MatAdd(B11, B12))
    M7 = MatMulStrassen(MatSub(A12, A22), MatAdd(B21, B22))

    C11 = MatAdd(MatSub(MatAdd(M1, M4), M5), M7)
    C12 = MatAdd(M3, M5)
    C21 = MatAdd(M2, M4)
    C22 = MatAdd(MatSub(MatAdd(M1, M3), M2), M6)

    new_matrix = []
    for i in range(mid):
        new_matrix.append(C11[i] + C12[i])
    for i in range(mid):
        new_matrix.append(C21[i] + C22[i])

    return new_matrix


A = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

B = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
]

C = MatMulStrassen(A, B)

for row in C:
    print(row)

print("---------------------------------------------------------------------")  