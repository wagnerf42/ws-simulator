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

    def __init__(self, task_id, work, start_time):
        self.id = task_id  # id of task will be update when we intialise tasks
        self.work = work
        self.start_time = start_time

    def finishes_at(self, finish_time, processor_speed):
        """
        compute if we finish at given time with given speed
        """
        return (finish_time - self.start_time) * processor_speed == self.work

    def update_json_data(self, json_data, time=0, processor_number=0):
        """
        update_json_data with the current tasks
        if the task does't exist, insert it
        else update the information
        """

        if "tasks_logs" in json_data.keys():
            if get_last_id_from_the_json_data(json_data) >= self.id:
                json_data["tasks_logs"][self.id]["id"] = self.id
                json_data["tasks_logs"][self.id]["thread_id"] = processor_number
                json_data["tasks_logs"][self.id]["end_time"] = time * wssim.UNIT
                json_data["tasks_logs"][self.id]["start_time"] = (time - self.work) * wssim.UNIT
                # besoin speed
            else:
                info = dict()
                info["id"] = self.id
                info["start_time"] = 0
                info["end_time"] = 0
                info["thread_id"] = 0
                info["children"] = [child.id for child in self.children]

                json_data["tasks_logs"].insert(self.id, info)
        else:
            info = dict()
            info["id"] = self.id
            info["start_time"] = 0
            info["end_time"] = 0
            info["thread_id"] = processor_number
            info["children"] = [child.id for child in self.children]
            json_data["tasks_logs"] = [info]


class Divisible_load_task(Task):
    """
    class for divisible load tasks
    """

    def __init__(self, work, start_time=0, task_id=0):
        super().__init__(task_id, work, start_time)

    def total_work(self):
        """
        returns work
        """
        return self.work

    def update_json_data(self, json_data, time=0, processor_number=0):
        """
        """
        info = dict()
        info["id"] = self.id
        info["start_time"] = 0
        info["end_time"] = 0
        info["thread_id"] = processor_number
        info["children"] = []
        json_data["tasks_logs"] = [info]


    def split_work(self, current_time, granularity, json_data=None):
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
            return current_time + my_share, \
                    Divisible_load_task(other_share), 0

    def end_execute_task(self, json_data, current_time, processor_number):
        """
        return empty list because Divisible load task does't have childre
        """
        self.update_json_data(json_data, time=current_time, processor_number=processor_number)
        return []


class DAG_task(Task):
    """
    class for divisible load tasks
    """

    def __init__(self, work, children, children_id, task_id, start_time=0,
                 dependent_tasks_number=0):

        super().__init__(task_id, work, start_time)
        self.children = children
        self.children_id = children_id
        self.start_time = start_time
#                 at which time is the task started
        self.dependent_tasks_number = dependent_tasks_number
#                 it will be intialised when we initialise tasks

    def total_work(self):
        """
        returns work
        """
#       return sum(child.total_work() for child in self.children)
        return self.work

    def split_work(self, current_time, granularit, json_data=None):
        """
        unsplited tasks, return None
        """
        return None

    def end_execute_task(self, json_data, current_time, processor_number):
        """
        return all children tasks
        """
        ready_children = []
        self.update_json_data(json_data, time=current_time, processor_number=processor_number)
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


class adaptative_task(Task):
    """
    class for the adaptive tasks that could be divided
    when the owner processor receives a steal
    """

    def __init__(self, work, children=[], children_id=[], task_id=0, start_time=0,
            dependent_tasks_number=0):

        super().__init__(task_id, work, start_time)
        self.children = children
        self.children_id = children_id
        self.start_time = start_time
#                 at which time is the task started
        self.dependent_tasks_number = dependent_tasks_number
#                 it will be intialised when we initialise tasks

    def total_work(self):
        """
        returns work
        """
#       return sum(child.total_work() for child in self.children)
        return self.work

    def get_waiting_time(self, current_time, with_waiting_time):
        """
        get the remainder time to finish the current blocks
        """
        if with_waiting_time:
            return 100
        else:
            return 0

    def split_tasks_with_waiting_time(self, left_work, right_work, waiting_time, json_data):
        """
        """
        last_id = get_last_id_from_the_json_data(json_data)

        left_child = adaptative_task(left_work,
                                     task_id=(last_id + 1),
                                     dependent_tasks_number=1)
        right_child = adaptative_task(right_work,
                                      task_id=(last_id + 3),
                                      dependent_tasks_number=1)
        waiting_task = DAG_task(waiting_time, [right_child],
                               [right_child.id], task_id=(last_id+ 2),
                                dependent_tasks_number=0)

        reduce_work = get_reduce_work(left_child, right_child)
        reduce_task = DAG_task(reduce_work, self.children, self.children_id,
                               task_id=(last_id + 4),
                               dependent_tasks_number=2)

        left_child.children = [reduce_task]
        left_child.children_id = [reduce_task.id]

        right_child.children = [reduce_task]
        right_child.children_id = [reduce_task.id]

        # update current_tasks
        return left_child, right_child, waiting_task, reduce_task

    def split_tasks_without_waiting_time(self, left_work, right_work, waiting_time, json_data):
        """
        """
        last_id = get_last_id_from_the_json_data(json_data)

        left_child = adaptative_task(left_work,
                                     task_id=(last_id + 1),
                                     dependent_tasks_number=1)
        right_child = adaptative_task(right_work,
                                      task_id=(last_id + 2),
                                      dependent_tasks_number=1)

        reduce_work = get_reduce_work(left_child, right_child)
        reduce_task = DAG_task(reduce_work, self.children, self.children_id,
                               task_id=(last_id + 3),
                               dependent_tasks_number=2)

        left_child.children = [reduce_task]
        left_child.children_id = [reduce_task.id]

        right_child.children = [reduce_task]
        right_child.children_id = [reduce_task.id]

        # update current_tasks
        return left_child, right_child, reduce_task


    def split_work(self, current_time, granularity, json_data=None, with_waiting_time=True):
        """
        unsplited tasks, return None
        """
        computed_work = current_time - self.start_time
        waiting_time = self.get_waiting_time(current_time, with_waiting_time)
        # a voire comment on va le calculer
        remaining_work = self.work - computed_work - waiting_time
        my_share = remaining_work//2

        assert remaining_work + waiting_time >= 0

        if my_share < granularity:
            return None

        if with_waiting_time:
            l_child, r_child, waiting_task, reduce_task = \
                    self.split_tasks_with_waiting_time(
                            my_share,
                            remaining_work - my_share,
                            waiting_time,
                            json_data
                            )
            add_tasks_to_json([l_child, waiting_task, r_child, reduce_task], json_data)
            json_data["tasks_logs"][self.id]["children"] = \
                    [l_child.id, waiting_task.id]

            self.work = computed_work + waiting_time
            self.children = [l_child]
            self.children_id = [l_child.id]
            return current_time + waiting_time, waiting_task,\
                    waiting_time + reduce_task.work
        else:
            l_child, r_child, reduce_task = \
                    self.split_tasks_without_waiting_time(
                            my_share,
                            remaining_work - my_share,
                            waiting_time,
                            json_data
                            )
            add_tasks_to_json([l_child, r_child, reduce_task], json_data)
            json_data["tasks_logs"][self.id]["children"] = \
                    [l_child.id, r_child.id]

            self.work = computed_work + waiting_time
            self.children = [l_child]
            self.children_id = [l_child.id]
            return current_time, r_child, reduce_task.work

    def end_execute_task(self, json_data, current_time, processor_number):
        """
        return all children tasks
        """
        self.update_json_data(json_data, time=current_time, processor_number=processor_number)
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



def get_last_id_from_the_json_data(json_data):
    """
    get the last_id from thr json data
    """
    if "tasks_logs" in json_data.keys():
        return len(json_data["tasks_logs"]) - 1
    else:
        assert 1==2
        return 0


def add_tasks_to_json(tasks, json_data):
    """
    add tasks list to Json file
    """
    for task in tasks:
        task.update_json_data(json_data)

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
            return DAG_task(total_work, [], [], task_id, dependent_tasks_number=1)
        else:
            if (total_work//2 <= threshold):
                return DAG_task(0, [
                    init_task_tree(total_work=threshold  , threshold=threshold, task_id=(task_id*2 + 1)),
                    init_task_tree(total_work=total_work-threshold, threshold=threshold, task_id=(task_id*2 + 2))
                    ], [(task_id*2 + 1), (task_id*2 + 2)], task_id=task_id, dependent_tasks_number=1 )
            else:
                return DAG_task(0, [
                    init_task_tree(total_work=total_work//2, threshold=threshold, task_id=(task_id*2 + 1)),
                    init_task_tree(total_work=total_work-total_work//2, threshold=threshold, task_id=(task_id*2 +2))
                    ], [(task_id*2 + 1), (task_id*2 + 2)], task_id=task_id, dependent_tasks_number=1)


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
        current_task = DAG_task(
            task["end_time"]-task["start_time"],
            [], task["children"], task_index,
            start_time=task["start_time"])
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

def get_reduce_work(left_child, right_child):
    """
    methode to compute the reduce work based on the work of the two dependet tasks
    """
    return ( left_child.work + right_child.work )//8

