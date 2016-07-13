#!/usr/bin/env python3
"""
the processor module provides a Processor class
holding processors states for the simulation.
"""
from math import ceil
from events import IdleEvent, StealAnswerEvent, StealRequestEvent

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
    speed = 1 # speed of all processors

    def __init__(self, number, cluster, simulator, work=0):
        self.number = number
        self.work = work
        self.simulator = simulator
        self.current_time = 0
        self.network_time = 0  # network is in use until this time
        self.cluster = cluster
        simulator.add_event(IdleEvent(work//self.speed, self))

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
            self.simulator.logger.paje_sub_work(self.current_time, self,
                                                advanced_work)
            assert self.work >= 0  # only true if speed == 1


    def answer_steal_request(self, stealer):
        """
        update current local time.
        if work left and not using network and update local work.
        update events in simulator.
        """
        self.update_time()
        reply_time = self.simulator.communication_end_time(self, stealer)

        self.simulator.logger.paje_end_communication(self.current_time,
                                                     stealer, self,
                                                     "WR")

        if self.current_time >= self.network_time:
            # we can use network
            stolen_work = self.work // 2
            self.work -= stolen_work
            if stolen_work > 0:
                self.network_time = reply_time
                becoming_idle_time = self.current_time + \
                    self.work // self.speed
                self.simulator.add_event(IdleEvent(becoming_idle_time, self))

                self.simulator.logger.paje_push_processor_state(
                    self.current_time, self, self.simulator.SEND)
                self.simulator.logger.paje_update_processor_state(
                    self.current_time, stealer, self.simulator.REC)
                self.simulator.logger.paje_sub_work(self.current_time, self,
                                                    stolen_work)
                self.simulator.logger.paje_add_work(self.current_time,
                                                    stealer, stolen_work)
        else:
            stolen_work = 0

        self.simulator.add_event(
            StealAnswerEvent(reply_time, stealer, self, stolen_work)
        )

        self.simulator.logger.paje_start_communication(self.current_time,
                                                       self, stealer,
                                                       "Response")

    def idle_event(self):
        """
        update time, start stealing.
        """
        self.update_time()
        assert self.work == 0
        self.start_stealing()
        self.simulator.logger.paje_update_processor_state(self.current_time,
                                                          self,
                                                          self.simulator.STEAL)

    def start_stealing(self):
        """
        start stealing, update simulator.
        """
        victim = self.simulator.random_victim_not(self.number)
        steal_time = self.simulator.communication_end_time(self, victim)
        self.simulator.add_event(
            StealRequestEvent(steal_time, self, victim)
        )
        self.simulator.logger.paje_start_communication(self.current_time,
                                                       self, victim, "WR")


    def steal_answer(self, work, victim):
        """
        we receive an answer from steal request.
        """
        self.update_time()
        self.work = work
        if self.work == 0:
            # still no work, steal again
            self.start_stealing()
        else:
            self.simulator.add_event(
                IdleEvent(self.current_time + ceil(self.work // self.speed),
                          self)
            )
            self.simulator.logger.paje_update_processor_state(
                self.current_time, self, self.simulator.EXEC)
            self.simulator.logger.paje_pop_processor_state(
                self.current_time, victim)

        self.simulator.logger.paje_end_communication(self.current_time,
                                                     victim, self, "Response")

