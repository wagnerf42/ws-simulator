#!/usr/bin/env python3.5
"""
Simulation System configuration
"""

import json
import argparse
import operator
from math import floor, log2, sqrt
from random import seed
from time import clock

import wssim
from wssim.task import Task, DagTask, \
        DivisibleLoadTask, AdaptiveTask, init_blk_size
from wssim.simulator import Simulator
from wssim.task import init_task_tree
from wssim import activate_logs, svg_time_scal, block_factor, \
        init_task_cost, g_geo_blk_number, g_init_blk_size
from wssim.topology.cluster import Topology
# from wssim.topology.clusters import Topology


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


def display_config_type(config_type):
    """
    display config type based on input
    """
    if config_type == SQRT_DYNAMIC:
        print("#SQRT_DYNAMIC")
    elif config_type == LOG_DYNAMIC:
        print("#LOG_DYNAMIC")
    elif config_type == SQRT_STATIC:
        print("#SQRT_STATIC")
    elif config_type == LOG_STATIC:
        print("#LOG_STATIC")
    elif config_type == MIN_MAX_STATIC:
        print("#MIN_MAX_STATIC")
    elif config_type == MIN_MAX_DYNAMIC:
        print("#MIN_MAX_DYNAMIC")



SQRT_DYNAMIC = 0
LOG_DYNAMIC = 1
SQRT_STATIC = 2
LOG_STATIC = 3
MIN_MAX_STATIC = 4
MIN_MAX_DYNAMIC = 5


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
    parser.add_argument('-iwsconf', nargs=3, dest="iws_config",
                        type=int, help="interval config of \
                        input work size,\
                        (-iwsconf min_input_work_size\
                        max_input_work_size multiplicative_step)")
    parser.add_argument("-p", dest="processors",
                        default=4, type=int,
                        help="total number of processors")
    parser.add_argument("-iws", dest="work_size",
                        default=100, type=int,
                        help="Input Work Size")
    parser.add_argument("-l", dest="latency",
                        default=1, type=int,
                        help="latency for remote steal")
    parser.add_argument("-s", dest="seed", type=float,
                        default=clock(), help="random seed")
    parser.add_argument("-r", dest="runs",
                        default=1, type=int,
                        help="number of runs to execute")
    parser.add_argument("-tasks", dest="tasks", action="store_true",
                        help="use tree tasks")
    parser.add_argument("-adapt", dest="adaptive", action="store_true",
                        help="use adaptive tasks")
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
    parser.add_argument("-svgts", dest="svg_time_scal", default=100, type=int,
                        help="svg time scal")
    parser.add_argument("-blk_factor", dest="block_factor", default=2,
                        type=float)
    parser.add_argument("-itc", dest="init_task_cost", default=None,
                        type=int)
    parser.add_argument("-gbn", dest="geo_blk_number", default=None,
                        type=int)
    parser.add_argument("-config_type", dest="config_type", default=3,
                        type=int, help="0-sqrt_dynamic, 1-log_dynamic,\
                        2-sqrt_static, 3-log_static")

    arguments = parser.parse_args()

    print("#using seed", arguments.seed)
    seed(arguments.seed)

    if arguments.debug:
        activate_logs()

    if arguments.init_task_cost:
        init_task_cost(arguments.init_task_cost)

    if arguments.json_file_out:
        svg_time_scal(arguments.svg_time_scal)

    if arguments.block_factor:
        block_factor(arguments.block_factor)

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
        if not arguments.iws_config:
            works = [arguments.work_size]
        else:
            works = list(power_range(*arguments.iws_config))

    geo_blk_nb = arguments.geo_blk_number
    g_geo_blk_number(geo_blk_nb)
    geo_blk_max = None
    if arguments.config_type:
        display_config_type(arguments.config_type)

    print("#PROCESSORS: {}, RUNS: {}".format(
        arguments.processors,
        arguments.runs))
    print("#runTime\tprocessors\
    \tinput-work-size\tdepth\ttaskThreshold\tlGranularity\
    \trGranularity\tW0\tblock_factory\tinit_task_cost\twaiting-time\
    \tidle_time\ttask_creation_cost\tGeo_block_number\tinit_blk_size\tmax_blk_size")

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
                    for run_num in range(arguments.runs):
                        Task.tasks_number = 0
                        if arguments.tasks or \
                                arguments.json_file_in is not None:
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
                        elif arguments.adaptive:
                            if arguments.config_type == LOG_STATIC:
                                g_init_blk_size(init_blk_size(log2(work*wssim.INIT_TASK_COST), work))
                                if arguments.geo_blk_number is None:
                                    g_geo_blk_number(round(log2(sqrt(work * wssim.INIT_TASK_COST) / log2(work))))

                            elif arguments.config_type == SQRT_STATIC:
                                g_init_blk_size(init_blk_size(sqrt(work*wssim.INIT_TASK_COST), work))
                                if arguments.geo_blk_number is None:
                                    g_geo_blk_number(0)

                            elif arguments.config_type == MIN_MAX_STATIC:
                                g_init_blk_size(init_blk_size(log2(work*wssim.INIT_TASK_COST), work))
                                geo_blk_max = init_blk_size(sqrt(work*wssim.INIT_TASK_COST), work)

                            elif arguments.config_type == MIN_MAX_DYNAMIC:
                                g_geo_blk_number(None)

                            simulator.reset(work,
                                    AdaptiveTask(
                                        work, geo_blk_max, 0, arguments.config_type, geo_blk_nb,
                                        lambda left_size, right_size: DagTask(1,2),
                                        lambda size : size + wssim.INIT_TASK_COST,
                                        lambda n1, n2 : 1,
                                        )
                                    )
                            depth = 0
                            #simulator.reset(work,
                            #                AdaptiveTask(work, arguments.local_granularity, 0,
                            #                             lambda left_size, right_size:
                            #                             AdaptiveTask(left_size + right_size, arguments.local_granularity, 2,
                            #                                          lambda left_size, right_size: DagTask(1, 3),
                            #                                          lambda size: size,
                            #                                          lambda n1, n2: 1
                            #                                         ),
                            #                             lambda size: size * log2(size),
                            #                             lambda n1, n2: n1 + n2,
                            #                            )
                            #               )
                        else:
                            simulator.reset(work, DivisibleLoadTask(work))
                            depth = 0

                        simulator.run()
                        if arguments.json_file_out:
                            json_data = dict()
                            json_data["threads_number"] = arguments.processors
                            json_data["duration"] = simulator.time * wssim.SVGTS
                            json_data["tasks_number"] = len(simulator.graph)
                            simulator.graph.sort(key=operator.itemgetter('id'))
                            json_data["tasks_logs"] = simulator.graph

                            with open(arguments.json_file_out, 'w') as outfile:
                                json.dump(json_data,
                                          outfile, indent=4)

                        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\
                              \t{}\t{}\t{}\t{}\t{}\t{}"
                              .format(
                                  #probability,
                                  #latency,
                                  #simulator.steal_info["IWR"],
                                  # simulator.steal_info["SIWR"],
                                  #simulator.steal_info["EWR"],
                                  # simulator.steal_info["SEWR"],
                                  simulator.time,
                                  arguments.processors,
                                  work,
                                  depth,
                                  threshold,
                                  arguments.local_granularity,
                                  arguments.remote_granularity,
                                  simulator.steal_info["W0"],
                                  #simulator.steal_info["W1"],
                                  arguments.block_factor,
                                  wssim.INIT_TASK_COST,
                                  simulator.steal_info["waiting_time"],
                                  simulator.steal_info["idle_time"],
                                  len(simulator.graph)*wssim.INIT_TASK_COST,
                                  wssim.GEO_BLK_NUMBER,
                                  wssim.INIT_BLK_SIZE,
                                  geo_blk_max
                                  # simulator.steal_info["beginning"]
                              ))


if __name__ == "__main__":
    main()
