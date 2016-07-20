"""
main module for simulator.
"""
LOGGING = False

LOCAL_STEAL_LATENCY = 1
REMOTE_STEAL_LATENCY = 5

def activate_logs():
    """
    activate all logs on stdout
    """
    print("activating logs")
    global LOGGING
    LOGGING = True

def init_remote_latency(remote_latency):
    """
    update latency for remote steal
    """
    global REMOTE_STEAL_LATENCY
    REMOTE_STEAL_LATENCY = remote_latency
