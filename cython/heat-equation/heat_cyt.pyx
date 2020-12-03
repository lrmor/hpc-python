cimport numpy as cnp
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Set the colormap
plt.rcParams['image.cmap'] = 'BrBG'

def evolve(cnp.ndarray[cnp.float_t,ndim=2] u, cnp.ndarray[cnp.float_t,ndim=2] u_previous, float a,  float dt,  float dx2,  float dy2):
    """Explicit time evolution.
       u:            new temperature field
       u_previous:   previous field
       a:            diffusion constant
       dt:           time step. """
    cdef int n, m, i, j
    n, m = np.shape(u)
    dx2inv = 1.0/dx2
    dy2inv = 1.0/dy2

    for i in range(1, n-1):
        for j in range(1, m-1):
            u[i, j] = u_previous[i, j] + a * dt * ( \
             (u_previous[i+1, j] - 2*u_previous[i, j] + \
              u_previous[i-1, j]) * dx2inv + \
             (u_previous[i, j+1] - 2*u_previous[i, j] + \
                 u_previous[i, j-1]) * dy2inv )
    u_previous[:] = u[:]

def iterate(cnp.ndarray[cnp.float_t,ndim=2] field, cnp.ndarray[cnp.float_t,ndim=2] field0, float a, float dx,float dy, int timesteps, int image_interval):
    """Run fixed number of time steps of heat equation"""
    cdef float dx2, dy2, dt
    cdef int m
#    cdef cnp.ndarray[cnp.float_t,ndim=2] cfield, cfield0
#    cfield = field
#    cfield0 = field0 
    dx2 = dx**2
    dy2 = dy**2

    # For stability, this is the largest interval possible
    # for the size of the time-step:
    dt = dx2*dy2 / ( 2*a*(dx2+dy2) )    

    for m in range(1, timesteps+1):
        evolve(field, field0, a, dt, dx2, dy2)
        if m % image_interval == 0:
            write_field(field, m)

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


