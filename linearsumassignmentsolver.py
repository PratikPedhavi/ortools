from ortools.graph import pywrapgraph

def main():
    assignment = pywrapgraph.LinearSumAssignment()

    costs = [
    [90, 76, 75, 70],
    [35, 85, 55, 65],
    [125, 95, 90, 105],
    [45, 110, 95, 115],
    ]
    num_workers = len(costs)
    num_tasks = len(costs[0])

    for worker in range(num_workers):
        for task in range(num_tasks):
            if costs[worker][task]:
                assignment.AddArcWithCost(worker, task, costs[worker][task])

    status = assignment.Solve()

    if status == assignment.OPTIMAL:
        print(f'Total cost = {assignment.OptimalCost()}\n')
        for node in range(assignment.NumNodes()):
            print('Worker {} is assigned to task {}. Cost of assignment = {}' \
            .format(node, assignment.RightMate(node), costs[node][assignment.RightMate(node)]))

    elif status == assignment.INFEASIBLE:
        print('No Assignment is possible')
    elif status == assignment.POSSIBLE_OVERFLOW:
        print(' some input costs are too large and may cause an integer overflow')

if __name__ == '__main__':
    main()