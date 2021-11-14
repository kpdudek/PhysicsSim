#!/usr/bin/env python3

import os,sys, time, ctypes, math
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
    
    # Initialize Collision Checking Library
    cc_fun = ctypes.CDLL(f'{os.path.dirname(path)}/{file_paths.cc_lib_path}')
    res = cc_fun.get_library_version()
    logger.log(f"C collision checking library version: {res}")

    # Min Dist Point to Line test
    cc_fun.min_dist_point_to_line_test.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")]
    cc_fun.min_dist_point_to_line_test.restype = ctypes.c_double
    p = np.array([3.0,5.0])
    v1 = np.array([0.0,0.0])
    v2 = np.array([10.0,10.0])
    dist = cc_fun.min_dist_point_to_line_test(p,v1,v2)
    logger.log(f'Min Dist Result: {dist}')

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

    # Rect Rect collision check
    cc_fun.rect_rect.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ctypes.c_double,ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ctypes.c_double]
    cc_fun.rect_rect.restype = ctypes.c_double
    pose_1 = np.array([0.0,0.0])
    w1 = 5.0
    h1 = 5.0
    pose_2 = np.array([3.0,3.0])
    w2 = 5.0
    h2 = 5.0
    tic = time.time()
    res = cc_fun.rect_rect(pose_1,w1,h1,pose_2,w2,h2)
    toc = time.time()
    logger.log(f'Rect Rect collision check result: {res}')
    logger.log('Rect Rect collision check took: %f seconds'%(toc-tic))

    # Circle Poly collision check
    cc_fun.circle_poly.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_int]
    cc_fun.circle_poly.restype = ctypes.c_double
    pose = np.array([0.0,1.5])
    radius = 2.0
    poly = np.array([[0,3,3,0],[0,0,3,3]],dtype=np.double)
    r,c = poly.shape
    tic = time.time()
    res = cc_fun.circle_poly(pose,radius,poly,c)
    logger.log(f'Circle Poly collision check result: {res}')
    logger.log('Circle Poly collision check took: %f seconds'%(toc-tic))

    circ_points = 20
    circle = np.zeros((2,circ_points))
    theta = 0.0
    delta_theta = math.radians(360.0/float(circ_points))
    for i in range(20):
        circle[0,i] = math.cos(theta)+pose[0]
        circle[1,i] = math.sin(theta)+pose[1]
        theta += delta_theta
    circle = np.hstack((circle,circle[:,0].reshape(2,1)))
    plt.plot([0,1],[0,0],'r')
    plt.plot([0,0],[0,1],'g')
    plt.plot(circle[0,:],circle[1,:],'b')
    plt.plot(np.hstack((poly[0,:],poly[0,0])),np.hstack((poly[1,:],poly[1,0])),'k')
    
    # Plotting
    plt.gca().set_aspect('equal')
    plt.show()

if __name__ == '__main__':
    main()