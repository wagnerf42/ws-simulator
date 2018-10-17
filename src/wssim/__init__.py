#!/usr/bin/env python3.5
"""
main module for simulator.
"""
LOGGING = False

SVGTS = 100

BLOCK_FACTOR = 2


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
