#!/usr/bin/env python3.5

import sys
from collections import defaultdict

def write_head(title="", with_title=False):
    """
    write the firste line of the latex documents
    """
    print("\documentclass{article} ")
    print("\\"+"usepackage[paper=portrait,pagesize]{typearea}")
    print("\\"+"usepackage[left=0.2cm,right=2cm,top=0.2cm,bottom=2cm]{geometry} ")

    if with_title:
        print("\\title{"+title+"}")

    print("\\"+"begin{document}")
    print("\KOMAoptions{paper=landscape,pagesize}")
    print("\\"+"recalctypearea")


    if with_title:
        print("\\maketitle")


def write_end_file():
    print("\end{document}")


def read_file(workfile):
    """
    read file frome execution trace
    """
    num_line = 0
    f = open(workfile, 'r')
    lines = f.readlines()
    values = list()
    for line in lines:
        if num_line == 1:
            title = line.rstrip('\n')
        if num_line == 2 :
            keys = line.rstrip('\n').split('\t')
        if num_line > 2 :
            value = line.rstrip('\n').split('\t')
            values.append(value)
        num_line = num_line + 1
    f.close()

    return keys, values, title


def write_table_per_graphe(graph_name, keys, values):
    """
    write table of graph
    """
    nb_keys = len(keys)
    nb_simulation = len(values)
    print("\\textbf{"+graph_name+"}\\\\")

    print("\\begin{tabular}{|", end='')
    print(''.join( ['c|' for i in range(nb_keys)]), "}  ")

    print("\\hline")

    

    for i in range(nb_keys-1):
        print(keys[i].replace("#", ""), " & ", end='')

    print(keys[nb_keys-1], "\\\\")
    print("\\hline")

    for i in range(nb_simulation-1):
    #    assert(nb_keys == len(values[i]))
        for v in range(nb_keys-1):
            print(values[i][v], " & ", end='')
        print(values[i][nb_keys-1], " \\\\")

        print("\\hline")

    print("\\end{tabular}")



def run():

    write_head(title="rapport", with_title=True)
    keys, values, title = read_file("test")


    write_table_per_graphe(title.replace('#',''), keys, values)
    write_end_file()

if __name__ == "__main__":
    run()
