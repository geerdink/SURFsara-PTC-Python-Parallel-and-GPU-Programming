# mpi-example1.py
from mpi4py import MPI

comm = MPI.COMM_WORLD

print("rank: ", comm.rank, " size: ", comm.size)

