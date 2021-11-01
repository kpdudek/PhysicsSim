#!/usr/bin/env python3

import ctypes

def main():
    lib = ctypes.CDLL('.\DLLTest.dll')

    lib.mult.argtypes = [ctypes.c_int,ctypes.c_int]
    lib.mult.restype = ctypes.c_int
    res = lib.mult(ctypes.c_int(2),ctypes.c_int(2))
    print(res)

if __name__ == '__main__':
    main()