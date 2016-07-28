"""
main module for simulator.
"""
LOGGING = False

def activate_logs():
    """
    activate all logs on stdout
    """
    print("activating logs")
    global LOGGING
    LOGGING = True
