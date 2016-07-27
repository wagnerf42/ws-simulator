#!/usr/bin/python3
from collections import defaultdict
import sys

def main(processors):
    """
    generate 3d data for min for given processors number
    """
    for work in range(10000, 60000, 10000):
        for latency in range(5, 30, 5):
            filename = "log_p{}_w{}_l{}.data".format(
                processors, work, latency)
            best_proba = parse(filename)
            print("{}\t{}\t{}".format(work, latency, best_proba))

def parse(filename):
    """
    return column1 value when column2 is minimized
    """
    data_file = filename
    times = defaultdict(list)
    with open(data_file, "r") as data:
        best_proba = None
        for line in data:
            if line[0] == "#":
                continue
            proba, value = [float(v) for v in line.split(" ")]
            times[proba].append(value)

    average_times = dict()
    for proba, values in times.items():
        average_times[proba] = sum(values)/len(values)
    best_proba = min(average_times.keys(), key=lambda p: average_times[p])

    return best_proba

main(int(sys.argv[1]))
