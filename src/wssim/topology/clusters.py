"""
topology related functions for 2 clusters.
"""
from random import uniform, randint, random

class Topology:
    """
    Store all topology related informations and methods.
    """
    def __init__(self, processors_number, is_simultaneous,
                 local_latency=1, remote_latency=None,
                 remote_steal_probability=None,
                 victim_selection_strategy=None,
                 clusters_number=6
                ):
        self.processors_number = processors_number
        self.clusters_number = clusters_number
        self.remote_steal_probability = remote_steal_probability
        self.latencies = [remote_latency, local_latency]

        self.cluster_sizes = [self.processors_number//clusters_number]*(clusters_number-1)
        self.cluster_sizes.append(self.processors_number -\
                                  (clusters_number-1)*self.processors_number//clusters_number)
        self.cluster_starts = [self.cluster_sizes[0]*i for i in range(self.clusters_number)]
        self.remote_granularity = None
        self.local_granularity = None
        self.is_simultaneous = is_simultaneous
        self.victim_selection_strategy = victim_selection_strategy

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
        target_cluster = -1
        for start in self.cluster_starts:
            if processor_id >= start:
                target_cluster += 1

        return target_cluster

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

    def select_cluster_with_probability(self, stealer):
        """
        select cluster  with probabilistic strategy
        """
        cluster = self.cluster_number(stealer.number)
        remaining_clusters = list(filter(lambda c: c != cluster, range(self.clusters_number)))

        if uniform(0, 1) < self.remote_steal_probability:
            return remaining_clusters[randint(0, self.clusters_number-2)]

        return cluster

    def select_cluster_systematically(self, stealer):
        """
        select cluster  with systematic strategy
        """
        cluster = self.cluster_number(stealer.number)
        remaining_clusters = list(filter(lambda c: c != cluster, range(self.clusters_number)))
        print("stealer.steal_attempt_max", stealer.steal_attempt_max)
        if stealer.steal_attempt_number > stealer.steal_attempt_max:
            stealer.steal_attempt_number = 0
            return remaining_clusters[randint(0, self.clusters_number-2)]

        stealer.steal_attempt_number += 1
        return cluster

    def select_cluster_SBS(self, stealer):
        """
        select cluster based on successful steal
        """
        print(stealer.number,"at", stealer.simulator.time, "select_cluster_SBS: R:", stealer.successful_remote_steal," L", stealer.successful_local_steal )
        cluster = self.cluster_number(stealer.number)
        remaining_clusters = list(filter(lambda c: c != cluster, range(self.clusters_number)))
        if stealer.successful_remote_steal > stealer.successful_local_steal:
            #stealer.successful_remote_steal -= 1
            return remaining_clusters[randint(0, self.clusters_number-2)]

         #stealer.successful_local_steal -= 1
        return cluster

    def select_victim_not(self, unwanted_processor):
        """
        select a random target not unwanted_processor_number.
        """
        cluster = self.cluster_number(unwanted_processor.number)
        remaining_clusters = list(filter(lambda c: c != cluster, range(self.clusters_number)))
        assert not cluster in remaining_clusters
        target_cluster = cluster

        if self.victim_selection_strategy == 0: #Probabilistic strategy
            target_cluster = self.select_cluster_with_probability(unwanted_processor)
        elif self.victim_selection_strategy == 1 or self.victim_selection_strategy == 2: #Systematic strategy
            target_cluster = self.select_cluster_systematically(unwanted_processor)
        elif self.victim_selection_strategy == 3 or self.victim_selection_strategy == 4:
            if unwanted_processor.successful_remote_steal <= 0 and \
                    unwanted_processor.successful_local_steal <= 0:
                if self.victim_selection_strategy == 4:
                    target_cluster = self.select_cluster_systematically(unwanted_processor)
                elif self.victim_selection_strategy == 3 :
                    target_cluster = self.select_cluster_with_probability(unwanted_processor)

            else:
                target_cluster = self.select_cluster_SBS(unwanted_processor)

        victim = self.cluster_starts[target_cluster] +\
            int(random() * (self.cluster_sizes[target_cluster]-1))
        victim_1 = victim
        if victim >= unwanted_processor.number:
            victim += 1
        assert unwanted_processor.number != victim
        assert self.cluster_number(victim_1) == self.cluster_number(victim)
        return victim


