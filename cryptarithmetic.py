# CRYPTARITHMETIC PUZZLE

from ortools.sat.python import cp_model

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print('{}={}'.format(v, self.Value(v)), end=' ')
        print()

    def solution_count(self):
        return self.__solution_count

def main():
    ''' 
        CP engine 
    '''

    model = cp_model.CpModel()

    base = 10

    c = model.NewIntVar(1, base-1, 'C')
    p = model.NewIntVar(0, base-1, 'P')
    i = model.NewIntVar(1, base-1, 'I')
    s = model.NewIntVar(0, base-1, 'S')
    f = model.NewIntVar(1, base-1, 'F')
    u = model.NewIntVar(0, base-1, 'U')
    n = model.NewIntVar(0, base-1, 'N')
    t = model.NewIntVar(1, base-1, 'T')
    r = model.NewIntVar(0, base-1, 'R')
    e = model.NewIntVar(0, base-1, 'E')

    # We group variables in a list to apply constraint 'AllDifferent'
    letters = [c, p, i, s, f, u, n, t, r, e]

    # Verify that we have enough digits
    assert base >= len(letters)

    # Define Constraints
    model.AddAllDifferent(letters)

    # CP + IS + FUN = TRUE
    model.Add( c * base + p + i * base + s + f * base * base + u * base + n 
                    == t * base * base * base + r * base * base + u * base + e)

    # Call solver 
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter(letters)
    # Enumerate all solutions
    solver.parameters.enumerate_all_solutions = True
    # Solve 
    status = solver.Solve(model, solution_printer)

    # Statistics
    print('status       : {}'.format(solver.StatusName(status)))
    print('Wall Time    : {} s'.format(solver.WallTime()))
    print('sol found    : {}'.format(solution_printer.solution_count()))


if __name__ == '__main__':
    main()