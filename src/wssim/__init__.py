#!/usr/bin/env python3.5
"""
main module for simulator.
"""
LOGGING = False

UNIT = 100

def activate_logs():
    """
    activate all logs on stdout
    """
    print("activating logs")
    global LOGGING
    LOGGING = True



def set_unit(unit):
    """
    set unit to visualise the svg
    """
    global UNIT
    UNIT = unit
