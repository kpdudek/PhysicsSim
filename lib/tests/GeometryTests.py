#!/usr/bin/env python3

import os,sys, time
import numpy as np
from matplotlib import pyplot as plt

path = os.getcwd()
sys.path.insert(1,os.path.dirname(path))
import Geometry as geom

def min_dist_point_to_line_test():
    A = np.array([0,0])
    B = np.array([10,10])
    P = np.array([3,5])

    tic = time.time()
    dist,C = geom.min_dist_point_to_line(P,A,B)
    toc = time.time()
    print(f'Minimun distance: {dist}')
    print(f'Point of intersection: {C}')
    print('Distance check took (s): %f'%(toc-tic))
    plt.plot([A[0],B[0]],[A[1],B[1]],'bo-')
    plt.plot(P[0],P[1],'ko')
    plt.plot([P[0],C[0]],[P[1],C[1]],'r')

def main():
    min_dist_point_to_line_test()
    plt.gca().set_aspect('equal')
    plt.show()

if __name__ == '__main__':
    main()