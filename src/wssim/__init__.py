#!/usr/bin/env python3.5
"""
main module for simulator.
"""
LOGGING = False

SVGTS = 100


def activate_logs():
    """
    activate all logs on stdout
    """
    print("activating logs")
    global LOGGING
    LOGGING = True


def svg_time_scal(set_svg_time_scal):
    """
    set unit to visualise the svg
    """
    global SVGTS
    SVGTS = set_svg_time_scal
