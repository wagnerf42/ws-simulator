#!/usr/bin/env python3.5
"""
the task module provides a Task class
holding work of task and list of its children for the simulation.
"""
from copy import deepcopy
import json
from collections import deque



class Task:
    """
    class represent Task with its work, list of children.
    work : work of tasks, task is virtual if work=0
    childrens : list of dependent tasks
    """

    def __init__(self, work, children, children_id=None, task_id=0, start_time=0  ,is_DAG=False):
        self.id = task_id # id of task will be update when we intialise tasks
        self.work = work
        self.children = children
        self.children_id = children_id
        self.start_time = start_time  # at which time is the task started
        self.dependent_tasks_number = 0 # it will be intialised when we initialise tasks
        self.is_DAG = is_DAG

    def total_work(self):
        """
        returns work contained in ourselves and all our children
        """
        if self.children:
            #return sum(child.total_work() for child in self.children)
            return self.work
        else:
            return self.work

    def split_work(self, current_time, granularity):
        """
        cut task in two if we have enough remaining work (updates self,
        returns next idle time event and new task)
        """
        computed_work = current_time - self.start_time
        remaining_work = self.work - computed_work
        assert remaining_work >= 0
        my_share = remaining_work//2
        if my_share > granularity:
            # we have enough work to share
            self.work = computed_work + my_share
            other_share = remaining_work - my_share
            return current_time + my_share, \
                Task(other_share, [])

    def end_execute_task(self):
        """
        return all children tasks
        """
       # print(" End of execution of : ", self.id ,"(",self.total_work(),")")
        #print("number of children id: ", self.children_id)
        if self.is_DAG:
            ready_children = []
            #print("number of children : ", len(self.children))
            # reversed because next task to execute should be pushed last
            for child in reversed(self.children):
                child.update_dependent_task()
                if child.dependent_tasks_number == 0:
                    ready_children.append(child)
            #print("ready_children : ", ready_children)
            return ready_children
        else:
            return self.children

    def finishes_at(self, finish_time, processor_speed):
        """
        compute if we finish at given time with given speed
        """
        return (finish_time - self.start_time) * processor_speed == self.work

    def update_dependent_task(self):
       """
       decrease the number of dependents task when it's finished
       When the number of dependent tasks is 0, we return the tasks with true.
       """
       self.dependent_tasks_number -= 1

    def display(self, depth=0, is_tree=True):
        """
        display tasks with work and its childrens
        """
        if is_tree:
            print("task_id:{} Work:{} children:{}, start_time:{}"
                  .format(
                      self.id, self.work, [t.id for t in self.children], self.start_time
                  ))
        else:
            print("  "*depth, "[")
            print("  "*depth, id(self), " ", self.work)
            for child in self.children:
                child.display(depth+1)
            print("  "*depth, "]")




def init_task_tree(total_work=0, threshold=0, file_name=None, task_id=0):
    """
    create the task tree recursively
    """
    if file_name is not None:
        tasks, work, depth, logs = read_task_tree_from_json(file_name)
        return tasks[0], work, depth, logs
    else:
        #if total_work//2 < threshold:
        if total_work <= threshold:
           # print("T", task_id )
            return Task(total_work, [], task_id=task_id)
        else:
           # print("T", task_id , " -> T",(task_id*2 + 1) , " , T", (task_id*2 + 2))
            if (total_work//2 <= threshold):
                return Task(0, [
                    init_task_tree(total_work=threshold  , threshold=threshold, task_id=(task_id*2 + 1)),
                    init_task_tree(total_work=total_work-threshold, threshold=threshold, task_id=(task_id*2 + 2))
                    ], task_id=task_id)
            else:
                return Task(0, [
                    init_task_tree(total_work=total_work//2, threshold=threshold, task_id=(task_id*2 + 1)),
                    init_task_tree(total_work=total_work-total_work//2, threshold=threshold, task_id=(task_id*2 +2))
                    ], task_id=task_id)





CACHE = dict()
def init_task_tree_with_cache(total_work, threshold):
    """
    create the task tree recursively
    """
    global CACHE
    if (total_work, threshold) in CACHE:
        return deepcopy(CACHE[(total_work, threshold)])

    if total_work//2 < threshold:
        result = Task(total_work, [])
    else:
        result = Task(0, [
            init_task_tree(total_work//2, threshold),
            init_task_tree(total_work-total_work//2, threshold)
            ])

        CACHE[(total_work, threshold)] = deepcopy(result)
    return result


def update_dependencies(tasks):
    """
    update dependencies by update number of related tasks
    """
    for task in tasks:
        for children_id in task.children_id:
            tasks[children_id].dependent_tasks_number = tasks[children_id].dependent_tasks_number + 1
            task.children.append(tasks[children_id])
    return tasks



def read_task_tree_from_json(file_name):
    """
    Read task from json file
    stor tasks in list
    """
    tasks = []
    with open(file_name) as file:
        logs = json.load(file)

    #tasks = [
    #    Task(
    #        l["end_time"] - l["start_time"],
    #        [],
    #        children_id = l["children"],
    #        task_id = i
    #    )
    #    for (i, l) in enumerate(logs) ]

    for task_index, task in enumerate(logs["tasks_logs"]):
        current_task = Task(
            task["end_time"]-task["start_time"],
            [], children_id=task["children"], task_id=task_index,
            start_time=task["start_time"],  is_DAG=True)
        tasks.append(current_task)

    work = compute_work(tasks)
    tasks = update_dependencies(tasks)
    depth = compute_depth(tasks)

    return tasks, work, depth, logs


def display_DAG(DAG, level="", level_num=0):
    DAG.display()
    level_num = level_num + 1
    level = level + "--"
    print(level_num, level, end='')
    for child in DAG.children:
        display_DAG(child, level=level, level_num=level_num)


def compute_depth(tasks):
    """
    compute the depth of the graph of given tasks.
    """
    depths = [0 for _ in tasks]
    size = len(tasks)
    tasks_ids = list(range(size))
    tasks_ids.sort(key=lambda i: tasks[i].start_time)#, reversed=True)
    tasks_ids.reverse()

    for task_id in tasks_ids:
        task = tasks[task_id]
        if task.children:
            depths[task_id] = task.total_work() + max(depths[c] for c in task.children_id)
        else:
            depths[task_id] = task.total_work()

    return depths[0]


def compute_work(tasks):
    """
    compute the total work of the graph of given tasks.
    """
    return sum(t.total_work() for t in tasks)


def get_critical_path(DAG):
    """
    compute critical path of the Graphe
    """
    return DAG.total_work() + max(get_critical_path(c) for c in DAG.children)
    critical_path = 0
    # if len(DAG.children) == 0:
    if not DAG.children:
        return DAG.total_work()
    else:
        for child in DAG.children:
           child_critical_path = get_critical_path(child)
           if(child_critical_path > critical_path):
               critical_path = child_critical_path + child.total_work()
        return critical_path

def get_work(DAG):
    """
    compute the total work in the graphe
    """
    return DAG.total_work() + sum(get_critical_path(c) for c in DAG.children)
    total_work = 0
    if len(DAG.children) == 0:
        return DAG.total_work()
    else:
        for child in DAG.children:
            child_total_work = get_work(child)
            total_work = child_total_work + child.total_work()
        return total_work




#DAG = init_task_tree(file_name="../tasks_file/merge_sort32.json" )

#display_DAG(DAG)


#work, depth = get_info(DAG)

#print("work:", work, "critical_path", critical_path)




