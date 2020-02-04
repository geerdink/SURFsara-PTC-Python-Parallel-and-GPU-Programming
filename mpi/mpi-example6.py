# mpi-example6.py
from mpi4py import MPI
comm = MPI.COMM_WORLD

if comm.rank == 0:
    comm.send("Hello world", 1)
else:
    message = comm.recv()
    print(f"Rank {comm.rank} received '%s'" %
          message)

