from pysat.solvers import Glucose3
import math
import csv


def build_clauses(grid, grid2, N, D):

    # to get the variable corresponding to (i,j)th cell containing kth digit

    def value1(i, j, k):
        return N*N*(i-1)+(j-1)*N+(k-1)+1

    def value2(i, j, k):
        return N*N*(i-1)+(j-1)*N+(k-1)+1 + N*N*N

    # clauses will form the CNF formula

    clauses = Glucose3()

    # to ensure that each cell have exactly one value

    for i in range(1, N+1):
        for j in range(1, N+1):

            # The cell at (i,j) has at least one value

            clauses.add_clause([value1(i, j, k) for k in range(1, N+1)])
            clauses.add_clause([value2(i, j, k) for k in range(1, N+1)])

            # The cell at (i,j) has at most one value

            for k in range(1, N+1):
                for k_ in range(k+1, N+1):
                    clauses.add_clause([-value1(i, j, k), -value1(i, j, k_)])
                    clauses.add_clause([-value2(i, j, k), -value2(i, j, k_)])

    # to ensure that each sub-grid(row, column, block) containes all the numbers from 1 to K*K

    def val(grid_block):
        # The new clauses
        # ensure that the cells contain distinct values.
        for i, i_ in enumerate(grid_block):
            for j, j_ in enumerate(grid_block):
                if i < j:
                    for k in range(1, N+1):
                        clauses.add_clause(
                            [-value1(i_[0], i_[1], k), -value1(j_[0], j_[1], k)])
                        clauses.add_clause(
                            [-value2(i_[0], i_[1], k), -value2(j_[0], j_[1], k)])

    # ensure rows and columns have distinct values
    for i in range(1, N+1):
        val([(i, j) for j in range(1, N+1)])
        val([(j, i) for j in range(1, N+1)])

    # ensure DxD sub-grids "regions" have distinct values
    sub_grid_index = []
    for i in range(0, D):
        sub_grid_index.append(i*D+1)
    for i in sub_grid_index:
        for j in sub_grid_index:
            val([(i + k % D, j + k // D) for k in range(N)])

    # this is to ensure that clues(cells which already contain a number) are not updated
    for i in range(1, N+1):
        for j in range(1, N+1):
            k = int(grid[i - 1][j - 1])
            k_ = int(grid2[i - 1][j - 1])
            if k:
                clauses.add_clause([value1(i, j, k)])
            if k_:
                clauses.add_clause([value2(i, j, k_)])

                # to ensure that if there are corresponding blank cells in the two sudokus then they do not contain same value

            if k == 0 and k_ == 0:
                for d in range(1, N+1):
                    clauses.add_clause([-value1(i, j, d), -value2(i, j, d)])

    # now the formula is ready

    p = clauses.solve()
    print("The solutions are :") if p else print("None")
    if(p):
        sol = set(clauses.get_model())

        # this is to fill the grids from the model

        def read_cell1(i, j):
            for k in range(1, N+1):
                if value1(i, j, k) in sol:
                    return k

        def read_cell2(i, j):
            for k in range(1, N+1):
                if value2(i, j, k) in sol:
                    return k

        for i in range(1, N+1):
            for j in range(1, N+1):
                grid[i - 1][j - 1] = read_cell1(i, j)
                grid2[i - 1][j - 1] = read_cell2(i, j)

        # to print the final solution on terminal

        print(*grid, sep="\n")
        print("")
        print(*grid2, sep="\n")


if __name__ == '__main__':

    # change to name of the .csv file for different test cases
    file = "test_case.csv"
    rows = []
    grid1 = []
    grid2 = []

    with open(file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)

        for row in csvreader:
            rows.append(row)
    N = len(rows[0])
    D = int(math.sqrt(N))
    for i in range(0, N):
        grid1.append(rows[i])
        grid2.append(rows[i+N])

    build_clauses(grid1, grid2, N, D)
