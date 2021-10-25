#!/usr/bin/env python3

import os,sys, time, ctypes
import numpy as np
from matplotlib import pyplot as plt

path = os.getcwd()
sys.path.insert(1,os.path.dirname(path))
import Geometry as geom
from Logger import Logger, FilePaths

def main():
    logger = Logger()
    file_paths = FilePaths()
    
    cc_fun = ctypes.CDLL(f'{os.path.dirname(path)}/{file_paths.cc_lib_path}')
    res = cc_fun.get_library_version()
    logger.log(f"C collision checking library version: {res}")

    cc_fun.sphere_collision_check_test.restype = ctypes.c_double
    res = cc_fun.sphere_collision_check_test()
    logger.log(f'Circle collision check: {res}')

    plt.gca().set_aspect('equal')
    # plt.show()

if __name__ == '__main__':
    main()