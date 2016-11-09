#!/usr/bin/env python3
"""
the task module provides a Task class
holding work of task and list of its children for the simulation.
"""
from copy import deepcopy




class Task:
    """
    class represent Task with its work, list of children.
    work : work of tasks, task is virtual if work=0
    childrens : list of dependent tasks
    """

    def __init__(self, work, children):
        self.work = work
        self.children = children
        self.start_time = 0  # at which time is the task started

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
        return self.children

    def finishes_at(self, finish_time, processor_speed):
        """
        compute if we finish at given time with given speed
        """
        return (finish_time - self.start_time) * processor_speed == self.work

    def display(self, depth=0):
        """
        display tasks with work and its childrens
        """
        print("  "*depth, "[")
        print("  "*depth, id(self), " ", self.work)
        for child in self.children:
            child.display(depth+1)
        print("  "*depth, "]")



def init_task_tree(total_work, threshold):
    """
    create the task tree recursively
    """
    if total_work//2 < threshold:
        return Task(total_work, [])
    else:
        return Task(0, [
            init_task_tree(total_work//2, threshold),
            init_task_tree(total_work-total_work//2, threshold)
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
