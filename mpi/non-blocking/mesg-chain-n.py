from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
ntasks = comm.Get_size()
mypid = comm.Get_rank()

smsg = np.full(10, mypid, dtype = int)
print('process', mypid, 'of', ntasks)
bf = np.empty(10, dtype = int)
destR = mypid + 1
srcR = mypid - 1
if mypid == ntasks - 1:
    destR = MPI.PROC_NULL
elif mypid == 0:
    scrR = MPI.PROC_NULL
req1 = comm.Isend(smsg, dest = destR)
req2 = comm.Irecv(bf, source = srcR)

req1.wait()
print(smsg.shape)
req2.wait()
print(mypid, bf[0])

    
