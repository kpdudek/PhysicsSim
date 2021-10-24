#!/usr/bin/env python3

import os,sys, time
import numpy as np
from matplotlib import pyplot as plt

path = os.getcwd()
sys.path.insert(1,os.path.dirname(path))
import Geometry as geom

def main():
    plt.gca().set_aspect('equal')
    plt.show()

if __name__ == '__main__':
    main()