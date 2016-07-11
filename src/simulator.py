#!/usr/bin/env python3
"""
Simulation System configuration
"""

import sys
from time import clock
from random import randint, seed
from heapq import heappush, heappop
from processor import Processor

class Simulator:
    """
    Simulation
    """

    internal_communication_time = 1
    external_communication_time = 5

    def __init__(self, total_work, processors_number):
        self.time = 0
        self.total_work = total_work
        self.processors_number = processors_number
        self.processors = list()
        self.distances = two_clusters_topology(processors_number)
        self.events = list()
        # associate to each processor the next valid event
        # we do that since the heap contains cancelled events which we
        # cannot remove
        self.valid_events = dict()
        self.init_processors()

    def run(self):
        """
        start Simulation of the system
        """
        while self.total_work > 0:
            event = self.next_event()
            self.time = event.time
            event.execute()

    def add_event(self, event):
        """
        add given event to system.
        pre-requisite : event's time is >= simulator's time
        """
        heappush(self.events, event)
        # newest event is always the valid one
        assert isinstance(event.processor, Processor)
        self.valid_events[event.processor] = event

    def next_event(self):
        """
        returns the next valid event to take place.
        """
        # loop discarding all cancelled events
        event = heappop(self.events)
        while event != self.valid_events[event.processor]:
            event = heappop(self.events)
        return event

    def init_processors(self):
        """
        cree l'ensemble des processor
        """
        self.processors.append(Processor(0, self, self.total_work))
        for id_processor in range(1, self.processors_number):
            self.processors.append(Processor(id_processor, self))

    def communication_time(self, source, destination):
        """
        return time when communication between source and destination
        processors will end if we start it now.
        """
        return self.time + self.distances[source.number][destination.number]

    def random_victim_not(self, avoided_number):
        """
        return a random processor id chosen uniformly among ids different
        from given import one.
        """
        random_processor = randint(0, self.processors_number-2)
        if random_processor >= avoided_number:
            return self.processors[random_processor+1]
        else:
            return self.processors[random_processor]


def cluster_number(processor_id, processors_number):
    """
    return cluster id for given processor
    """
    if processor_id < processors_number // 2:
        return 0
    else:
        return 1

def two_clusters_topology(processors_number):
    """
    return matrix containing for line i, column j
    the cost in time for communicating between processor
    number i and processor number j in two clusters topology.
    """
    distances = []
    for start_processor in range(processors_number):
        start_cluster = cluster_number(start_processor, processors_number)
        distances_from_start = []
        for destination_processor in range(processors_number):
            destination_cluster = cluster_number(destination_processor,
                                                 processors_number)
            if start_cluster == destination_cluster:
                distances_from_start.append(1)
            else:
                distances_from_start.append(10)

        distances.append(distances_from_start)

    return distances


def main(processors_number, work):
    """
    main program to start Simulation
    """
    simulator = Simulator(work, processors_number)
    simulator.run()
    print("total work ", simulator.time)

if __name__ == "__main__":

    if __debug__:
        current_time = clock()
        seed(current_time)
        print("seeding with", current_time)

    for argument in sys.argv:
        if argument == "--help":
            print("no help yet !")
            sys.exit(1)
    if len(sys.argv) < 3:
        print("please give following args Processor Number and Total Work")
    else:
        processors_number = int(sys.argv[1])
        total_work = int(sys.argv[2])
        main(processors_number, total_work)
