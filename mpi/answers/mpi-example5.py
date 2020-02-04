
from mpi4py import MPI
from random import random

comm = MPI.COMM_WORLD

n = 10000
count = 0

for i in range(int(n / comm.size)):
    (x,y) = (random(), random())
    if x * x + y * y < 1.0:
        count += 1

total = comm.reduce(count, MPI.SUM )

if comm.rank == 0:
    print("pi = %9.7f" % (4.0 * total / n) )


