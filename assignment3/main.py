from prettytable import PrettyTable

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
    #Initialize result matrix
    result_matrix = [[0 for _ in range(4)] for _ in range(3)]
    #Solve until there is no supply and demand left
    while source_supply.count(0) < len(source_supply) and destination_demand.count(0) < len(destination_demand):
        key_cell_i = 0
        key_cell_j = 0
        #Finding the most north-west possible cell
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
        #Allocating supply to found cell
        allocate_supply(key_cell_i, key_cell_j, cost_matrix, result_matrix, destination_demand, source_supply)
    #Printing results
    print("North-west corner method basic feasible solution:")
    print_matrix(result_matrix)

def vogel(cost_matrix, source_supply, destination_demand):
    #Initializing results matrix
    result_matrix = [[0 for _ in range(4)] for _ in range(3)]
    # Solve until there is no supply and demand left
    while source_supply.count(0) < len(source_supply) and destination_demand.count(0) < len(destination_demand):
        #True for row, False for column
        row_or_column = True
        #Finding penalties for rows
        difference_rows = list()
        for row in cost_matrix:
            row_copy = row.copy()
            row_copy.sort()
            #Getting rid of unwanted -1 ("Indications, that the row/column is disabled")
            while row_copy.count(-1) > 0:
                row_copy.remove(-1)
            # Calculating penalty in case of two or more values being available
            if len(row_copy) >= 2:
                difference_rows.append(row_copy[1] - row_copy[0])
            # If only one value is available, consider it as a penalty
            elif len(row_copy) == 1:
                difference_rows.append(row_copy[0])
            # If no values are available - mark the row as disabled
            else:
                difference_rows.append(-1)
        #Finding penalties for columns
        difference_columns = list()
        for i in range(len(cost_matrix[0])):
            column = list()
            for row in cost_matrix:
                column.append(row[i])
            column.sort()
            # Getting rid of unwanted -1 ("Indications, that the row/column is disabled")
            while column.count(-1) > 0:
                column.remove(-1)
            # Calculating penalty in case of two or more values being available
            if len(column) > 2:
                difference_columns.append(column[1] - column[0])
            # If only one value is available, consider it as a penalty
            elif len(column) == 1:
                difference_columns.append(column[0])
            # If no values are available - mark the row as disabled
            else:
                difference_columns.append(-1)
        #Finding the biggest penalty possible
        line_index = difference_rows.index(max(difference_rows))
        if max(difference_columns) > max(difference_rows):
            line_index = difference_columns.index(max(difference_columns))
            row_or_column = False
        #Finding the minimum cost cell in known row
        if row_or_column:
            key_cell_i = line_index
            min_value = 10 ** 10
            for j in range(len(cost_matrix[key_cell_i])):
                if cost_matrix[key_cell_i][j] < min_value and cost_matrix[key_cell_i][j] != -1:
                    key_cell_j = j
                    min_value = cost_matrix[key_cell_i][j]
        #Finding the minimum cost cell in known column
        else:
            key_cell_i = 0
            key_cell_j = line_index
            min_value = 10 ** 10
            for i in range(len(cost_matrix)):
                if cost_matrix[i][key_cell_j] < min_value and cost_matrix[i][key_cell_j] != -1:
                    key_cell_i = i
                    max_value = cost_matrix[i][key_cell_j]
        #Allocating supply from found supply to found demand
        allocate_supply(key_cell_i, key_cell_j, cost_matrix, result_matrix, destination_demand, source_supply)

    #Printing the results
    print("Vogel's approximation method basic feasible solution:")
    print_matrix(result_matrix)

def russel(cost_matrix, source_supply, destination_demand):
    # Initializing result matrix
    result_matrix = [[0 for _ in range(4)] for _ in range(3)]
    #Initializing russel matrix
    russel_matrix = [[0 for _ in range(4)] for _ in range(3)]
    #Solving until supply and demand reaches zero
    while source_supply.count(0) < len(source_supply) and destination_demand.count(0) < len(destination_demand):
        # Constructing Russel's matrix
        for i in range(len(cost_matrix)):
            for j in range(len(cost_matrix[i])):
                #Convert value, until it has been disabled (-1 indicator)
                if cost_matrix[i][j] != -1:
                    highest_row_cost = 0
                    highest_column_cost = 0
                    for r in cost_matrix[i]:
                        highest_row_cost = max(highest_row_cost, r)
                    for c in cost_matrix:
                        highest_column_cost = max(highest_column_cost, c[j])
                    russel_matrix[i][j] = cost_matrix[i][j] - highest_column_cost - highest_row_cost
                #If value is disabled, set value to None
                else:
                    russel_matrix[i][j] = None
        max_absolute_value = 0
        key_cell_i = 0
        key_cell_j = 0
        # Finding cell with the maximum absolute value
        for i in range(len(russel_matrix)):
            for j in range(len(russel_matrix[i])):
                if russel_matrix[i][j] != None:
                    if abs(russel_matrix[i][j]) > max_absolute_value:
                        max_absolute_value = abs(russel_matrix[i][j])
                        key_cell_i = i
                        key_cell_j = j

        # Allocating supply to the found supply from found demand
        allocate_supply(key_cell_i, key_cell_j, cost_matrix, result_matrix, destination_demand, source_supply)

    print("Russell's approximation method basic feasible solution:")
    print_matrix(result_matrix)

def allocate_supply(key_cell_i, key_cell_j, cost_matrix, result_matrix, destination_demand, source_supply):
    #Working with case of supply in the source, being higher than demand
    if source_supply[key_cell_i] > destination_demand[key_cell_j]:
        result_matrix[key_cell_i][key_cell_j] = destination_demand[key_cell_j]
        #Setting the demand as disabled
        for supply in cost_matrix:
            supply[key_cell_j] = -1
        source_supply[key_cell_i] -= destination_demand[key_cell_j]
        destination_demand[key_cell_j] = 0
    #Working with case of demand, being higher than supply
    elif source_supply[key_cell_i] < destination_demand[key_cell_j]:
        result_matrix[key_cell_i][key_cell_j] = source_supply[key_cell_i]
        # Setting the supply as disabled
        for j in range(len(cost_matrix[key_cell_i])):
            cost_matrix[key_cell_i][j] = -1
        destination_demand[key_cell_j] -= source_supply[key_cell_i]
        source_supply[key_cell_i] = 0
    #Working with case of demand and supply being equal (combination of previous two cases)
    else:
        result_matrix[key_cell_i][key_cell_j] = source_supply[key_cell_i]
        for supply in cost_matrix:
            supply[key_cell_j] = -1
        for j in range(len(cost_matrix[key_cell_i])):
            cost_matrix[key_cell_i][j] = -1
        destination_demand[key_cell_j] = 0
        source_supply[key_cell_i] = 0

def print_matrix(matrix):
    '''
    Prints given matrix
    '''
    for i in range(len(matrix)):
        for j in matrix[i]:
            print(j, end=" ")
        print()

def sum_matrix(matrix):
    '''
    Returns the summation of all elements in given matrix
    '''
    sum = 0
    for i in matrix:
        for j in i:
            sum += j
    return sum

def get_cost_matrix_input():
    '''
    Gets input for the cost matrix, and returns one
    '''
    print("Input cost matrix")
    cost_matrix = [[0 for _ in range(4)] for _ in range(3)]
    for i in range(3):
        cost_matrix[i] = [int(x) for x in input().split()]
    return cost_matrix

def get_vector():
    '''
    Gets input for source supply and destination demand vectors
    '''
    return [int(x) for x in input().split()]

def get_double_array_copy(matrix):
    '''
    Gets a copy of a double array, so the methods won't change the initial matrix
    '''
    result = [[0 for _ in range(4)] for _ in range(3)]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            result[i][j] = matrix[i][j]
    return result

def check_balance(source_supply, destination_demand):
    '''
    Checks if the problem is balanced
    '''
    if sum(source_supply) != sum(destination_demand):
        print("The problem is not balanced!")
        exit(0)

def check_dimensions(cost_matrix, source_supply, destination_demand):
    '''
    Checks dimensions of input data
    :return:
    '''
    # Check if cost matrix dimensions align with source supply and destination demand
    if len(cost_matrix) != len(source_supply) and (len(destination) for destination in cost_matrix) != destination_demand:
        print("The method is not applicable!")
        exit(0)
    # Check if cost matrix dimensions don't apply to the given task
    if len(cost_matrix) != 3 and (len(destination) for destination in cost_matrix) != 4:
        print("The method is not applicable!")
        exit(0)

def construct_input_table(cost_matrix, source_supply, destination_demand):
    '''
    Constructs and prints input parameter table
    :return:
    '''
    parameter_table = PrettyTable([" ", "D1", "D2", "D3", "D4", "Supply"])

    parameter_table.add_row(
        ["S1", cost_matrix[0][0], cost_matrix[0][1], cost_matrix[0][2], cost_matrix[0][3], source_supply[0]])
    parameter_table.add_row(
        ["S2", cost_matrix[1][0], cost_matrix[1][1], cost_matrix[1][2], cost_matrix[1][3], source_supply[1]])
    parameter_table.add_row(
        ["S3", cost_matrix[2][0], cost_matrix[2][1], cost_matrix[2][2], cost_matrix[2][3], source_supply[2]])
    parameter_table.add_row(
        ["Demand: ", destination_demand[0], destination_demand[1], destination_demand[2], destination_demand[3], " "]
    )

    print("Input parameter table:")
    print(parameter_table)

if __name__ == "__main__":
    cost_matrix = get_cost_matrix_input()
    print("Input source supply vector")
    source_supply = get_vector()
    print("input destination demand vector")
    destination_demand = get_vector()
    check_balance(source_supply, destination_demand)
    check_dimensions(cost_matrix, source_supply, destination_demand)
    construct_input_table(cost_matrix, source_supply, destination_demand)
    north_west_corner(get_double_array_copy(cost_matrix), source_supply.copy(), destination_demand.copy())
    vogel(get_double_array_copy(cost_matrix), source_supply.copy(), destination_demand.copy())
    russel(get_double_array_copy(cost_matrix), source_supply.copy(), destination_demand.copy())





