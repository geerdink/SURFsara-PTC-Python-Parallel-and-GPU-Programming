
from mpi4py import MPI

comm = MPI.COMM_WORLD

if comm.rank == 0:
  status = comm.isend("Hello", 1)
  # do something else . . .

  status.wait()

if comm.rank == 1:
  msg = comm.recv()

