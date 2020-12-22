from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
ntasks = comm.Get_size()
mypid = comm.Get_rank()

smsg = np.full(10, mypid, dtype = int)
print('process', mypid, 'of', ntasks)
if mypid < ntasks - 1:
    comm.Send(smsg, dest = mypid +1) 
    print(smsg.shape)
if mypid >= 1:
    bf = np.empty(10, dtype = int)
    comm.Recv(bf, source = mypid - 1)
    print(mypid, bf[0])

    
