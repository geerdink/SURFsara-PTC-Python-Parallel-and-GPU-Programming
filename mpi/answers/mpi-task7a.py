from mpi4py import MPI

comm = MPI.COMM_WORLD

# Alice; say Hello to Bob
if comm.rank == 0:
    comm.send("Hello Bob!", 1)
    mesg = comm.recv()
    print("Alice: Bob said '%s'" % mesg)

# Bob; say Hello to Alice
if comm.rank == 1:
    mesg = comm.recv()
    comm.send("Hello Alice!", 0)
    print("Bob: Alice said '%s'" % mesg)
