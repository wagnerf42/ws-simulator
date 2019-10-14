"""
provides Simulator class containing the global simulation state.
"""
from heapq import heappush, heappop
from collections import defaultdict
from random import randint
from wssim.processor import Processor
from wssim.logger import Logger
from wssim.task import Task


class Simulator:
    """
    Simulation
    """

    def __init__(self, processors_number, log_file, topology):
        self.log_file = log_file
        self.time = 0
        self.total_work = 0
        self.logger = None
        self.topology = topology
        self.remote_steal_probability = None
        self.local_granularity = None
        self.remote_granularity = None
        self.is_beginning = True

        if __debug__:
            if self.log_file is not None:
                self.logger = Logger(log_file, self)
        self.events = list()
        self.processors = list()
        self.graph = list()
        # associate to each processor the next valid event
        # we do that since the heap contains cancelled events which we
        # cannot remove
        self.active_processors = dict()
        self.valid_events = dict()
        self.init_processors(processors_number)
        self.steal_info = defaultdict(int)
        self.Isteal_data = defaultdict(int)
        self.Esteal_data = defaultdict(int)
        if __debug__:
            if self.log_file is not None:
                self.platform_definition_logger(topology.clusters_number)

    def reset(self, work, first_task):
        """
        sets work, create all initial events
        """
        self.valid_events.clear()
        self.events.clear()
        self.total_work = 0
        self.time = 0
        self.graph.clear()
        self.is_beginning = True
        self.steal_info.clear()
        self.active_processors.clear()
        for index, processor in enumerate(self.processors):
            if index:
                processor.reset()
            else:
                processor.reset(first_task=first_task)
                self.add_active_processor(processor)


    def run(self):
        """
        start Simulation of the system
        """
        info = dict()
        while Task.remaining_tasks:
        # while self.total_work > 0:
            event = self.next_event()
            self.time = event.time
            event.execute()
            potential = sum([proc.potential(self.time) for proc in self.processors])
            latence = self.topology.distance(0, 1)
            info[self.time] = (len(self.processors)- len(self.active_processors), 1 + potential / (latence**2))

        for time in info:
            print(time, len(self.processors), info[time][0], info[time][1] )
                  #"W", [(proc.number, proc.current_task.get_remaining_work(self.time)) for proc in self.processors if proc.current_task is not None],
                  #"S", [(proc.number, proc.stolen_task.get_work()) for proc in self.processors if proc.stolen_task is not None],
                  #"potential", [(proc.number, proc.potential(self.time)) for proc in self.processors], "", potential)

        if __debug__:
            if self.log_file is not None:
                self.logger.end_of_logger(clusters_number=self.topology.clusters_number,
                                          processors_number=len(
                                              self.processors))

    def add_event(self, event):
        """
        add given event to system.
        pre-requisite : event's time is >= simulator's time
        """
        heappush(self.events, event)
        # newest event is always the valid one
        if event.processor is not None:
            assert isinstance(event.processor, Processor)
            self.valid_events[event.processor] = event

    def next_event(self):
        """
        returns the next valid event to take place.
        """
        # loop discarding all cancelled events
        event = heappop(self.events)
        while event.processor is not None and \
                event != self.valid_events[event.processor]:
            event = heappop(self.events)
        return event

    def init_processors(self, processors_number):
        """
        cree l'ensemble des processor
        """
        cluster = self.topology.cluster_number(0)
        self.processors.append(Processor(0, cluster, self))
        for id_processor in range(1, processors_number):
            cluster = self.topology.cluster_number(id_processor)
            self.processors.append(Processor(id_processor, cluster, self))

    def communication_end_time(self, source, destination):
        """
        return time when communication between source and destination
        processors will end if we start it now.
        """
        return self.time +\
            self.topology.distance(source.number, destination.number)

    def platform_definition_logger(self, clusters_number):
        """
        log to create platform definition,
            clusters and processors with their names and numbers
        """
        # Create Clusters.
        for id_cluster in range(clusters_number):
            self.logger.add_cluster(id_cluster)

        # Create Processors.
        for processor in self.processors:
            self.logger.add_processor(processor)

        # set (update) intial state Processors.
        for processor in self.processors:
            if processor.number == 0:
                self.logger.update_processor_state(processor,
                                                   new_state="Executing")
            else:
                self.logger.update_processor_state(processor,
                                                   new_state="Idle")
        # set initial work Processors.
        for processor in self.processors:
            if processor.number == 0:
                self.logger.set_work(processor, self.total_work)
            else:
                self.logger.set_work(processor)

    def add_active_processor(self, processor):
        """
        add processor to the active processor list.
        """
        # print("+ P", processor.number)
        # if self.is_beginning:
        #     print("+ P", processor.number)
        self.active_processors[processor.number] = processor.number
        if self.is_beginning and len(self.active_processors) == \
                len(self.processors):
            self.steal_info["beginning"] = self.time
            self.is_beginning = False

    def rm_active_processor(self, processor):
        """
        remove processor to the active processor list.
        """
        if processor.number in self.active_processors:
            self.active_processors.pop(processor.number)
        # if len(self.active_processors) == 0:

