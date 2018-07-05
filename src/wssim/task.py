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

    def __init__(self, work, children, children_id=None, task_id=0):
        self.id = task_id # id of task will be update when we intialise tasks
        self.work = work
        self.children = children
        self.children_id = children_id
        self.start_time = 0  # at which time is the task started
        self.dependent_tasks_number = 0 # it will be intialised when we initialise tasks

    def total_work(self):
        """
        returns work contained in ourselves and all our children
        """
        if self.children:
            return sum(child.total_work() for child in self.children)
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
        if self.children_id is not None:
            ready_children = []
            for child in self.children:
                child.update_dependent_task()
                if child.dependent_tasks_number == 0:
                    ready_children.append(child)
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
            print("task_id:{} Work:{} children_id:{} children:{} dependent_tasks_number:{}"
                  .format(
                      self.id, self.work, self.children_id, self.children,
                      self.dependent_tasks_number
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
        tasks = read_task_tree_from_json(file_name)
        return tasks[0]
    else:
        if total_work//2 < threshold:
            return Task(total_work, [])
        else:
            return Task(0, [
                init_task_tree(total_work=total_work//2, threshold=threshold),
                init_task_tree(total_work=total_work-total_work//2, threshold=threshold)
            ])


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
    with open(file_name) as file:
        logs = json.load(file)

    tasks = [
        Task(
            l["end_time"] - l["start_time"],
            [],
            children_id = l["children"],
            task_id = i
        )
        for (i, l) in enumerate(logs) ]

    #for task_indix in range(len(tasks)):
    #    current_task = Task(
    #        tasks[task_indix]["end_time"]-tasks[task_indix]["start_time"],
    #        [], children_id=tasks[task_indix]["children"], task_id=task_indix)

    #    tasks_list.append(current_task)

    return update_dependencies(tasks)


def display_DAG(DAG, level="", level_num=0):
    DAG.display()
    level_num = level_num + 1
    level = level + "--"
    print(level_num, level, end='')
    for child in DAG.children:
        display_DAG(child, level=level, level_num=level_num)


#All_tasks = read_task_tree_from_json("../tasks_file/merge_sort.json")
#print(All_tasks)
#DAG = init_task_tree(file_name="../tasks_file/merge_sort.json" )

#display_DAG(DAG)




