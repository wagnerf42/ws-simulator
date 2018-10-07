#!/usr/bin/env python3.5
"""
the task module provides a Task class
holding work of task and list of its children for the simulation.
"""
from copy import deepcopy
import json
import wssim


class Task:
    """
    class represent Task with its work, list of children.
    work : work of tasks, task is virtual if work=0
    childrens : list of dependent tasks
    """
    tasks_number = 0
    remaining_tasks = 0
    def __init__(self, work, task_id=None):
        if task_id:
            self.id = task_id  # id of task will be update when we intialise tasks
        else:
            self.id = Task.tasks_number
        self.work = work

        Task.remaining_tasks += 1
        Task.tasks_number += 1

    def finishes_at(self, finish_time, processor_speed):
        """
        compute if we finish at given time with given speed
        """
        return (finish_time - self.start_time) * processor_speed == self.work

    def update_graph_data(self, graph, time=0, processor_number=0):
        """
        update json data with the current tasks
        if the task does't exist, insert it
        else update the information
        """
        if get_last_id_from_the_json_data(graph) >= self.id:
            graph[self.id]["id"] = self.id
            graph[self.id]["thread_id"] = processor_number
            graph[self.id]["end_time"] = time * wssim.UNIT
            graph[self.id]["start_time"] = (time - self.work) * wssim.UNIT
                # besoin speed
        else:
            info = dict()
            info["id"] = self.id
            if hasattr(self, "children"):
                info["children"] = [child.id for child in self.children]

            graph.insert(self.id, info)

    def end_execute_task(self, graph, current_time, processor_number):
        """
        In all cases, we need to update the task info on the graph
        """
        self.update_graph_data(graph, time=current_time, processor_number=processor_number)
        Task.remaining_tasks -= 1


class Divisible_load_task(Task):
    """
    class for divisible load tasks
    """

    def __init__(self, work):
        super().__init__(work)
        self.children = []

    def total_work(self):
        """
        returns work
        """
        return self.work

    def split_work(self, current_time, granularity, graph=None):
        """
        cut task in two if we have enough remaining work
        update update the work on the current task
        return new Divisible load task
        """
        computed_work = current_time - self.start_time
        remaining_work = self.work - computed_work
        assert remaining_work >= 0
        my_share = remaining_work//2
        if my_share > granularity:
            self.work = computed_work + my_share
            other_share = remaining_work - my_share

            new_child = Divisible_load_task(other_share)
            new_child.update_graph_data(graph)

            graph[self.id]["children"].append(new_child.id)

            return current_time + my_share, new_child, 0

    def end_execute_task(self, graph, current_time, processor_number):
        """
        return empty list because Divisible load task does't have childre
        """
        super().end_execute_task(graph, current_time, processor_number)
        return []


class DAG_task(Task):
    """
    class for divisible load tasks
    """

    def __init__(self, work, task_id=None):

        super().__init__(work, task_id=task_id)
        self.children = []
#                 it will be intialised when we initialise tasks
        self.dependent_tasks_number = 0

    def total_work(self):
        """
        returns work
        """
#       return sum(child.total_work() for child in self.children)
        return self.work

    def split_work(self, current_time, granularit, graph=None):
        """
        unsplited tasks, return None
        """
        return None

    def end_execute_task(self, graph, current_time, processor_number):
        """
        return all children tasks
        """
        super().end_execute_task(graph, current_time, processor_number  )
        ready_children = []
        # reversed because next task to execute should be pushed last
        for child in reversed(self.children):
            child.update_dependent_task()
            if child.dependent_tasks_number == 0:
                ready_children.append(child)
        return ready_children

    def update_dependent_task(self):
        """
        Decrease the number of dependents task when it's finished
        When the number of dependent tasks is 0, we return the tasks with true.
        """
        self.dependent_tasks_number -= 1


class Adaptive_task(Task):
    """
    class for the adaptive tasks that could be divided
    when the owner processor receives a steal
    """

    def __init__(self, work, reduction_tasks_factory):

        super().__init__(work)
        self.children = []
#                 at which time is the task started
        self.reduction_tasks_factory = reduction_tasks_factory
#                 it will be intialised when we initialise tasks

    def total_work(self):
        """
        returns work
        """
#       return sum(child.total_work() for child in self.children)
        return self.work

    def get_waiting_time(self, current_time):
        """
        get the remainder time to finish the current blocks
        """
        return 100

    def split_tasks_with_waiting_time(self, left_work, right_work,
                                      waiting_time, graph):
        """

        """

        left_child = Adaptive_task(left_work,
                                   self.reduction_tasks_factory)
        waiting_task = DAG_task(waiting_time)

        right_child = Adaptive_task(right_work,
                                    self.reduction_tasks_factory)

        reduce_task = self.reduction_tasks_factory(left_child.work,
                                                   right_child.work)

        reduce_task.children = self.children
        waiting_task.children = [right_child]

        left_child.children = [reduce_task]
        right_child.children = [reduce_task]


        left_child.dependent_tasks_number=1
        waiting_task.dependent_tasks_number=0
        right_child.dependent_tasks_number=1
        reduce_task.dependent_tasks_number=2



        # reduce_work = get_reduce_work(left_child, right_child)
        # reduce_task = DAG_task(reduce_work, self.children,
        #                        dependent_tasks_number=2)
        # update current_tasks
        return left_child, right_child, waiting_task, reduce_task


    def split_work(self, current_time, granularity, graph=None):
        """
        unsplited tasks, return None
        """
        computed_work = current_time - self.start_time
        waiting_time = self.get_waiting_time(current_time)
        # a voire comment on va le calculer
        remaining_work = self.work - computed_work - waiting_time
        my_share = remaining_work//2

        assert remaining_work + waiting_time >= 0

        if my_share < granularity:
            return None

        l_child, r_child, waiting_task, reduce_task = \
                self.split_tasks_with_waiting_time(my_share,
                                                   remaining_work - my_share,
                                                   waiting_time,
                                                   graph
                                                   )
        add_tasks_to_json([l_child, waiting_task, r_child, reduce_task], graph)
        graph[self.id]["children"] = \
                [l_child.id, waiting_task.id]

        self.work = computed_work + waiting_time
        self.children = [l_child]
        return current_time + waiting_time, waiting_task,\
                waiting_time + reduce_task.work

    def end_execute_task(self, graph, current_time, processor_number):
        """
        return all children tasks
        """
        super().end_execute_task(graph, current_time, processor_number)
        ready_children = []
        # reversed because next task to execute should be pushed last
        for child in reversed(self.children):
            child.update_dependent_task()
            if child.dependent_tasks_number == 0:
                ready_children.append(child)
        return ready_children

    def update_dependent_task(self):
        """
        Decrease the number of dependents task when it's finished
        When the number of dependent tasks is 0, we return the tasks with true.
        """
        self.dependent_tasks_number -= 1



def get_last_id_from_the_json_data(graph):
    """
    get the last_id from thr json data
    """
    return len(graph) - 1


def add_tasks_to_json(tasks, graph):
    """
    add tasks list to Json file
    """
    for task in tasks:
        task.update_graph_data(graph)

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
            current_task = DAG_task(total_work, task_id=task_id)
            current_task.dependent_tasks_number=1
            return current_task
        else:
            if (total_work//2 <= threshold):

                l_child = init_task_tree(total_work=threshold  , threshold=threshold, task_id=(task_id*2 + 1))
                r_child = init_task_tree(total_work=total_work-threshold, threshold=threshold, task_id=(task_id*2 + 2))

                current_task = DAG_task(0, task_id=task_id)
                current_task.children = [l_child, r_child]
                current_task.dependent_tasks_number=1

                return current_task
            else:

                l_child = init_task_tree(total_work=total_work//2, threshold=threshold, task_id=(task_id*2 + 1))
                r_child = init_task_tree(total_work=total_work-total_work//2, threshold=threshold, task_id=(task_id*2 + 2))

                current_task = DAG_task(0, task_id=task_id)
                current_task.children = [l_child, r_child]
                current_task.dependent_tasks_number=1
                return current_task



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

#for children_id in task.children_id:
#            tasks[children_id].dependent_tasks_number = tasks[children_id].dependent_tasks_number + 1
#            task.children.append(tasks[children_id])



def read_task_tree_from_json(file_name):
    """
    Read task from json file
    stor tasks in list
    """
    tasks = []
    with open(file_name) as file:
        logs = json.load(file)

    for task_index, task in enumerate(logs["tasks_logs"]):
        current_task = DAG_task(
            task["end_time"]-task["start_time"], task_id=task_index)
        current_task.children_id = task["children"]
        current_task.start_time = task["start_time"]
        tasks.append(current_task)

    work = compute_work(tasks)
    tasks = update_dependencies(tasks)
    depth = compute_depth(tasks)

    return tasks, work, depth, logs


def display_DAG(DAG, level="", level_num=0):
    print("T:",DAG.id, "(", DAG.work ,")")
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
            depths[task_id] = task.total_work() + max(depths[c.id] for c in task.children)
        else:
            depths[task_id] = task.total_work()

    return depths[0]


def compute_work(tasks):
    """
    compute the total work of the graph of given tasks.
    """
    return sum(t.total_work() for t in tasks)

def get_reduce_work(left_child, right_child):
    """
    methode to compute the reduce work based on the work of the two dependet tasks
    """
    return ( left_child.work + right_child.work )//8

