'''
Checked problem:
Cost matrix:
8 6 10 9
9 12 13 7
14 9 16 5

Supply vector:
20 30 25

Demand vector:
15 25 20 15

Whole input (for copying):
8 6 10 9
9 12 13 7
14 9 16 5
20 30 25
15 25 20 15
'''
def north_west_corner(cost_matrix, source_supply, destination_demand):
    result_matrix = [[0 for _ in range(4)] for _ in range(3)]
    result_cost_matrix = [[0 for _ in range(4)] for _ in range(3)]
    while source_supply.count(0) < len(source_supply) and destination_demand.count(0) < len(destination_demand):
        key_cell_i = 0
        key_cell_j = 0
        for i in range(len(cost_matrix)):
            break_flag = 0
            for j in range(len(cost_matrix[i])):
                if cost_matrix[i][j] != -1:
                    key_cell_i = i
                    key_cell_j = j
                    break_flag = 1
                    break
            if break_flag == 1:
                break
        if source_supply[key_cell_i] > destination_demand[key_cell_j]:
            result_cost_matrix[key_cell_i][key_cell_j] = destination_demand[key_cell_j] * cost_matrix[key_cell_i][key_cell_j]
            result_matrix[key_cell_i][key_cell_j] = destination_demand[key_cell_j]
            for supply in cost_matrix:
                supply[key_cell_j] = -1
            source_supply[key_cell_i] -= destination_demand[key_cell_j]
            destination_demand[key_cell_j] = 0
        elif source_supply[key_cell_i] < destination_demand[key_cell_j]:
            result_cost_matrix[key_cell_i][key_cell_j] = source_supply[key_cell_i] * cost_matrix[key_cell_i][key_cell_j]
            result_matrix[key_cell_i][key_cell_j] = source_supply[key_cell_i]
            for j in range(len(cost_matrix[key_cell_i])):
                cost_matrix[key_cell_i][j] = -1
            destination_demand[key_cell_j] -= source_supply[key_cell_i]
            source_supply[key_cell_i] = 0
        else:
            result_cost_matrix[key_cell_i][key_cell_j] = destination_demand[key_cell_j] * cost_matrix[key_cell_i][key_cell_j]
            result_matrix[key_cell_i][key_cell_j] = source_supply[key_cell_i]
            for supply in cost_matrix:
                supply[key_cell_j] = -1
            for j in range(len(cost_matrix[key_cell_i])):
                cost_matrix[key_cell_i][j] = -1
            destination_demand[key_cell_j] = 0
            source_supply[key_cell_i] = 0

    print("North-west approximation method basic feasible solution:")
    print_matrix(result_matrix)
    print("Total cost of the solution is", sum_matrix(result_cost_matrix), sep=" ")

#Bugged. Find why matrices are being nullified, and why the code chooses wrong cell (Step 2)
def vogel(cost_matrix, source_supply, destination_demand):
    result_matrix = [[0 for _ in range(4)] for _ in range(3)]
    result_cost_matrix = [[0 for _ in range(4)] for _ in range(3)]
    while source_supply.count(0) < len(source_supply) and destination_demand.count(0) < len(destination_demand):
        #True for row, False for column
        row_or_column = True
        difference_rows = list()
        for row in cost_matrix:
            row_copy = row.copy()
            row_copy.sort()
            while row_copy.count(-1) > 0:
                row_copy.remove(-1)
            if len(row_copy) > 2:
                difference_rows.append(row_copy[1] - row_copy[0])
            elif len(row_copy) == 1:
                difference_rows.append(row_copy[0])
            else:
                difference_rows.append(-1)
        difference_columns = list()
        for i in range(len(cost_matrix[0])):
            column = list()
            for row in cost_matrix:
                column.append(row[i])
            column.sort()
            while column.count(-1) > 0:
                column.remove(-1)
            if len(column) > 2:
                difference_columns.append(column[1] - column[0])
            elif len(column) == 1:
                difference_columns.append(column[0])
            else:
                difference_columns.append(-1)
        line_index = difference_rows.index(max(difference_rows))
        if max(difference_columns) > max(difference_rows):
            line_index = difference_columns.index(max(difference_columns))
            row_or_column = False
        if row_or_column:
            key_cell_i = line_index
            key_cell_j = cost_matrix[key_cell_i].index(min(cost_matrix[key_cell_i]))
        else:
            key_cell_i = 0
            key_cell_j = line_index
            min_value = 10 ** 10
            for i in range(len(cost_matrix)):
                if cost_matrix[i][key_cell_j] < min_value:
                    key_cell_i = i
                    max_value = cost_matrix[i][key_cell_j]
        if source_supply[key_cell_i] > destination_demand[key_cell_j]:
            result_cost_matrix[key_cell_i][key_cell_j] = destination_demand[key_cell_j] * cost_matrix[key_cell_i][key_cell_j]
            result_matrix[key_cell_i][key_cell_j] = destination_demand[key_cell_j]
            for supply in cost_matrix:
                supply[key_cell_j] = -1
            source_supply[key_cell_i] -= destination_demand[key_cell_j]
            destination_demand[key_cell_j] = 0
        elif source_supply[key_cell_i] < destination_demand[key_cell_j]:
            result_cost_matrix[key_cell_i][key_cell_j] = source_supply[key_cell_i] * cost_matrix[key_cell_i][key_cell_j]
            result_matrix[key_cell_i][key_cell_j] = source_supply[key_cell_i]
            for j in range(len(cost_matrix[key_cell_i])):
                cost_matrix[key_cell_i][j] = -1
            destination_demand[key_cell_j] -= source_supply[key_cell_i]
            source_supply[key_cell_i] = 0
        else:
            result_cost_matrix[key_cell_i][key_cell_j] = destination_demand[key_cell_j] * cost_matrix[key_cell_i][key_cell_j]
            result_matrix[key_cell_i][key_cell_j] = source_supply[key_cell_i]
            for supply in cost_matrix:
                supply[key_cell_j] = -1
            for j in range(len(cost_matrix[key_cell_i])):
                cost_matrix[key_cell_i][j] = -1
            destination_demand[key_cell_j] = 0
            source_supply[key_cell_i] = 0
    print("Vogel's approximation method basic feasible solution:")
    print_matrix(result_matrix)
    print("Total cost of the solution is", sum_matrix(result_cost_matrix), sep=" ")

def russel(cost_matrix, source_supply, destination_demand):
    print("solved")

def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in matrix[i]:
            print(j, end=" ")
        print()

def sum_matrix(matrix):
    sum = 0
    for i in matrix:
        for j in i:
            sum += j
    return sum

def get_cost_matrix_input():
    print("Input cost matrix")
    cost_matrix = [[0 for _ in range(4)] for _ in range(3)]
    for i in range(3):
        cost_matrix[i] = [int(x) for x in input().split()]
    return cost_matrix

def get_vector():
    return [int(x) for x in input().split()]

def get_double_matrix_copy(matrix):
    result = [[0 for _ in range(4)] for _ in range(3)]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            result[i][j] = matrix[i][j]
    return result



if __name__ == "__main__":
    cost_matrix = get_cost_matrix_input()
    print("Input source supply vector")
    source_supply = get_vector()
    print("input destination demand vector")
    destination_demand = get_vector()
    north_west_corner(get_double_matrix_copy(cost_matrix), source_supply.copy(), destination_demand.copy())
    vogel(get_double_matrix_copy(cost_matrix), source_supply.copy(), destination_demand.copy())
    russel(get_double_matrix_copy(cost_matrix), source_supply.copy(), destination_demand.copy())

