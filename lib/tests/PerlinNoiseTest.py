#!/usr/bin/env python3

import os,sys
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import numpy as np

path = os.getcwd()
sys.path.insert(1,os.path.dirname(path))
import Noise

def perlin_noise_test_1D():
    r,c = 1,10
    noise = Noise.generate_perlin_noise(r,c)
    noise = noise * 10
    plt.plot(range(c),noise.reshape(c),'bo-')
    plt.gca().set_aspect('equal')

def perlin_noise_test_2D():
    r,c = 100,100
    noise = Noise.generate_perlin_noise(r,c)
    noise = noise
    
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # Make data.
    X = np.arange(0, r, 1)
    Y = np.arange(0, c, 1)
    X, Y = np.meshgrid(X, Y)
    Z = noise

    # Plot the surface.
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)

def main():
    perlin_noise_test_2D()
    plt.show()

if __name__ == '__main__':
    main()