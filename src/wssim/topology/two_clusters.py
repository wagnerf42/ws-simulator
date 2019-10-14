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
                 victim_selection_strategy=None
                 ):
        self.processors_number = processors_number
        self.clusters_number = 2
        self.latencies = [remote_latency, local_latency]
        self.cluster_sizes = [self.processors_number//2]
        self.cluster_sizes.append(self.processors_number -
                                  self.cluster_sizes[0])
        self.cluster_starts = [0, self.cluster_sizes[0]]
        self.remote_granularity = None
        self.local_granularity = None
        self.is_simultaneous = is_simultaneous
        self.victim_selection_strategy = victim_selection_strategy
        self.remote_steal_probability = list()
        self.remote_steal_probability_step = None
        self.steal_attempt_max = list()
        self.steal_attempt = list()
        self.successful_local_steal = list()
        self.successful_remote_steal = list()


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

    def victim_selection_config(self, config, step=None):
        """
        """
        if step is not None:
            self.remote_steal_probability_step = step
        if self.victim_selection_strategy == 0 or self.victim_selection_strategy == 1:
            self.remote_steal_probability = self.processors_number*[config]
        elif self.victim_selection_strategy == 2 :
            self.steal_attempt_max = self.processors_number*[config]
            self.steal_attempt = self.processors_number*[0]
        elif self.victim_selection_strategy == 3:
            self.remote_steal_probability = self.processors_number*[config]
            self.successful_local_steal = self.processors_number*[0]
            self.successful_remote_steal = self.processors_number*[0]


        #print("proba config", self.remote_steal_probability)
        #rint("syst config", self.steal_attempt_max)
        #print("succ local config", self.successful_local_steal)
        #print("succ remote config", self.successful_remote_steal)

    def steal_config(self, stealer, victim, task=None):
        """
        """
        if task:
            if self.victim_selection_strategy == 1: #proba_dynamic
                self.remote_steal_probability[stealer.number] = 0

            elif self.victim_selection_strategy == 2: #systematic
                self.steal_attempt[stealer.number] = 0

            elif self.victim_selection_strategy == 3: ##based on successful steal
                self.remote_steal_probability[stealer.number] = 0
                if stealer.cluster == victim.cluster:
                    self.successful_local_steal[stealer.number] += 1
                else:
                    self.successful_remote_steal[stealer.number] += 1
        else:
            if self.victim_selection_strategy == 1:
                if stealer.cluster == victim.cluster:
                    self.remote_steal_probability[stealer.number] += self.remote_steal_probability_step
                else:
                    self.remote_steal_probability[stealer.number] = 0

            elif self.victim_selection_strategy == 2:
                if stealer.cluster == victim.cluster:
                    self.steal_attempt[stealer.number] += 1
                else:
                    self.steal_attempt[stealer.number] = 0

            elif self.victim_selection_strategy == 3:
                self.remote_steal_probability[stealer.number] += self.remote_steal_probability_step
                if stealer.cluster == victim.cluster:
                    if self.successful_local_steal[stealer.number] != 0:
                        self.successful_local_steal[stealer.number] -= 1
                else:
                    if self.successful_remote_steal[stealer.number] != 0:
                        self.successful_remote_steal[stealer.number] -= 1

    def select_cluster_with_probability(self, stealer):
        """
        select cluster  with probabilistic strategy
        """
        cluster = self.cluster_number(stealer.number)
        if uniform(0, 1) < self.remote_steal_probability[stealer.number]:
            return 1 - cluster
        return cluster

    def select_cluster_with_dynamic_probability(self, stealer):
        """
        select cluster  with dynamic probabily strategy
        """
        cluster = self.cluster_number(stealer.number)
        if uniform(0, 1) < self.remote_steal_probability[stealer.number]:
            return 1 - cluster

        return cluster

    def select_cluster_systematically(self, stealer):
        """
        select cluster  with systematic strategy
        """
        cluster = self.cluster_number(stealer.number)
        if self.steal_attempt[stealer.number] >= self.steal_attempt_max[stealer.number]:
            return 1 - cluster
        return cluster

    def select_cluster_SBS(self, stealer):
        """
        select cluster based on successful steal
        """
        if self.successful_local_steal[stealer.number] == 0 and self.successful_remote_steal[stealer.number] == 0:
            return self.select_cluster_with_dynamic_probability(stealer)
        else:
            cluster = self.cluster_number(stealer.number)
            if self.successful_remote_steal[stealer.number] >= self.successful_local_steal[stealer.number]:
                return 1 - cluster
            return cluster

    def select_victim_not(self, unwanted_processor):
        """
        select a random target not unwanted_processor_number.
        """
        if self.victim_selection_strategy == 0: #Probabilistic strategy
            target_cluster = self.select_cluster_with_probability(unwanted_processor)

        elif self.victim_selection_strategy == 1 : #Dynamic Probabilistic strategy 
            target_cluster = self.select_cluster_with_dynamic_probability(unwanted_processor)

        elif self.victim_selection_strategy == 2 : #systematically strategy 
            target_cluster = self.select_cluster_systematically(unwanted_processor)

        elif self.victim_selection_strategy == 3: #based on successful steal 
            target_cluster = self.select_cluster_SBS(unwanted_processor)

        victim = self.cluster_starts[target_cluster] +\
            int(random() * (self.cluster_sizes[target_cluster]-1))
        victim_1 = victim
        if victim >= unwanted_processor.number:
            victim += 1
        assert unwanted_processor.number != victim
        assert self.cluster_number(victim_1) == self.cluster_number(victim)
        return victim












"""


    def select_victim_not(self, unwanted_processor):
        ""
  #      select a random target not unwanted_processor_number.
       ""
        cluster = self.cluster_number(unwanted_processor.number)
        if self.victim_selection_strategy == 0 :
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

"""
