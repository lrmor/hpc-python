from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

a = np.empty(100000, dtype = int)
a[:] = rank
bf = np.empty(100000, dtype = int)

if rank ==0:
    comm.Send(a, dest = 1)
    comm.Recv(bf, source = 1)
    print(rank, bf[0])
if rank ==1:
    comm.Recv(bf, source = 0)
    comm.Send(a, dest = 0)
    print(rank, bf[0])
    
    
