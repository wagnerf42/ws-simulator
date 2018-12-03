#!/usr/bin/env python3.5
"""
main module for simulator.
"""
LOGGING = False

SVGTS = 100

BLOCK_FACTOR = 2

INIT_TASK_COST = 4

GEOM_BLOCK_NUMBER = 0

def activate_logs():
    """
    activate all logs on stdout
    """
    print("activating logs")
    global LOGGING
    LOGGING = True


def svg_time_scal(set_svg_time_scal):
    """
    set svg time scal
    """
    global SVGTS
    SVGTS = set_svg_time_scal


def block_factor(block_factor):
    """
    set block factor
    default value is phi
    """
    global BLOCK_FACTOR
    BLOCK_FACTOR = block_factor

def init_task_cost(init_task_cost):
    """
    update init tasks cost
    default valus is 4
    """
    global INIT_TASK_COST
    INIT_TASK_COST = init_task_cost


def geom_block_number(geom_block_number):
    """
    update init tasks cost
    default valus is 4
    """
    global GEOM_BLOCK_NUMBER
    GEOM_BLOCK_NUMBER = geom_block_number
