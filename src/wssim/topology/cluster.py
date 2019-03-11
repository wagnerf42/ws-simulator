"""
topology related functions for 1 cluster.
"""
from random import random


class Topology:
    """
    Store all topology related informations and methods.
    """

    def __init__(self, processors_number, is_simultaneous,
                 local_latency=1, remote_latency=None,
                 remote_steal_probability=None,
                 victim_selection_strategy=None
                 ):
        self.processors_number = processors_number
        self.latency = local_latency
        self.local_granularity = None
        self.is_simultaneous = is_simultaneous
        self.victim_selection_strategy = None

    def distance(self, *processor_numbers):
        """
        Returns distance between the two given processors numbers.
        """
        return self.latency

    def update_remote_latency(self, latency):
        """
        Set remote latency.
        """
        self.latency = latency

    def cluster_number(self, processor_id):
        """
        return cluster id for given processor
        """
        return 0


    def update_granularity(self, local_granularity, remote_granularity,
                           threshold):
        """
        update local and remote grenularity,
        """
        if local_granularity is None:

            self.local_granularity = threshold
        else:
            self.local_granularity = local_granularity

    def select_victim_not(self, unwanted_processor):
        """
        select a random target not unwanted_processor.number.
        """
        if self.processors_number == 1:
            print("one processor")
            return 0
        victim = int(random() * (self.processors_number-1))
        if victim >= unwanted_processor.number:
            victim += 1
        return victim

