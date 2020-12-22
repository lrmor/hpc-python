from __future__ import print_function
import numpy as np
import time
from mpi4py import MPI

# TODO: initialise MPI by importing it

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Set the colormap
plt.rcParams['image.cmap'] = 'BrBG'

# Basic parameters
a = 0.5                # Diffusion constant
timesteps = 200        # Number of time-steps to evolve system
image_interval = 4000  # Write frequency for png files

# Grid spacings
dx = 0.01
dy = 0.01
dx2 = dx**2
dy2 = dy**2

# For stability, this is the largest interval possible
# for the size of the time-step:
dt = dx2*dy2 / ( 2*a*(dx2+dy2) )

# MPI globals
# TODO: find out your rank and communicator size
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Up/down neighbouring MPI ranks
up = rank - 1
down = rank + 1
# TODO: if at the edge of the grid, use MPI.PROC_NULL
#--------------------------------------------------------------------------
if rank == 0:
    up = MPI.PROC_NULL
if rank == size-1:
    down = MPI.PROC_NULL
#--------------------------------------------------------------------------
def evolve(u, u_previous, a, dt, dx2, dy2):
    """Explicit time evolution.
       u:            new temperature field
       u_previous:   previous field
       a:            diffusion constant
       dt:           time step
       dx2:          grid spacing squared, i.e. dx^2
       dy2:            -- "" --          , i.e. dy^2"""

    u[1:-1, 1:-1] = u_previous[1:-1, 1:-1] + a * dt * ( \
            (u_previous[2:, 1:-1] - 2*u_previous[1:-1, 1:-1] + \
             u_previous[:-2, 1:-1]) / dx2 + \
            (u_previous[1:-1, 2:] - 2*u_previous[1:-1, 1:-1] + \
                 u_previous[1:-1, :-2]) / dy2 )
    u_previous[:] = u[:]

def init_fields(filename):
    # Read the initial temperature field from file
    field = np.loadtxt(filename)
    field0 = field.copy() # Array for field of previous time step
    return field, field0

def write_field(field, step):
    plt.gca().clear()
    plt.imshow(field)
    plt.axis('off')
    plt.savefig('heat_{0:03d}.png'.format(step))

def exchange(field):
    # TODO: select border rows from the field and add MPI calls to
    #       exchange them with the neighbouring tasks
    # send down, receive from up
#--------------------------------------------------------------------------
    sbuf = field[-2,:]  # last row of real data
    rbuf = field[0,:]  # ghost row
    comm.Sendrecv(sbuf, dest=down, recvbuf = rbuf, source = up)
    # send up, receive from down
    sbuf = field[1,:]  # first row of real data
    rbuf = field[-1,:]  # ghost row
    comm.Sendrecv(sbuf, dest = up, recvbuf = rbuf, source = down)
#--------------------------------------------------------------------------

def iterate(field, local_field, local_field0, timesteps, image_interval):
    for m in range(1, timesteps+1):
        exchange(local_field0)
        evolve(local_field, local_field0, a, dt, dx2, dy2)
        if m % image_interval == 0:
#--------------------------------------------------------------------------
            # TODO: gather partial fields to reconstruct the full field
            comm.Gather(...)
#--------------------------------------------------------------------------
            if rank == 0:
                write_field(field, m)


def main():
    # Read and scatter the initial temperature field
    if rank == 0:
        field, field0 = init_fields('bottle_large.dat')
        shape = field.shape
        dtype = field.dtype
        print("rank0",field.dtype)
#--------------------------------------------------------------------------
        # TODO: send the shape and dtype to everyone else
        sptp = {'shape':shape, 'dtype':dtype}
#--------------------------------------------------------------------------
    else:
        field = None
        sptp = {}
#--------------------------------------------------------------------------
        # TODO: receive the shape and dtype
    bsptp = comm.bcast(sptp, root = 0) 
    shape = bsptp["shape"]
#--------------------------------------------------------------------------
    if shape[0] % size:
        raise ValueError('Number of rows in the temperature field (' \
                + str(shape[0]) + ') needs to be divisible by the number ' \
                + 'of MPI tasks (' + str(size) + ').')
    n = int(shape[0] / size)  # number of rows for each MPI task
    m = shape[1]         # number of columns in the field

    # TODO: scatter a portion of the field to each MPI task
#--------------------------------------------------------------------------
    xxtype = bsptp["dtype"]
    print(xxtype)
    print(type(xxtype))
#    buff = np.zeros((n,m), dtype = bsptp["dtype"]) 
    buff = np.zeros((n, m), xxtype)
# receive buffer for (n,m) elements of dtype
    comm.Scatter(field, buff, root = 0)

#--------------------------------------------------------------------------
    # TODO: construct local field based on the received data
    #       Note: remember to add two ghost rows (one on each side)
#--------------------------------------------------------------------------
#    if rank == 0:
#        local_field = np.r_[np.zeros(m), buff, field[rank*n+n,:]]
#    elif rank == size-1:
#        local_field = np.r_[field[rank*n-1,:] , buff, np.zeros(m)]
#    else:
#        local_field = np.r_[field[rank*n-1,:] , buff, field[rank*n+n,:]]
#
    local_field = np.zeros((n+2,m),xxtype)
    local_field[1:-1,:] = buff
#--------------------------------------------------------------------------
    local_field0 = np.zeros_like(local_field)  # array for previous time step
    # Fix outer boundary ghost layers to account for aperiodicity?
    if True:
        if rank == 0:
            local_field[0,:] = local_field[1,:]
        if rank == size - 1:
            local_field[-1,:] = local_field[-2,:]
    local_field0[:] = local_field[:]

    # Plot/save initial field
    if rank == 0:
        write_field(field, 0)
    # Iterate
    t0 = time.time()
    iterate(field, local_field, local_field0, timesteps, image_interval)
    t1 = time.time()
    # Plot/save final field
#--------------------------------------------------------------------------
    # TODO: gather partial fields to reconstruct the full field
    comm.Gather(local_field[1:-1,:], field, root = 0)
#--------------------------------------------------------------------------
    if rank == 0:
        write_field(field, timesteps)
        print("Running time: {0}".format(t1-t0))

if __name__ == '__main__':
    main()
