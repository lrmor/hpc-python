from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

msg = {'rank':rank}

if rank == 0:
    comm.send(msg, dest = 1)
    b = comm.recv(source = 1)
    print(rank, b)

elif rank == 1:
    comm.send(msg, dest = 0)
    b = comm.recv(source = 0)
    print(rank, b)


