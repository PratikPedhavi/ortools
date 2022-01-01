from ortools.sat.python import cp_model

def main():
    #data
    costs = [
        [90, 80, 75, 70],
        [35, 85, 55, 65],
        [125, 95, 90, 95],
        [45, 110, 95, 115],
        [50, 100, 90, 100],
        [45, 34, 66, 100]
    ]
    num_workers = len(costs)
    num_tasks = len(costs[0])

    team1 = [0,2,4]
    team2 = [1,3,5]
    team_max = 2

    # Model
    model = cp_model.CpModel()

    # Variables
    x = {}
    for worker in range(num_workers):
        for task in range(num_tasks):
            x[worker, task] = model.NewBoolVar('x[{}, {}'.format(worker, task))

    # Constraints
    for worker in range(num_workers):
        model.Add(sum([x[worker, task] for task in range(num_tasks)]) <=1)

    for task in range(num_tasks):
        model.Add(sum([x[worker, task] for worker in range(num_workers)]) == 1)

    team_task1 = []
    for worker in team1:
        for task in range(num_tasks):
            team_task1.append(x[worker, task])
    model.Add(sum(team_task1) <= team_max)

    team_task2 = []
    for worker in team2:
        for task in range(num_tasks):
            team_task2.append(x[worker,task])
    model.Add(sum(team_task2) <= team_max)
    
    # Objective 
    objective_terms = []
    for worker in range(num_workers):
        for task in range(num_tasks):
            objective_terms.append(costs[worker][task] * x[worker,task])
    model.Minimize(sum(objective_terms))

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or cp_model.FEASIBLE:
        print('Total Cost = ', solver.ObjectiveValue(), '\n')
        for worker in range(num_workers):
            for task in range(num_tasks):
                if solver.BooleanValue(x[worker,task]):
                    print('worker {} assigned to task {}. Cost = {}'.format(worker,task,costs[worker][task]))

    else: 
        print('No Solution Found')

if __name__ == '__main__':
    main()