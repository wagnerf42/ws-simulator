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

    def end_execute_task(self):
        """
        return empty list because Divisible load task does't have childre
        """
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

    def end_execute_task(self):
        """
        return all children tasks
        """
        ready_children = []
        # reversed because next task to execute should be pushed last
        print("End of : T",self.id, "= ", self.work)
        for child in reversed(self.children):
            child.update_dependent_task()
            if child.dependent_tasks_number == 0:
                ready_children.append(child)
                print("ready_children : ", ready_children)
        return ready_children

    def update_dependent_task(self):
        """
        Decrease the number of dependents task when it's finished
        When the number of dependent tasks is 0, we return the tasks with true.
        """
        print(" update_dependent_task of T", self.id, " = ", self.dependent_tasks_number-1 )
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

    def split_work(self, current_time, granularity, json_data=None):
        """
        unsplited tasks, return None
        """
        computed_work = current_time - self.start_time
        waiting_time = 100  # a voire comment on va le calculer
        remaining_work = self.work - computed_work - waiting_time
        my_share = remaining_work//2

        assert remaining_work + waiting_time >= 0

        if my_share < granularity:
            return None

        last_id = get_last_id_from_the_json_data(self.id, json_data)
        print("last_id",last_id)

        left_child = adaptative_task(remaining_work//2,
                                     task_id=(last_id + 1),
                                     dependent_tasks_number=1)
        right_child = adaptative_task(remaining_work - remaining_work//2,
                                      task_id=(last_id + 3),
                                      dependent_tasks_number=1)

        # create the reduce tasks
        current_reduce = self.children

        reduce_work = get_reduce_work(left_child, right_child)
        reduce_task = DAG_task(reduce_work, self.children, self.children_id,
                               task_id=(last_id + 4),
                               dependent_tasks_number=2)

        left_child.children = [reduce_task]
        left_child.children_id = [reduce_task.id]

        right_child.children = [reduce_task]
        right_child.children_id = [reduce_task.id]

        # create the waited time
        waiting_task = DAG_task(waiting_time, [right_child],
                               [right_child.id], task_id=(last_id+ 2),
                               dependent_tasks_number=0)
        # update current_tasks
        self.work = computed_work + waiting_time
        self.children = [left_child]
        self.children_id = [left_child.id]


        if len(json_data) >= 1:
            add_tasks_to_json([left_child, right_child, waiting_task, reduce_task] , json_data)
            json_data["tasks_logs"][self.id]["children"] = [left_child.id, waiting_task.id]
            #json_data["tasks_logs"][self.id]["end_time"] = (json_data["tasks_logs"][self.id]["start_time"] + self.work ) * wssim.UNIT
            print("Updated", json_data["tasks_logs"][self.id])


        return current_time + waiting_time, waiting_task, reduce_work+waiting_time

    def end_execute_task(self):
        """
        return all children tasks
        """
        print("End of : T",self.id, "= ", self.work)
        ready_children = []
        # reversed because next task to execute should be pushed last
        for child in reversed(self.children):
            child.update_dependent_task()
            if child.dependent_tasks_number == 0:
                ready_children.append(child)
        [print("R_child of ", self.id, " is ", ready_child.id) for ready_child in ready_children]
        return ready_children

    def update_dependent_task(self):
        """
        Decrease the number of dependents task when it's finished
        When the number of dependent tasks is 0, we return the tasks with true.
        """
        print(" update_dependent_task of T", self.id, " = ", self.dependent_tasks_number-1 )
        self.dependent_tasks_number -= 1



def get_last_id_from_the_json_data(current_id, json_data):
    """
    get the last_id from thr json data
    """
    if len(json_data) >= 1:
        return len(json_data["tasks_logs"]) - 1
    else:
        return current_id * 4


def add_tasks_to_json(tasks, json_data):
    """
    add tasks list to Json file
    """
#   [print(task.id) for task in tasks]
    for task in tasks:
        info = dict()
        info["id"] = task.id
        info["start_time"] = 0
        info["end_time"] = 0
        info["thread_id"] = 0
        info["children"] = [child.id for child in task.children]
        json_data["tasks_logs"].insert(task.id, info)

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
            return DAG_task(total_work, [], [], task_id, dependent_tasks_number=1)
        else:
           # print("T", task_id , " -> T",(task_id*2 + 1) , " , T", (task_id*2 + 2))
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

def get_reduce_work(left_task, right_task):
    """
    methode to compute the reduce work based on the work of the two dependet tasks
    """
    return ( left_task.work + right_task.work )//3

