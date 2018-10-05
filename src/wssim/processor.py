#!/usr/bin/env python3.5
"""
the processor module provides a Processor class
holding processors states for the simulation.
"""
import wssim
from collections import deque
from wssim.events import IdleEvent, StealAnswerEvent, StealRequestEvent
from wssim.task import DAG_task, Divisible_load_task, adaptative_task

class Processor:
    """
    class represent Processor with its number, work and the current time
    number : number of processor
    work : the load of work in this processor
    Simulator : pointer to the Simulator
    current_time : the current time in the simulator
    network_time : network is in use until this time, if != 0 the network
    is used
    """
    speed = 1  # speed of all processors

    def __init__(self, number, cluster, simulator):
        self.number = number
        self.simulator = simulator
        self.current_time = 0
        self.network_time = 0  # network is in use until this time
        self.current_task = None
        self.cluster = cluster
        self.tasks = deque()

    def reset(self, first_task=None):
        """
        reset all counters. initialize work with given value.
        """
        self.current_time = 0
        self.network_time = 0
        self.current_task = None
        self.tasks = deque()
        if first_task is not None:
            self.current_task = first_task
            self.current_task.start_time = 0
            self.simulator.steal_info["W0"] = self.current_task.total_work()
            self.current_task.update_json_data(self.simulator.json_data, time=0, processor_number=self.number)
            self.simulator.add_event(IdleEvent(
                self.current_task.work//self.speed, self))
        else:
            self.simulator.add_event(IdleEvent(0, self))

    def __hash__(self):
        return hash(self.number)

    def __eq__(self, other):
        return self.number == other.number

    def display(self):
        """
        display processor info
        """
        nom  = "P" + str(self.number)

        print(nom, self.tasks)

    def get_part_of_work_if_exist(self, stealer):
        """
        methode return half of work.
        if we use work : return new half of work if exist in new task and
        update current task. return None if there's no work
        if we use tasks, popleft task and return it if there's tasks,
        else, return None
        """
        if self.tasks:
            return self.tasks.popleft()
        elif self.current_task:

            if self.cluster == stealer.cluster:
                granularity = self.simulator.topology.local_granularity
            else:
                granularity = self.simulator.topology.remote_granularity

            splitting_result = \
                    self.current_task.split_work(
                            self.current_time,
                            granularity,
                            json_data=self.simulator.json_data
                            )

            if splitting_result:
                idle_time, created_task, reduce_work = splitting_result
                self.simulator.total_work += reduce_work
                self.simulator.add_event(IdleEvent(idle_time, self))
                return created_task

    def answer_steal_request(self, stealer):
        """
        update current local time.
        if work left and not using network and update local work.
        update events in simulator.
        """
        self.current_time = self.simulator.time
        reply_time = self.simulator.communication_end_time(self, stealer)
        if __debug__:
            if self.simulator.log_file is not None:
                self.simulator.logger.end_communication(stealer, self, "WReq")

        if self.current_time >= self.network_time:
            # we can use network and we have enough work to send
            stolen_task = self.get_part_of_work_if_exist(stealer)
            if stolen_task is not None:
                if self.cluster == stealer.cluster:
                    self.simulator.steal_info["SIWR"] += 1
                    self.simulator.steal_info["WI"] += stolen_task.total_work()
                else:
                    self.simulator.steal_info["SEWR"] += 1
                    self.simulator.steal_info["WE"] += stolen_task.total_work()
                    if stealer.cluster == 1:
                        self.simulator.steal_info["W1"] += stolen_task.total_work()
                        self.simulator.steal_info["W0"] -= stolen_task.total_work()
                    else:
                        self.simulator.steal_info["W1"] -= stolen_task.total_work()
                        self.simulator.steal_info["W0"] += stolen_task.total_work()


                if not self.simulator.topology.is_simultaneous:
                    self.network_time = reply_time

                if __debug__:
                    if self.simulator.log_file is not None:
                        self.simulator.logger.push_processor_state(
                            self, new_state="Sending")
                        stealer.simulator.logger.update_processor_state(
                            stealer, new_state="Receiving")
                        self.simulator.logger.sub_work(self, stolen_task.work)
                        self.simulator.logger.add_work(
                            stealer, stolen_task.work)
        else:
            stolen_task = None

        self.simulator.add_event(
            StealAnswerEvent(reply_time, stealer, self, stolen_task)
        )

        if __debug__:
            if self.simulator.log_file is not None:
                self.simulator.logger.start_communication(
                    self, stealer, data="Response")

    def idle_event(self):
        """
        update time, start stealing.
        """
        self.current_time = self.simulator.time
        if self.current_task:
            assert self.current_task.finishes_at(self.current_time, self.speed)
            self.simulator.total_work -= self.current_task.work
            ready_tasks = self.current_task.end_execute_task(self.simulator.json_data, self.current_time, self.number)
            #print("P",self.number, "executing tasks : ", self.current_task.id, "(", self.current_task.work, ")" )
            #update_tasks_on_json(self.simulator.json_data, self.current_task, self.current_time, self.number)
            self.tasks.extend(ready_tasks)
            self.current_task = None
            if self.tasks:
                self.current_task = self.tasks.pop()
                while self.current_task.work == 0:
                    self.tasks.extend(self.current_task.end_execute_task(self.simulator.json_data, self.current_time, self.number))
                    assert self.tasks
                    #update_tasks_on_json(self.simulator.json_data, self.current_task, self.current_time, self.number)
                    self.current_task = self.tasks.pop()

                if self.cluster == 0:
                    self.simulator.steal_info["W0"] += self.current_task.total_work()
                else:
                    self.simulator.steal_info["W1"] += self.current_task.total_work()

                self.current_task.start_time = self.current_time
                becoming_idle_time = self.current_time + \
                self.current_task.work//self.speed
                assert self.current_task.work >= self.speed
                self.simulator.add_event(IdleEvent(becoming_idle_time, self))
                if __debug__:
                    if self.simulator.log_file is not None:
                        self.simulator.logger.update_processor_state(
                            self, new_state="Executing")

        if self.current_task is None:
            self.start_stealing()
            if __debug__:
                if self.simulator.log_file is not None:
                    self.simulator.logger.update_processor_state(
                        self, new_state="Stealing")

    def start_stealing(self):
        """
        start stealing, update simulator.
        """
        # victim = self.simulator.random_victim_not(self.number)
        self.simulator.rm_active_processor(self)
        victim = self.simulator.processors[
            self.simulator.topology.select_victim_not(self.number)
        ]
        steal_time = self.simulator.communication_end_time(self, victim)
        self.simulator.add_event(
            StealRequestEvent(steal_time, self, victim)
        )
        if self.cluster == victim.cluster:
            self.simulator.steal_info["IWR"] += 1
        else:
            self.simulator.steal_info["EWR"] += 1
        if __debug__:
            if self.simulator.log_file is not None:
                self.simulator.logger.start_communication(self, victim,
                                                          "WReq")

    def steal_answer(self, stolen_task, victim):
        """
        we receive an answer from steal request.
        """
        self.current_time = self.simulator.time
        #assert not self.tasks
        if stolen_task is None:
            # still no work, steal again
            self.start_stealing()
        else:
            self.current_task = stolen_task
            #TODO: repetition
            while self.current_task.work == 0:
                self.tasks.extend(self.current_task.end_execute_task(self.simulator.json_data, self.current_time, self.number))
                assert self.tasks
                #update_tasks_on_json(self.simulator.json_data, self.current_task, self.current_time, self.number)
                self.current_task = self.tasks.pop()
            assert self.current_task.work
            #update_tasks_on_json(self.simulator.json_data, self.current_task, self.current_time, self.number)
            self.simulator.steal_info["W0"] += stolen_task.total_work()
            self.current_task.start_time = self.current_time
            becoming_idle_time = self.current_time + \
                self.current_task.work//self.speed
            self.simulator.add_event(IdleEvent(becoming_idle_time, self))
            self.simulator.add_active_processor(self)

            if __debug__:
                if self.simulator.log_file is not None:
                    self.simulator.logger.update_processor_state(
                        self, new_state="Executing")
                    self.simulator.logger.pop_processor_state(victim)

        if __debug__:
            if self.simulator.log_file is not None:
                self.simulator.logger.end_communication(victim, self,
                                                        data="Response")

























