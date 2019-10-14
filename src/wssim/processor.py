"""
the processor module provides a Processor class
holding processors states for the simulation.
"""

#from random import randint
from collections import deque, defaultdict
from wssim.events import IdleEvent, StealAnswerEvent, StealRequestEvent

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
        self.stolen_task = None
        self.current_task = None
        self.cluster = cluster
        self.tasks = deque()
#        self.steal_configs = defaultdct(float)
#        self.steal_attempt_number = 0
#        self.steal_attempt_max = 1
#        self.successful_remote_steal = 0
#        self.successful_local_steal = 0
        #self.steal_attempt_max =  randint(6, 12)

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
            #self.current_task.update_graph_data(self.simulator.graph,
            #                                    current_time=0,
            #                                    processor_number=self.number)
            self.simulator.add_event(IdleEvent(
                self.current_task.get_work()//self.speed, self))
            self.simulator.steal_info["WI0"] += self.current_task.get_work()
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
        print("P{}".format(self.number), self.tasks)

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
                    self.current_task.split_work(self.current_time,
                                                 granularity,
                                                 remote_steal=(self.cluster != stealer.cluster),
                                                 graph=self.simulator.graph
                                                )


            if splitting_result:
                idle_time, created_task, reduce_work = splitting_result
                self.simulator.total_work += reduce_work
                self.simulator.add_event(IdleEvent(idle_time, self))
                return created_task
        return None

    def answer_steal_request(self, stealer):
        """
        update current local time.
        if work left and not using network and update local work.
        update events in simulator.
        """
        self.current_time = self.simulator.time
        reply_time = self.simulator.communication_end_time(self, stealer)
        self.simulator.steal_info["idle_time"] += \
            self.simulator.topology.distance(stealer.number, self.number)
        if __debug__:
            if self.simulator.log_file is not None:
                self.simulator.logger.end_communication(stealer, self, "WReq")
        if self.current_time >= self.network_time:
            # we can use network and we have enough work to send
            stolen_task = self.get_part_of_work_if_exist(stealer)
            if stolen_task is not None:
                if self.cluster == stealer.cluster:
                    self.simulator.steal_info["SIWR"] += 1
                    self.simulator.steal_info["WI"] += stolen_task.get_work()
                else:
                    self.simulator.steal_info["SEWR"] += 1
                    self.simulator.steal_info["WE"] += stolen_task.get_work()
                    if stealer.cluster == 0:
                        self.simulator.steal_info["WI1"] -= \
                            stolen_task.get_work()
                        self.simulator.steal_info["WI0"] += \
                            stolen_task.get_work()
                    if stealer.cluster == 1:
                        self.simulator.steal_info["WI0"] -= \
                            stolen_task.get_work()
                        self.simulator.steal_info["WI1"] += \
                            stolen_task.get_work()

                if not self.simulator.topology.is_simultaneous:
                    self.network_time = reply_time
                    if stolen_task.type == 1:
                        self.network_time += stolen_task.get_work()

                if __debug__:
                    if self.simulator.log_file is not None:
                        self.simulator.logger.push_processor_state(
                            self, new_state="Sending")
                        stealer.simulator.logger.update_processor_state(
                            stealer, new_state="Receiving")
                        self.simulator.logger.sub_work(self,
                                                       stolen_task.get_work())
                        self.simulator.logger.add_work(
                            stealer, stolen_task.get_work())
        else:
            stolen_task = None

        self.stolen_task = stolen_task
        self.simulator.add_event(
            StealAnswerEvent(reply_time, stealer, self, stolen_task)
        )

        if __debug__: #and self.cluster != stealer.cluster:
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
            if self.current_task.type == -1:
                self.simulator.steal_info["waiting_time"] += \
                        self.current_task.get_work()
            elif self.cluster == 0:
                self.simulator.steal_info["W0"] += \
                        self.current_task.get_work()
                self.simulator.steal_info["WI0"] -= \
                    self.current_task.get_work()
            else:
                self.simulator.steal_info["W1"] += \
                        self.current_task.get_work()
                self.simulator.steal_info["WI1"] -= \
                    self.current_task.get_work()

            self.simulator.total_work -= self.current_task.get_work()
            ready_tasks = self.current_task.end_execute_task(
                self.simulator.graph,
                self.current_time,
                self.number)
            self.tasks.extend(ready_tasks)
            self.current_task = None
            if self.tasks:
                self.current_task = self.tasks.pop()
                while self.current_task.get_work() == 0:
                    self.current_task.start_time = self.current_time
                    self.tasks.extend(self.current_task.end_execute_task(
                        self.simulator.graph,
                        self.current_time,
                        self.number))
                    assert self.tasks
                    self.current_task = self.tasks.pop()

                self.current_task.start_time = self.current_time
                becoming_idle_time = \
                    self.current_time + self.current_task.get_work()//self.speed
                assert self.current_task.get_work() >= self.speed
                self.simulator.add_event(IdleEvent(becoming_idle_time, self))
                if __debug__:
                    if self.simulator.log_file is not None:
                        self.simulator.logger.update_processor_state(
                            self, new_state="Executing")

        if self.current_task is None:
            self.start_stealing()
            #if __debug__:
            #    if self.simulator.log_file is not None:
            #        self.simulator.logger.update_processor_state(
            #            self, new_state="StealingE")

    def start_stealing(self):
        """
        start stealing, update simulator.
        """
        # victim = self.simulator.random_victim_not(self.number)
        self.simulator.rm_active_processor(self)
        victim = self.simulator.processors[
            self.simulator.topology.select_victim_not(self)
        ]
        steal_time = self.simulator.communication_end_time(self, victim)
        self.simulator.add_event(
            StealRequestEvent(steal_time, self, victim)
        )
        self.simulator.steal_info["idle_time"] += \
            self.simulator.topology.distance(victim.number, self.number)

        if self.cluster == victim.cluster:
            self.simulator.steal_info["IWR"] += 1
            self.simulator.Isteal_data[self.current_time] += 1
        else:
            self.simulator.steal_info["EWR"] += 1
            self.simulator.Esteal_data[self.current_time] += 1

        if __debug__:
            if self.simulator.log_file is not None:
                self.simulator.logger.start_communication(self, victim,
                                                          "WReq")
        if __debug__: 
            if self.simulator.log_file is not None:
                if self.cluster != victim.cluster:
                    self.simulator.logger.update_processor_state(
                        self, new_state="StealingE")
                else:
                    self.simulator.logger.update_processor_state(
                        self, new_state="Stealing")


    def steal_answer(self, stolen_task, victim):
        """
        we receive an answer from steal request.
        """
        self.current_time = self.simulator.time
        # assert not self.tasks
        if stolen_task is None:
            # still no work, steal again
            self.simulator.topology.steal_config(self, victim)
            self.start_stealing()
            #if self.cluster == victim.cluster :
            #    if self.steal_configs["successful_local_steal"] != 0:
            #        self.steal_configs["successful_local_steal"] -= 1
            #else:
            #    if self.steal_configs["successful_remote_steal"] != 0:
            #        self.steal_configs["successful_remote_steal"] -= 1
        else:
            self.simulator.topology.steal_config(self, victim, task=stolen_task)
            #if self.cluster == victim.cluster:
            #    self.steal_configs["successful_local_steal"] += 1
            #else:
            #    self.steal_configs["successful_remote_steal"] += 1

            self.current_task = stolen_task
            victim.stolen_task = None
            # Todo: repetition
            while self.current_task.get_work() == 0:
                self.current_task.start_time = self.current_time
                self.tasks.extend(self.current_task.end_execute_task(
                    self.simulator.graph,
                    self.current_time,
                    self.number))
                assert self.tasks
                self.current_task = self.tasks.pop()
            assert self.current_task.get_work()
            self.current_task.start_time = self.current_time
            becoming_idle_time = self.current_time + \
                self.current_task.get_work()//self.speed
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
    def potential(self, current_time):
        """
        return potential function value for the current processor at the current time
        """
        potential = 0
        if self.current_task is not None:
            potential += self.current_task.get_remaining_work(current_time)**2
        if self.stolen_task is not None:
            potential += 2 * self.stolen_task.get_work()**2
        return potential 




