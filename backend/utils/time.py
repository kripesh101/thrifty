from time import time_ns

def time_ms():
    return time_ns() // 1000000
