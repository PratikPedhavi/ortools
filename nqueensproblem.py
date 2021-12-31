## Solution to N-Queens Problem

import sys
import time
from ortools.sat.python import cp_model

class NQueenSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, queens):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__queens = queens
        self.__solution_count = 0
        self.__start_time = time.time()

    def solution_count(self):
        return self.__solution_count

    def on_solution_callback(self):
        current_time = time.time()
        print('Solution {}, time = {} s '.format(self.__solution_count, current_time - self.__start_time))
        self.__solution_count += 1
        
        all_queens = range(len(self.__queens))
        for i in all_queens:
            for j in all_queens:
                if self.Value(self.__queens[j]) == i:
                    print('Q', end = ' ')
                else:
                    print('_', end=' ')
            print()
        print()

def main(board_size):
    model = cp_model.CpModel()

    # Array index is the column and the value is the row
    queens = [model.NewIntVar(0, board_size -1, 'x{}'.format(i)) for i in range(board_size)]

    # All rows must be different 
    model.AddAllDifferent(queens)

    # No two queens can be on the same diagonal
    model.AddAllDifferent([queens[i] + i for i in range(board_size)])
    model.AddAllDifferent([queens[i] - i for i in range(board_size)])

    # Solve the model
    solver = cp_model.CpSolver()
    solution_printer = NQueenSolutionPrinter(queens)
    solver.parameters.enumerate_all_solutions = True
    solver.Solve(model, solution_printer)

    # Statistics
    print(f' conflicts   : {solver.NumConflicts()}')
    print(f' branches   : {solver.NumBranches()}')
    print(f' wall time   : {solver.WallTime()} s')
    print(f' solutions found   : {solution_printer.solution_count()}')




if __name__ == "__main__":
    size = 4
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    main(size)

