
from mpi4py import MPI
from random import random

comm = MPI.COMM_WORLD

mydata = comm.rank

data = comm.allgather(mydata)

print(f"Rank: {comm.rank}, Data = ", data)



