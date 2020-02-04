from mpi4py import MPI

comm = MPI.COMM_WORLD

# FIXME: there is something going wrong with the communication

# Alice; say Hello to Bob
if comm.rank == 0:
    status = comm.isend("Hello Bob!", 1)
    status.wait()
    mesg = comm.recv()
    print("Alice: Bob said '%s'" % mesg)

# Bob; say Hello to Alice
if comm.rank == 1:
    status = comm.isend("Hello Alice!", 0)
    status.wait()
    mesg = comm.recv()
    print("Bob: Alice said '%s'" % mesg)
