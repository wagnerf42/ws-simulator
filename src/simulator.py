#!/usr/bin/env python3
"""
Simulation System configuration
"""

import argparse
from random import seed
from time import clock
import wssim
from wssim.simulator import Simulator
from wssim import activate_logs, init_remote_latency

def main():
    """
    main program to start Simulation
    """
    parser = argparse.ArgumentParser(
        description="simulate work stealing algorithm")
    parser.add_argument("-rsp", dest="remote_steal_probability",
                        default=0.25, type=float,\
                        help="probability of stealing remotely")
    parser.add_argument('-rspconf', nargs=3, dest="prbabilities_config",
                        type=float, help="interval config of \
                        stealing remotely probabilities ,\
                        (-rspconf min_probability max_probability step)")
    parser.add_argument('-lconf', nargs=3, dest="latencies_config",
                        type=int, help="interval config of \
                        latencies ,\
                        (-lconf min_latency max_latency step)")
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
    parser.add_argument("-d", dest="debug", action="store_true",
                        help="activate traces")
    parser.add_argument("-f", dest="log_file", default=None)
    arguments = parser.parse_args()

    print("#using seed", arguments.seed)
    seed(arguments.seed)


    if arguments.debug:
        activate_logs()

    if arguments.prbabilities_config and arguments.latencies_config:
        print("you can't use -lconf:{} and -rsps:{} in the same time".format(
            arguments.prbabilities_config, arguments.latencies_conf))

    simulator = Simulator(arguments.processors,
                          arguments.log_file)


    if not arguments.prbabilities_config and not arguments.latencies_config:
        print("#processors:{} remote_steal_latency:{}\
              remote_steal_proba:{}"\
              .format(arguments.processors,
                      wssim.REMOTE_STEAL_LATENCY,
                      arguments.remote_steal_probability))
        run_probability(simulator, arguments)
    elif arguments.prbabilities_config:
        proba_start, proba_end, proba_step = arguments.prbabilities_config
        probability = proba_start
        while probability <= proba_end:
            arguments.remote_steal_probability = probability
            print("#processors:{} remote_steal_latency:{}\
                  remote_steal_proba:{}".format(
                      arguments.processors,
                      wssim.REMOTE_STEAL_LATENCY,
                      arguments.remote_steal_probability))
            run_probability(simulator, arguments)
            probability += proba_step
    else:
        latency_start, latency_end, latency_step = arguments.latencies_config
        for latency in range(latency_start, latency_end, latency_step):
            init_remote_latency(latency)
            simulator.update_latency(latency)
            print("#processors:{} remote_steal_latency:{}\
                  remote_steal_proba:{}".format(
                      arguments.processors,
                      wssim.REMOTE_STEAL_LATENCY,
                      arguments.remote_steal_probability))
            run_latency(simulator, arguments)

def run_probability(simulator, arguments):
    """
    compute simulation for one probability
    """
    for _ in range(arguments.runs):
        simulator.reset(arguments.work, arguments.remote_steal_probability)
        simulator.run()
        print(arguments.remote_steal_probability, simulator.time)
       # print("RSP:{} time:{} IWR:{} EWR:{} SIWR:{} SEWR:{}".format(
       #     arguments.remote_steal_probability, simulator.time,
       #     len(simulator.steal_info["IWR"]),
       #     len(simulator.steal_info["EWR"]),
       #     len(simulator.steal_info["SIWR"]),
       #     len(simulator.steal_info["SEWR"])
       # ))


def run_latency(simulator, arguments):
    """
    compute simulation for one probability
    """
    for _ in range(arguments.runs):
        simulator.reset(arguments.work, arguments.remote_steal_probability)
        simulator.run()
        print(wssim.REMOTE_STEAL_LATENCY, simulator.time)
       # print("RSP:{} time:{} IWR:{} EWR:{} SIWR:{} SEWR:{}".format(
       #     arguments.remote_steal_probability, simulator.time,
       #     len(simulator.steal_info["IWR"]),
       #     len(simulator.steal_info["EWR"]),
       #     len(simulator.steal_info["SIWR"]),
       #     len(simulator.steal_info["SEWR"])
       # ))

if __name__ == "__main__":
    main()
