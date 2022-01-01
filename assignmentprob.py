from ortools.linear_solver import pywraplp

def main():
    #data
    costs = [
        [90, 80, 75, 70],
        [35, 85, 55, 65],
        [125, 95, 90, 95],
        [45, 110, 95, 115],
        [50, 100, 90, 100]
    ]
    num_workers = len(costs)
    num_tasks = len(costs[0])

    # Create the mip solver with the SCIP backend
    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    x = {}
    for i in range(num_workers):
        for j in range(num_tasks):
            x[i, j] = solver.IntVar(0,1, '')

    # Constraints
    for i in range(num_workers):
        solver.Add(solver.Sum([x[i,j] for j in range(num_tasks)]) <= 1)
    
    for j in range(num_tasks):
        solver.Add(solver.Sum([x[i,j] for i in range(num_workers)]) == 1)

    # Objective 
    objective_terms = []
    for i in range(num_workers):
        for j in range(num_tasks):
            objective_terms.append(costs[i][j] * x[i,j])
    solver.Minimize(solver.Sum(objective_terms))

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or pywraplp.Solver.FEASIBLE:
        print('Total Cost = ', solver.Objective().Value(), '\n')
        for i in range(num_workers):
            for j in range(num_tasks):
                if x[i,j].solution_value() > 0.5:
                    print('worker {} assigned to task {}. Cost = {}'.format(i,j,costs[i][j]))

if __name__ == "__main__":
    main()
