#!/usr/bin/env python3
"""
Simulation System configuration
"""

import argparse
from random import seed
from time import clock
from wssim.simulator import Simulator
from wssim import activate_logs, init_remote_latency

def main():
    """
    main program to start Simulation
    """
    parser = argparse.ArgumentParser(
        description="simulate work stealing algorithm")
    parser.add_argument("-rp", dest="remote_steal_probability",
                        default=0.25, type=float,\
                        help="probability of stealing remotely")
    parser.add_argument("-p", dest="processors",
                        default=4, type=int,\
                        help="total number of processors")
    parser.add_argument("-w", dest="work",
                        default=100, type=int,\
                        help="total work")
    parser.add_argument("-l", dest="latency",
                        default=5, type=int,\
                        help="latency for remote steal")
    parser.add_argument("-s", dest="seed",
                        default=clock(), type=float,\
                        help="random seed")
    parser.add_argument("-r", dest="runs",
                        default=1, type=int,\
                        help="number of runs to execute")
    parser.add_argument("-d", dest="debug", action="store_true",
                        help="activate traces")
    parser.add_argument("-f", dest="log_file", default=None)
    arguments = parser.parse_args()
    seed(arguments.seed)

    if arguments.debug:
        activate_logs()

    init_remote_latency(arguments.latency)
    if __debug__:
        print("#using seed", arguments.seed)
    simulator = Simulator(arguments.processors,
                          arguments.remote_steal_probability,
                          arguments.log_file)

    for _ in range(arguments.runs):
        simulator.reset(arguments.work)
        simulator.run()
        print(arguments.remote_steal_probability, simulator.time)


if __name__ == "__main__":
    main()
