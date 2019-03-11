"""
topology related functions for 2 clusters.
"""
from random import uniform, randint

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
        self.latencies = [remote_latency, local_latency]
        self.cluster_sizes = [self.processors_number//2]
        self.cluster_sizes.append(self.processors_number -
                                  self.cluster_sizes[0])
        self.cluster_starts = [0, self.cluster_sizes[0]]
        self.remote_granularity = None
        self.local_granularity = None
        self.is_simultaneous = is_simultaneous
        self.victim_selection_strategy = victim_selection_strategy
        """
        if self.victim_selection_strategy == 0: 
            self.remote_steal_probability = 0.5 
        elif self.victim_selection_strategy == 1:
            self.steal_attempt_max = victim_selection_strategy[1]
        elif self.victim_selection_strategy == 2:
            assert(len(victim_selection_strategy) > 2)
            self.steal_attempt_max = victim_selection_strategy[1]
            self.steal_attempt_min = victim_selection_strategy[2]
        """

    def distance(self, *processor_numbers):
        """
        Returns distance between the two given processors numbers.
        """
        assert self.latencies[0] is not None
        clusters = [self.cluster_number(p) for p in processor_numbers]
        return self.latencies[clusters[0] == clusters[1]]

    def update_remote_latency(self, remote_latency):
        """
        Set remote latency.
        """
        self.latencies[0] = remote_latency

    def cluster_number(self, processor_id):
        """
        return cluster id for given processor
        """
        if processor_id < self.processors_number // 2:
            return 0
        else:
            return 1

    def update_granularity(self, local_granularity, remote_granularity, 
                           threshold):
        """
        update local and remote grenularity,
        """
        if local_granularity is None:
            self.local_granularity = threshold
        else:
            self.local_granularity = local_granularity

        if remote_granularity is None:
            self.remote_granularity = threshold
        else:
            self.remote_granularity = remote_granularity

    def select_victim_not(self, unwanted_processor):
        """
        select a random target not unwanted_processor_number.
        """
        cluster = self.cluster_number(unwanted_processor.number)
        if self.victim_selection_strategy == 0:
            if uniform(0, 1) < self.remote_steal_probability:
                target_cluster = 1 - cluster
            else:
                target_cluster = cluster
        else:
            if unwanted_processor.steal_attempt_number > unwanted_processor.steal_attempt_max:
                target_cluster = 1 - cluster
                unwanted_processor.steal_attempt_number = 0
            else:
                target_cluster = cluster
                unwanted_processor.steal_attempt_number += 1

        target_number = unwanted_processor.number
        while target_number == unwanted_processor.number:
            target_number = self.cluster_starts[target_cluster] +\
                randint(0, self.cluster_sizes[target_cluster]-1)
        return target_number
