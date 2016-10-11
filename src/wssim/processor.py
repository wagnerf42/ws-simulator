#!/usr/bin/env python3
"""
the processor module provides a Processor class
holding processors states for the simulation.
"""
from math import ceil, isclose
from collections import defaultdict
from sortedcontainers import SortedListWithKey
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

    def __init__(self, number, cluster, simulator, work=0):
        self.number = number
        self.work = work
        self.time_stealing = 0
        self.simulator = simulator
        self.current_time = 0
        self.network_time = 0  # network is in use until this time
        self.work_sending = 0
        self.cluster = cluster
        self.steal_probabilities = []
        self.potential = defaultdict(int)

    def reset(self, work):
        """
        reset all counters. initialize work with given value.
        """
        self.current_time = 0
        self.network_time = 0
        self.work_sending = 0
        self.time_stealing = 0
        self.work = work

    def __hash__(self):
        return hash(self.number)

    def __eq__(self, other):
        return self.number == other.number

    def update_time(self):
        """
        advance local time to simulator time.
        """
        advanced_work = (self.simulator.time - self.current_time)\
            * self.speed

        self.current_time = self.simulator.time

        if self.work > 0:
            self.work -= advanced_work
            self.simulator.total_work -= advanced_work
            assert self.work >= 0  # only true if speed == 1
            if __debug__:
                if self.simulator.log_file is not None:
                    self.simulator.logger.sub_work(self, advanced_work)

    def answer_steal_request(self, stealer):
        """
        update current local time.
        if work left and not using network and update local work.
        update events in simulator.
        """
        self.update_time()
        reply_time = self.simulator.communication_end_time(self, stealer)

        if __debug__:
            if self.simulator.log_file is not None:
                self.simulator.logger.end_communication(stealer, self, "WReq")

        if self.current_time >= self.network_time and \
                self.work > self.simulator.threshold_steal *\
                self.simulator.topology.distance(self.number, stealer.number):
            # we can use network and we have enough work to send
            stolen_work = self.work // 2
            self.work -= stolen_work
            self.work_sending += stolen_work # !!!!!!!!!!!!!!
            if stolen_work > 0:
                if self.cluster == stealer.cluster:
                    self.simulator.steal_info["SIWR"] += 1
                else:
                    self.simulator.steal_info["SEWR"] += 1
                self.network_time = reply_time
                becoming_idle_time = self.current_time + \
                    self.work // self.speed
                self.simulator.add_event(IdleEvent(becoming_idle_time, self))

                if __debug__:
                    if self.simulator.log_file is not None:
                        self.simulator.logger.push_processor_state(
                            self, new_state="Sending")
                        self.simulator.logger.update_processor_state(
                            stealer, new_state="Receiving")
                        self.simulator.logger.sub_work(self, stolen_work)
                        self.simulator.logger.add_work(stealer, stolen_work)
        else:
            stolen_work = 0

        self.simulator.add_event(
            StealAnswerEvent(reply_time, stealer, self, stolen_work)
        )

        if __debug__:
            if self.simulator.log_file is not None:
                self.simulator.logger.start_communication(
                    self, stealer, data="Response")

    def idle_event(self):
        """
        update time, start stealing.
        """
        self.update_time()
        if __debug__:
            if self.work != 0:
                print("work is", self.work)
                raise Exception("work non zero")
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

    def steal_answer(self, work, victim):
        """
        we receive an answer from steal request.
        """
        self.time_stealing += 2*self.simulator.topology.distance(
            self.number, victim.number)
        self.update_time()
        self.work = work
        if self.work == 0:
            # still no work, steal again
            self.start_stealing()
        else:
            victim.work_sending -= work
            self.simulator.add_event(
                IdleEvent(self.current_time + ceil(self.work // self.speed),
                          self)
            )
            if __debug__:
                if self.simulator.log_file is not None:
                    self.simulator.logger.update_processor_state(
                        self, new_state="Executing")
                    self.simulator.logger.pop_processor_state(victim)

        if __debug__:
            if self.simulator.log_file is not None:
                self.simulator.logger.end_communication(victim, self,
                                                        data="Response")

    def compute_stealing_probabilities(self, processors):
        """
        compute probabilities used for stealing operations.
        """
        remaining_processors = SortedListWithKey(processors,
                                                 key=lambda p: p[0])
        target = sum([p[0] for p in processors])/len(processors)
        for _ in range(len(processors)):
            min_probability, min_processor = remaining_processors.pop(0)
            if isclose(min_probability, target):
                self.steal_probabilities.append(
                    ((target, min_processor), (0, None))
                )
            else:
                assert len(remaining_processors) > 0
                max_probability, max_processor = remaining_processors.pop()
                assert max_probability + min_probability > target or\
                    isclose(max_probability + min_probability, target)
                needed = target - min_probability
                remaining_processors.add((max_probability - needed,
                                          max_processor))
                self.steal_probabilities.append(
                    ((min_probability, min_processor),
                     (needed, max_processor))
                )

    def update_potential(self):
        """
        update potential value in the processor.
        """
        self.potential[self.current_time] = self.work**2
