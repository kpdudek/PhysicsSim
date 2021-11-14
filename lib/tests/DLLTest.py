#!/usr/bin/env python3

import numpy as np
import ctypes
from numpy.ctypeslib import ndpointer

def main():
    lib = ctypes.CDLL('.\DLLTest.dll')

    lib.mult.argtypes = [ctypes.c_int,ctypes.c_int]
    lib.mult.restype = ctypes.c_int
    res = lib.mult(ctypes.c_int(2),ctypes.c_int(2))
    print(res)

    test_array = np.array([[1,2,3],[1,2,3]],dtype=np.double)
    r,c = test_array.shape
    lib.array_test.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"), ctypes.c_int]
    lib.array_test(test_array,c)

if __name__ == '__main__':
    main()