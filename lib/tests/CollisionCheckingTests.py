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

    # Circle Circle collision check
    cc_fun.circle_circle.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.c_double]
    cc_fun.circle_circle.restype = ctypes.c_int
    circ_1 = np.array([1,1]) #.astype(np.double)
    circ_2 = np.array([4,1]) #.astype(np.double)
    circ_1_pass = circ_1.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    circ_2_pass = circ_2.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    rad_1 = ctypes.c_double(3.0)
    rad_2 = ctypes.c_double(3.0)
    res = cc_fun.circle_circle(circ_1_pass,rad_1,circ_2_pass,rad_2)
    logger.log(f'Circle Circle collision check: {res}')

    # Circle Rect collision check
    cc_fun.circle_rect.argtypes = [ctypes.POINTER(ctypes.c_double),ctypes.c_double,ctypes.POINTER(ctypes.c_double),ctypes.c_double,ctypes.c_double]
    cc_fun.circle_rect.restype = ctypes.c_int
    circ_1 = np.array([1.0,1.0])
    rad_1 = ctypes.c_double(1.0)
    pose = np.array([1.0,1.0])
    width = ctypes.c_double(3.0)
    height = ctypes.c_double(3.0)
    circ_1_pass = circ_1.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    pose_pass = pose.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    res = cc_fun.circle_rect(circ_1_pass,rad_1,pose_pass,width,height)
    logger.log(f'Circle Rect collision check: {res}')

    # Plotting
    plt.gca().set_aspect('equal')
    # plt.show()

if __name__ == '__main__':
    main()