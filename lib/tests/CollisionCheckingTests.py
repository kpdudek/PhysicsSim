#!/usr/bin/env python3

import os,sys, time, ctypes
import numpy as np
from matplotlib import pyplot as plt
from numpy.ctypeslib import ndpointer

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

    cc_fun.min_dist_point_to_line_test.restype = ctypes.c_double
    dist = cc_fun.min_dist_point_to_line_test()
    print(f'Min Dist Result: {dist}')

    # Circle Circle collision check
    cc_fun.circle_circle.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double]
    cc_fun.circle_circle.restype = ctypes.c_int
    circ_1 = np.array([1.0,1.0])
    circ_2 = np.array([4.0,1.0])
    rad_1 = 3.0
    rad_2 = 3.0
    res = cc_fun.circle_circle(circ_1,rad_1,circ_2,rad_2)
    logger.log(f'Circle Circle collision check: {res}')

    # Circle Rect collision check
    cc_fun.circle_rect.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ctypes.c_double]
    cc_fun.circle_rect.restype = ctypes.c_double
    circ_1 = np.array([1.0,1.0])
    rad_1 = 1.0
    pose = np.array([1.0,1.0])
    width = 3.0
    height = 3.0
    tic = time.time()
    res = cc_fun.circle_rect(circ_1,rad_1,pose,width,height)
    toc = time.time()
    logger.log(f'Circle Rect collision check result: {res}')
    logger.log('Circle Rect collision check took: %f seconds'%(toc-tic))

    # Plotting
    plt.gca().set_aspect('equal')
    # plt.show()

if __name__ == '__main__':
    main()