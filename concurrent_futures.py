from concurrent import futures
import threading
import time

def task(n):
    return n / 10

ex = futures.ThreadPoolExecutor(max_workers=2)

results = ex.map(task, range (5, 0, -1))

real_results = list(results)
