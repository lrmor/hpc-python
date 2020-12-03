from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""
    void evolve(double *u, double *u_previous, int nx, int ny, double a, double dt, double dx2, double dy2);
""") 

ffibuilder.set_source("evolve_cmodule",
'''
   void evolve(double *u, double *u_previous, int nx, int ny, 
            double a, double dt, double dx2, double dy2);
''',
    sources = ["evolve.c"],
    library_dirs = ['.'],
    extra_compile_args = ['-O3'],
#    libraries = ['m']
)

ffibuilder.compile(verbose = True)     

