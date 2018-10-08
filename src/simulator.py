#!/usr/bin/env python3.5
"""
Simulation System configuration
"""
import json
import wssim
import argparse
from math import floor
from random import seed
from time import clock
from wssim.task import DAG_task, Divisible_load_task, Adaptive_task
from wssim.simulator import Simulator
from wssim.task import Task, init_task_tree, compute_depth, display_DAG
from wssim import activate_logs, set_unit
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


def update_graph(tasks, graph):
    """
    add tasks list to Json file
    """
    info = dict()
    info["id"] = tasks.id
    info["start_time"] = 0
    info["end_time"] = 0
    info["thread_id"] = 0
    info["children"] = [child.id for child in tasks.children]
    graph[tasks.id] = info
    for child in tasks.children:
        update_graph(child, graph)


def main():
    """
    main program to start Simulation
    """
    parser = argparse.ArgumentParser(
        description="simulate work stealing algorithm")
    parser.add_argument("-rsp", dest="remote_steal_probability",
                        default=0.5, type=float,
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
    parser.add_argument("-s", dest="seed", type=float,
                        default=clock(), help="random seed")
    parser.add_argument("-r", dest="runs",
                        default=1, type=int,
                        help="number of runs to execute")
    parser.add_argument("-tasks", dest="tasks", action="store_true",
                        help="use tree tasks")
    parser.add_argument("-adapt", dest="adaptative", action="store_true",
                        help="use adaptative tasks")
    parser.add_argument("-d", dest="debug", action="store_true",
                        help="activate traces")
    parser.add_argument("-tt", dest="task_threshold", default=[100],
                        nargs='+', type=int, help="threshold for real tasks")
    parser.add_argument("-lg", dest="local_granularity", default=2,
                        type=int, help="local stealing granularity")
    parser.add_argument("-rg", dest="remote_granularity", default=None,
                        type=int, help="remote stealing granularity ")
    parser.add_argument("-f", dest="log_file", default=None)
    parser.add_argument("-sim", dest="is_simultaneous", action="store_true",
                        help="activate simultaneously steal")
    parser.add_argument("-json_in", dest="json_file_in", default=None)
    parser.add_argument("-json_out", dest="json_file_out", default=None)
    parser.add_argument("-svg_time_scal", dest="unit", default=100, type=int,
                        help="unit for svg")

    arguments = parser.parse_args()

    print("#using seed", arguments.seed)
    seed(arguments.seed)

    if arguments.debug:
        activate_logs()

    if arguments.json_file_out is not None:
        set_unit(arguments.unit)

    platform = Topology(arguments.processors,
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

    if arguments.json_file_in:
        works = [0]
    else:
        simulator.graph = []
        if not arguments.work_config:
            works = [arguments.work]
        else:
            works = list(power_range(*arguments.work_config))

    print("#PROCESSORS: {}, RUNS: {}".format(
        arguments.processors,
        arguments.runs))
    print("#prb\tR-l\tISR\tESR\trunTime\tprocessors\
    \twork\tdepth\ttaskThreshold\tlGranularity\
    \trGranularity\tIDATAT\tEDATAT\tW0\tW1")

    for work in works:
        for threshold in arguments.task_threshold:
            for probability in probabilities:
                arguments.probability = probability
                simulator.topology.remote_steal_probability = probability
                for latency in latencies:
                    simulator.topology.update_remote_latency(latency)
                    # arguments.local_granularity = 2
                    # arguments.remote_granularity = 2*latency
                    if arguments.tasks:
                        arguments.local_granularity = threshold
                    simulator.topology.update_granularity(
                        arguments.local_granularity,
                        arguments.remote_granularity, threshold)
                    for _ in range(arguments.runs):
                        if arguments.tasks or arguments.json_file_in is not None:

                            if arguments.json_file_in is not None:
                                first_task, work, depth, logs = init_task_tree(file_name=arguments.json_file_in)
                                if arguments.json_file_out:
                                    simulator.graph = logs["tasks_logs"]
                            else:
                                first_task = init_task_tree(work, threshold)
                                depth = threshold
                                if arguments.json_file_out:
                                    tasks_data = dict()
                                    update_graph(first_task, tasks_data)
                                    simulator.graph = [v for v in
                                                       tasks_data.values()]

                            simulator.reset(work, first_task)
                        elif arguments.adaptative:
                            #  simulator.reset(work,
                            #        Adaptive_task(
                            #            work,
                            #            lambda left_work, right_work:DAG_task(left_work+right_work),
                            #            lambda size : size*2
                            #                    )
                            #               )
                            simulator.reset(work,
                                    Adaptive_task(work,
                                        lambda left_work, right_work, :
                                        Adaptive_task(left_work + right_work,
                                                    lambda left_work, right_work, :
                                                    DAG_task(1),
                                                    lambda size: size
                                                    ),
                                        lambda size:size*3
                                        )
                                    )
                            depth = 0
                        else:
                            simulator.reset(work, Divisible_load_task(work))
                            depth = 0

                        simulator.run()
                        if arguments.json_file_out:
                            json_data = dict()
                            json_data["threads_number"] = arguments.processors
                            json_data["duration"] = simulator.time * wssim.UNIT
                            json_data["tasks_number"] = len(simulator.graph)
                            json_data["tasks_logs"] = simulator.graph

                            with open(arguments.json_file_out, 'w') as outfile:
                                json.dump(json_data,
                                          outfile, indent=2)

                        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\
                              \t{}\t{}\t{}\t{}\t{}"
                              .format(
                                  probability, latency,
                                  simulator.steal_info["IWR"],
                                  # simulator.steal_info["SIWR"],
                                  simulator.steal_info["EWR"],
                                  # simulator.steal_info["SEWR"],
                                  simulator.time,
                                  arguments.processors,
                                  work,
                                  depth,
                                  threshold,
                                  arguments.local_granularity,
                                  arguments.remote_granularity,
                                  simulator.steal_info["WI"],
                                  simulator.steal_info["WE"],
                                  simulator.steal_info["W0"],
                                  simulator.steal_info["W1"],
                                  # simulator.steal_info["beginning"]
                              ))


if __name__ == "__main__":
    main()
