#!/usr/bin/python3

import io

def work(num_workers, tasks, verbose=False, simulate_time=False):
    todo_list = sorted(tasks.keys())
    completed = set()
    worker_task = [None] * num_workers
    worker_time = [0] * num_workers
    time_spent = 0
    output = io.StringIO()

    while len(completed) != len(tasks):
        if verbose:
            print('Second', time_spent, end='\t')
        for i in range(num_workers):
            if worker_task[i] is not None:
                worker_time[i] -= 1
            else:
                for todo in todo_list:
                    for step in tasks[todo]:
                        if step not in completed:
                            break
                    else:
                        worker_task[i] = todo
                        worker_time[i] = (ord(todo)-65+60) if simulate_time else 0
                        todo_list.remove(todo)
                        break
            if verbose:
                if worker_task[i] is None:
                    print('-', end=' ')
                else:
                    print(worker_task[i], end=' ')
        if verbose:
            print(output.getvalue(), end='')
        for i in range(num_workers):
            if worker_task[i] is not None and worker_time[i] <= 0:
                completed.add(worker_task[i])
                output.write(worker_task[i])
                worker_task[i] = None
        time_spent += 1
        if verbose:
            print()
    if simulate_time:
        print(time_spent)
    else:
        print(output.getvalue())



def main():
    dependencies = {}

    with open('../input/07.txt') as infile:
        data = [(line[36], line[5]) for line in infile]
        for d in data:
            dependencies[d[0]] = []
            dependencies[d[1]] = []
        for d in data:
            dependencies[d[0]].append(d[1])

    work(1, dependencies)
    work(5, dependencies, simulate_time=True)

if __name__ == "__main__":
    main()
