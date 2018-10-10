#!/usr/bin/env python3.5
"""
main module for simulator.
"""
LOGGING = False

SVGTS = 100

BLOCK_FACTORY = (1 + 5 ** 0.5) / 2


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


def block_factory(block_factory):
    """
    set block factory
    default value is phi
    """
    global BLOCK_FACTORY
    BLOCK_FACTORY = block_factory
