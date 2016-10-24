"""
topology related functions for 1 cluster.
"""
from random import randint


class Topology:
    """
    Store all topology related informations and methods.
    """
    def __init__(self, processors_number, is_tasks,
                 local_latency=1, remote_latency=None,
                 remote_steal_probability=None):
        self.processors_number = processors_number
        self.latency = local_latency
        self.local_granularity = None
        self.is_tasks = is_tasks

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


    def update_granularity(self, local_granularity, remote_granularity):
        """
        update local and remote grenularity,
        """
        if local_granularity is None:
            self.local_granularity = 4 * self.latency
        else:
            self.local_granularity = local_granularity

    def select_victim_not(self, unwanted_processor_number):
        """
        select a random target not unwanted_processor_number.
        """
        target_number = unwanted_processor_number
        while target_number == unwanted_processor_number:
            target_number = randint(0, self.processors_number-1)
        return target_number
