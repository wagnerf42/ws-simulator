#!/usr/bin/env python3.5
"""
main module for simulator.
"""
LOGGING = False

SVGTS = 100

BLOCK_FACTOR = 2

INIT_TASK_COST = 4

GEO_BLK_NUMBER = None
INIT_BLK_SIZE = None

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


def g_geo_blk_number(geo_blk_number):
    """
    update geometric block number
    default valus is 0
    """
    global GEO_BLK_NUMBER
    GEO_BLK_NUMBER = geo_blk_number


def g_init_blk_size(init_blk_size):
    """
    update init blk task
    default valus is None
    """
    global INIT_BLK_SIZE
    INIT_BLK_SIZE = init_blk_size
