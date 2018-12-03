"""
the task module provides a Task class
holding work of task and list of its children for the simulation.
"""
from copy import deepcopy
import json
import wssim
from math import ceil, floor, log2, sqrt


class Task:
    """
    class represent Task with its work, list of children.
    work : work of tasks, task is virtual if work=0
    childrens : list of dependent tasks
    """
    tasks_number = 0
    remaining_tasks = 0

    def __init__(self, task_size, task_type, task_id=None):
        self.id = Task.tasks_number
        self.task_size = task_size
        self.start_time = 0
        self.children = []
        Task.remaining_tasks += 1
        Task.tasks_number += 1
        self.type = task_type

    def set_work_size(self, task_size):
        """
        update task size
        """
        self.task_size = task_size

    def get_task_size(self):
        """
        returns task size
        """
        return self.task_size

    def get_computed_work(self, current_time):
        """
        get the work done at this instance
        """
        return current_time - self.start_time

    def get_work(self):
        """
        method redefined in children class
        """
        return

    def finishes_at(self, finish_time, processor_speed):
        """
        compute if we finish at given time with given speed
        """
        return (finish_time - self.start_time) *\
                processor_speed == self.get_work()

    def update_graph_data(self, graph, current_time=0, processor_number=0):
        """
        update json data with the current tasks
        if the task does't exist, insert it
        else update the information
        """
        info = dict()
        info["id"] = self.id
        if hasattr(self, "children"):
            info["children"] = [child.id for child in self.children]
        info["thread_id"] = processor_number
        info["end_time"] = current_time * wssim.SVGTS
        info["start_time"] = self.start_time * wssim.SVGTS

        assert self.start_time * wssim.SVGTS == info["start_time"]
        info["work"] = [self.type, self.get_work() * wssim.SVGTS]
        graph.append(info)

    def end_execute_task(self, graph, current_time, processor_number):
        """
        In all cases, we need to update the task info on the graph
        """
        self.update_graph_data(graph, current_time=current_time,
                               processor_number=processor_number)
        Task.remaining_tasks -= 1


class DivisibleLoadTask(Task):
    """
    class for divisible load tasks
    """

    def __init__(self, task_size):
        super().__init__(task_size, 0)
        self.children = []

    def get_work(self):
        """
        returns work wish equal task size
        """
        return self.task_size

    def split_work(self, current_time, granularity, graph=None):
        """
        cut task in two if we have enough remaining work
        update update the work on the current task
        return new Divisible load task
        """
        computed_work = self.get_computed_work(current_time)
        remaining_work = self.get_work() - computed_work
        assert remaining_work >= 0
        my_share = remaining_work//2
        if my_share > granularity:
            self.set_work_size(computed_work + my_share)
            other_share = remaining_work - my_share

            new_child = DivisibleLoadTask(other_share)
            self.children.append(new_child)

            return current_time + my_share, new_child, 0

    def end_execute_task(self, graph, current_time, processor_number):
        """
        return empty list because Divisible load task does't have childre
        """
        super().end_execute_task(graph, current_time, processor_number)
        return []


class DagTask(Task):
    """
    class for divisible load tasks
    """

    def __init__(self, task_size, task_type, work_for_size=lambda size: size,
                 task_id=None):

        super().__init__(task_size, task_type)
        if task_id:
            self.id = task_id
        self.children = []
        self.dependent_tasks_number = 0
        self.work_for_size = work_for_size

    def get_work(self):
        """
        get work based on work_for_size function
        """
        return self.work_for_size(self.task_size)

    def split_work(self, current_time, granularity, graph=None):
        """
        unsplited tasks, return None
        """
        return None

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


class AdaptiveTask(Task):
    """
    class for the adaptive tasks that could be divided
    when the owner processor receives a steal
    """

    def __init__(self, task_size, granularity, task_type, reduction_tasks_factory, work_for_size, reduce_for_size):

        super().__init__(task_size, task_type)
        self.children = []
#                 at which time is the task started
        self.reduction_tasks_factory = reduction_tasks_factory
        self.work_for_size = work_for_size
        self.reduce_for_size = reduce_for_size
        self.granularity = granularity
#                 it will be intialised when we initialise tasks
        self.completed_size = 0


        #self.log_init_blk()
        self.log_init_blk(wssim.GEOM_BLOCK_NUMBER)
        #self.best_init_blk()
        #self.best_init_blk(wssim.GEOM_BLOCK_NUMBER)


    def log_init_blk(self, geo_blk_number=None):
        """
        """
        self.initial_block_size_threshold = log2(self.task_size)
        self.initial_block_size = init_blk_size(self.initial_block_size_threshold, self.task_size)
        # self.initial_block_size = round(self.initial_block_size_threshold)
        if geo_blk_number is None:
            self.best_geo_blk_number = log2(sqrt(self.task_size * wssim.INIT_TASK_COST) / log2(self.task_size))
        else:
            self.best_geo_blk_number = geo_blk_number
    #    print("size:{} initial_block_size:{} self.best_geo_blk_number:{}"
    #          .format(self.task_size, self.initial_block_size,
    #                  self.best_geo_blk_number))

    def best_init_blk(self, geo_blk_number=None):
        """
        """
        self.initial_block_size_threshold = sqrt(self.task_size * wssim.INIT_TASK_COST)
        #self.initial_block_size = init_blk_size(self.initial_block_size_threshold, self.task_size)
        self.initial_block_size = round(self.initial_block_size_threshold)
        if geo_blk_number is None:
            self.best_geo_blk_number = 0
        else:
            self.best_geo_blk_number = geo_blk_number

    #    print("size:{} initial_block_size:{} self.best_geo_blk_number:{}"
    #          .format(self.task_size, self.initial_block_size,
    #                  self.best_geo_blk_number))


    def get_work(self):
        """
        get work based on work_for_size function
        """

        work = 0
        current_block_number = 0
        remaining_size = self.task_size
        while remaining_size > 0:
            current_block_size = \
                    min(block_size(self.initial_block_size,
                                   current_block_number, self.best_geo_blk_number),
                        remaining_size)
            work += self.work_for_size(current_block_size)
            completed_size = self.task_size - remaining_size + self.completed_size
            if completed_size:
                work += self.reduce_for_size(completed_size, current_block_size)
            remaining_size -= current_block_size
            current_block_number += 1
        return int(work)

    def finishes_at(self, finish_time, processor_speed):
        """
        compute if we finish at given time with given speed
        """
        return (finish_time - self.start_time)\
                * processor_speed == self.get_work()

    def stop_task(self, current_time):
        """
        the task would be executed by blocks.
        at each time we can get the current block.
        this fonction returns time to finish the current blocks.
        it based on the function get_block_size
        """
        current_block_number = 0
        task_size = 0
        task_end_time = self.start_time
        remaining_size = self.task_size
        while current_time > task_end_time:
            current_block_size = min(block_size(self.initial_block_size, current_block_number, self.best_geo_blk_number),
                                     remaining_size)
            current_block_work = self.work_for_size(current_block_size)
            completed_size = self.task_size - remaining_size + self.completed_size
            if completed_size:
                current_block_work += self.reduce_for_size(completed_size, current_block_size)
            remaining_size -= current_block_size
            task_size += current_block_size
            task_end_time += current_block_work
            current_block_number += 1


        return task_end_time, task_size

    def split_tasks_with_waiting_time(self, left_size, right_size,
                                      waiting_time, graph):
        """
        split task and return all generated tasks
        """

        left_child = AdaptiveTask(left_size, self.granularity, self.type,
                                  self.reduction_tasks_factory,
                                  self.work_for_size, self.reduce_for_size)
        waiting_task = DagTask(waiting_time, 1)

        right_child = AdaptiveTask(right_size, self.granularity, self.type,
                                   self.reduction_tasks_factory,
                                   self.work_for_size, self.reduce_for_size)

        reduce_task = self.reduction_tasks_factory(left_size,
                                                   right_size)


        reduce_task.children = self.children
        waiting_task.children = [right_child]

        left_child.children = [reduce_task]
        right_child.children = [reduce_task]

        left_child.dependent_tasks_number = 1
        waiting_task.dependent_tasks_number = 0
        right_child.dependent_tasks_number = 1
        reduce_task.dependent_tasks_number = 2


        return left_child, right_child, waiting_task, reduce_task

    def split_work(self, current_time, granularity, graph=None):
        """
        unsplited tasks, return None
        """
        end_time, current_task_size = self.stop_task(current_time)
        waiting_time = ceil(end_time - current_time)
        # a voire comment on va le calculer
        remaining_size = self.task_size - current_task_size
        my_share = remaining_size//2

        if my_share <= self.initial_block_size or current_task_size == 0:
            return None

        # assert current_task_size == self.task_size

        l_child, r_child, waiting_task, reduce_task = \
                self.split_tasks_with_waiting_time(my_share,
                                                   remaining_size - my_share,
                                                   waiting_time,
                                                   graph
                                                  )

        #add_tasks_to_json([l_child, waiting_task, r_child, reduce_task], graph)
        #graph[self.id]["children"] = \
        #        [l_child.id, waiting_task.id]
        self.set_work_size(current_task_size)
        self.children = [l_child, waiting_task]

        l_child.completed_size = self.completed_size + current_task_size

        return self.start_time + self.get_work(), \
                waiting_task, \
                reduce_task.get_work()

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

    def update_graph_data(self, graph,
                          current_time=0, processor_number=0):
        """
        update json data with the current tasks
        if the task does't exist, insert it
        else update the information
        """
        work = 0
        current_block_number = 0
        remaining_size = self.task_size
        child_id = self.id
        virtual_children = list()
        while remaining_size > 0:
            child = dict()
            if work == 0:
                child["id"] = self.id
            else:
                child["id"] = Task.tasks_number
                Task.tasks_number += 1
            child["start_time"] = (self.start_time + int(work)) * wssim.SVGTS
            child["children"] = [ Task.tasks_number]
            current_block_size = \
                    min(block_size(self.initial_block_size,
                                   current_block_number, self.best_geo_blk_number),
                        remaining_size)
            work += floor(self.work_for_size(current_block_size))
            child["work"] = [self.type, floor(self.work_for_size(current_block_size)) * wssim.SVGTS ]
            completed_size = self.task_size - remaining_size + self.completed_size
            if completed_size:
                work += self.reduce_for_size(completed_size, current_block_size)
                child["work"][1]  += self.reduce_for_size(completed_size, current_block_size) * wssim.SVGTS
            child["end_time"] = child["start_time"] + child["work"][1]
            child["thread_id"] = processor_number
            remaining_size -= current_block_size
            current_block_number += 1
            virtual_children.append(child)

        virtual_children[len(virtual_children)-1]["children"] = [child.id for child in self.children]
        #assert work == self.get_work()
        graph.extend(virtual_children)
        #for child in virtual_children:
        #    graph.append(child)



def init_blk_size(initial_block_size_threshold, task_size):
    """
    """
    block_number = floor(
        log2(task_size / initial_block_size_threshold + 1)
        - 1)

    initial_block_size = ceil(task_size / (2**(block_number + 1) - 1))
    return initial_block_size


def block_size(initial_block_size, block_number, geo_blk_number):
    """
    return block size based on its number.
    we use "Golden ratio" to compute the size in each block
    """
    if block_number <  geo_blk_number:
        return ceil(initial_block_size * wssim.BLOCK_FACTOR**block_number)
    else:
        return ceil(initial_block_size * wssim.BLOCK_FACTOR ** geo_blk_number)

def init_task_tree(total_work=0, threshold=0, file_name=None, task_id=0):
    """
    create the task tree recursively
    """
    if file_name is not None:
        tasks, work, depth, logs = read_task_tree_from_json(file_name)
        return tasks[0], work, depth, logs
    else:
        # if total_work//2 < threshold:
        if total_work <= threshold:
            current_task = DagTask(total_work, 1)
            current_task.dependent_tasks_number = 1
            return current_task
        else:
            if total_work//2 <= threshold:

                current_task = DagTask(0,1)
                l_child = init_task_tree(total_work=threshold,
                                         threshold=threshold)
                r_child = init_task_tree(total_work=total_work-threshold,
                                         threshold=threshold)

                current_task.children = [l_child, r_child]
                current_task.dependent_tasks_number = 1

                return current_task
            else:
                current_task = DagTask(0,1)
                l_child = init_task_tree(total_work=total_work//2,
                                         threshold=threshold)
                r_child = init_task_tree(total_work=total_work-total_work//2,
                                         threshold=threshold)

                current_task.children = [l_child, r_child]
                current_task.dependent_tasks_number = 1
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
            tasks[children_id].dependent_tasks_number =\
                    tasks[children_id].dependent_tasks_number + 1
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

    for task_index, task in enumerate(logs["tasks_logs"]):
        current_task = DagTask(
            task["end_time"]-task["start_time"], 1, task_id=task_index )
        current_task.children_id = task["children"]
        current_task.start_time = task["start_time"]
        tasks.append(current_task)

    work = compute_work(tasks)
    tasks = update_dependencies(tasks)
    depth = compute_depth(tasks)

    return tasks, work, depth, logs


def display_DAG(DAG, level="", level_num=0):
    print("T:", DAG.id, "(", DAG.get_work(), ")")
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
    tasks_ids.sort(key=lambda i: tasks[i].start_time)
    # , reversed=True)
    tasks_ids.reverse()

    for task_id in tasks_ids:
        task = tasks[task_id]
        if task.children:
            depths[task_id] = task.get_work() + max(depths[c.id]
                                                    for c in task.children)
        else:
            depths[task_id] = task.get_work()

    return depths[0]


def compute_work(tasks):
    """
    compute the total work of the graph of given tasks.
    """
    return sum(t.get_work() for t in tasks)


def get_reduce_work(left_child, right_child):
    """
    methode to compute the reduce work
    based on the work of the two dependet tasks
    """
    return (left_child.work + right_child.work)//8

