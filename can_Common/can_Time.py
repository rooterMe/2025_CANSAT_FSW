import time


def Time_Init() :
    start_time = time.monotonic_ns()


def Time_Return():
    ns_time = (time.time_ns() % 1000000000) // 1000
    # ms_time = ns_time // 1000000
    # ns_time = ns_time // 1000

    timestamp = time.time()
    local_time = time.localtime(timestamp)
    formatted = time.strftime("%Y%m%d_%H%M%S", local_time)

    return formatted + str(ns_time)


def Time_Return_second():

    timestamp = time.time()
    local_time = time.localtime(timestamp)
    formatted = time.strftime("%Y%m%d_%H%M%S", local_time)

    return formatted
