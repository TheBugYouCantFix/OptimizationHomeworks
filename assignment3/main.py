def north_west_corner(cost_matrix, source_supply, destination_demand):
    result_matrix = [[0 for _ in range(4)] for _ in range(3)]
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
            result_matrix[key_cell_i][key_cell_j] = destination_demand[key_cell_j] * cost_matrix[key_cell_i][key_cell_j]
            for supply in cost_matrix:
                supply[key_cell_j] = -1
            source_supply[key_cell_i] -= destination_demand[key_cell_j]
            destination_demand[key_cell_j] = 0
        elif source_supply[key_cell_i] < destination_demand[key_cell_j]:
            result_matrix[key_cell_i][key_cell_j] = destination_demand[key_cell_j] * cost_matrix[key_cell_i][key_cell_j]
            for j in range(len(cost_matrix[key_cell_i])):
                cost_matrix[key_cell_i][j] = -1
            destination_demand[key_cell_j] -= source_supply[key_cell_i]
            source_supply[key_cell_i] = 0
        else:
            result_matrix[key_cell_i][key_cell_j] = destination_demand[key_cell_j] * cost_matrix[key_cell_i][key_cell_j]
            for supply in cost_matrix:
                supply[key_cell_j] = -1
            for j in range(len(cost_matrix[key_cell_i])):
                cost_matrix[key_cell_i][j] = -1
            destination_demand[key_cell_j] = 0
            source_supply[key_cell_i] = 0

    return result_matrix




def vogel(cost_matrix, source_supply, destination_demand):
    print("solved")

def russel(cost_matrix, source_supply, destination_demand):
    print("solved")

def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in matrix[i]:
            print(j, end=" ")
        print()

def get_cost_matrix_input():
    print("Input cost matrix")
    cost_matrix = [[0 for _ in range(4)] for _ in range(3)]
    for i in range(3):
        cost_matrix[i] = [int(x) for x in input().split()]
    return cost_matrix

def get_vector():
    return [int(x) for x in input().split()]



if __name__ == "__main__":
    cost_matrix = get_cost_matrix_input()
    print("Input source supply vector")
    source_supply = get_vector()
    print("input destination demand vector")
    destination_demand = get_vector()
    print("North-west approximation method basic feasible solution:")
    print_matrix(north_west_corner(cost_matrix, source_supply, destination_demand))
    vogel(cost_matrix, source_supply, destination_demand)
    russel(cost_matrix, source_supply, destination_demand)

