#!/usr/bin/env python3
"""
Simulation System configuration
"""

import argparse
from math import floor
from random import seed
from time import clock
from wssim.simulator import Simulator
from wssim.task import Task, init_task_tree
from wssim import activate_logs
from wssim.topology.cluster import Topology
#from wssim.topology.clusters import Topology


def floating_range(start, end, step):
    """
    return iterator from start to end with given step.
    """
    for iteration in range(1+floor((end-start)/step)):
        yield start + iteration * step


def power_range(start, end, step):
    """
    return iterator between start and end, multiplying by step
    """
    current_value = start
    while current_value <= end:
        yield current_value
        current_value *= step


def main():
    """
    main program to start Simulation
    """
    parser = argparse.ArgumentParser(
        description="simulate work stealing algorithm")
    parser.add_argument("-rsp", dest="remote_steal_probability",
                        default=0.5, type=float,\
                        help="probability of stealing remotely")
    parser.add_argument('-rspconf', nargs=3, dest="probabilities_config",
                        type=float, help="interval config of \
                        stealing remotely probabilities ,\
                        (-rspconf min_probability max_probability step)")
    parser.add_argument('-lconf', nargs=3, dest="latencies_config",
                        type=int, help="interval config of \
                        latencies ,\
                        (-lconf min_latency max_latency step)")
    parser.add_argument('-wconf', nargs=3, dest="work_config",
                        type=int, help="interval config of \
                        work,\
                        (-wconf min_work max_work multiplicative_step)")
    parser.add_argument("-p", dest="processors",
                        default=4, type=int,
                        help="total number of processors")
    parser.add_argument("-w", dest="work",
                        default=100, type=int,
                        help="total work")
    parser.add_argument("-l", dest="latency",
                        default=5, type=int,
                        help="latency for remote steal")
    parser.add_argument("-s", dest="seed", type=float,\
                        default=clock(), help="random seed")
    parser.add_argument("-r", dest="runs",
                        default=1, type=int,
                        help="number of runs to execute")
    parser.add_argument("-tasks", dest="tasks", action="store_true",
                        help="use tree tasks")
    parser.add_argument("-d", dest="debug", action="store_true",
                        help="activate traces")
    parser.add_argument("-tt", dest="task_threshold", default=[100],
                        nargs='+', type=int, help="threshold for real tasks")
    parser.add_argument("-lg", dest="local_granularity", default=None, type=int,
                        help="local stealing granularity")
    parser.add_argument("-rg", dest="remote_granularity", default=None,
                        type=int, help="remote stealing granularity ")
    parser.add_argument("-f", dest="log_file", default=None)
    parser.add_argument("-sim", dest="is_simultaneous", action="store_true",
                        help="activate simultaneously steal")
    arguments = parser.parse_args()

    print(arguments.is_simultaneous)
    print("#using seed", arguments.seed)
    seed(arguments.seed)

    if arguments.debug:
        activate_logs()

    platform = Topology(arguments.processors, arguments.tasks,
                        arguments.is_simultaneous)
    simulator = Simulator(arguments.processors,
                          arguments.log_file, platform)

    if not arguments.probabilities_config:
        probabilities = [arguments.remote_steal_probability]
    else:
        probabilities = list(floating_range(*arguments.probabilities_config))

    if not arguments.latencies_config:
        latencies = [arguments.latency]
    else:
        latencies = list(floating_range(*arguments.latencies_config))

    if not arguments.work_config:
        works = [arguments.work]
    else:
        works = list(power_range(*arguments.work_config))

    print("#PROCESSORS: {}, RUNS: {}".format(
        arguments.processors,
        arguments.runs))
    print("#probability\tremote latency\tinternal steal number\t SISN\t \
          external steal number\tSESN\trunning time\tprocessors\twork\t \
          task threshold")

    for work in works:
        for threshold in arguments.task_threshold:
            if arguments.tasks:
                first_task = init_task_tree(work, threshold)
            for probability in probabilities:
                arguments.probability = probability
                simulator.topology.remote_steal_probability = probability
                for latency in latencies:
                    simulator.topology.update_remote_latency(latency)
                    simulator.topology.update_granularity(
                        arguments.local_granularity,
                        arguments.remote_granularity, threshold)
                    for _ in range(arguments.runs):
                        if arguments.tasks:
                            simulator.reset(work, first_task)
                        else:
                            simulator.reset(work, Task(work, []))
                        simulator.run()
                        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                            probability, latency,
                            simulator.steal_info["IWR"],
                            simulator.steal_info["SIWR"],
                            simulator.steal_info["EWR"],
                            simulator.steal_info["SEWR"],
                            simulator.time,
                            arguments.processors,
                            work,
                            threshold
                        ))


if __name__ == "__main__":
    main()
