from mpi4py import MPI
from random import random

comm = MPI.COMM_WORLD

mydata = comm.rank

data = comm.gather(mydata)

if comm.rank == 0:
    print("Data = ", data)
