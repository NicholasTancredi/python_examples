cimport cython
print("Cython says hello!")

# NOTE: decorator turns off bounds-checking for speed
@cython.boundscheck(False)
def array_sum(double[:, ::1] ndarray):
    """
        An ndarray function that returns a scalar.
    """
    cdef int m = ndarray.shape[0]
    cdef int n = ndarray.shape[1]
    # NOTE: iteration variables should be unsigned for speed
    cdef unsigned int i, j
    cdef double result = 0

    for i in range(m):
        for k in range(n):
            result += ndarray[i, k]

    return result
