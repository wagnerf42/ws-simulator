#!/usr/bin/python3
"""
compute average time for each latency
"""
from collections import defaultdict
import sys

def main(filename):
    """
    generate 3d data for min for given processors number
    """
    average_times = parse(filename)
    for latency in range(2, 41, 4):
        print(latency, average_times[latency])

def parse(filename):
    """
    return column1 value when column2 is minimized
    """
    data_file = filename
    times = defaultdict(list)
    with open(data_file, "r") as data:
        for line in data:
            if line[0] == "#":
                continue
            latency, value = [int(v) for v in line.split(" ")]
            times[latency].append(value)

    average_times = dict()
    for latency, values in times.items():
        average_times[latency] = sum(values)/len(values)

    return average_times

main(sys.argv[1])
