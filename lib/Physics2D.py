#!/usr/bin/env python3

from lib.Logger import Logger, FilePaths
import lib.Geometry as geom
import numpy as np
from numpy.ctypeslib import ndpointer
from math import pi
import ctypes

class Physics2D(object):
    def __init__(self,config,mass,collision_bodies):
        self.config = config
        self.collision_bodies = collision_bodies
        self.logger = Logger()
        self.file_paths = FilePaths()

        self.pose = np.array([20.0,20.0])
        self.velocity = np.array([0.0,0.0])
        self.max_velocity = 2000.0
        self.theta = 0.0
        self.theta_dot = 0.0

        self.I = 5.0
        self.mass = mass #kg
        self.gravity_force = np.array([0.0,self.mass * geom.meters_to_pixels(9.8)])
        self.obstacles = []

        self.cc_fun = ctypes.CDLL(f'{self.file_paths.lib_path}/{self.file_paths.cc_lib_path}')
        # Circle Circle collision check
        self.cc_fun.circle_circle.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double]
        self.cc_fun.circle_circle.restype = ctypes.c_int
        # Circle Rect collision check
        self.cc_fun.circle_rect.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ctypes.c_double]
        self.cc_fun.circle_rect.restype = ctypes.c_double

    def collision_check(self,pose):
        collision,reflect = False,np.array([1,1])
        tol = 0.1
        if self.config['type'] == 'circle':
            for body in self.collision_bodies:
                # collision,reflect = geom.circle_collision_check(pose,self.config['radius'],body)
                res = self.cc_fun.circle_rect(pose,self.config['radius'],body.pose,body.config['width'],body.config['height'])
                if res != -999.0:
                    collision = True
                    if abs(res-1.57) < tol:
                        reflect[0] = -1
                    elif abs(res-0.0) < tol:
                        reflect[1] = -1
                    elif abs(res-3.14) < tol:
                        reflect[1] = -1
                    elif abs(res+1.57) < tol:
                        reflect[0] = -1
                    return collision,reflect
        return collision,reflect

    def rotational_acceleration(self,torque,time,collisions=True):
        #TODO: instead of returning a delta x, change the objects linear velocity since the two are coupled
        alpha = torque / self.I
        delta_theta_dot = alpha * time
        self.theta_dot = self.theta_dot + delta_theta_dot
        self.theta = self.theta + (self.theta_dot * time)
        if self.config['type'] == 'circle':
            delta_x = (2*pi*self.config['radius'])*self.theta
        return delta_x

    def accelerate(self,force,torque,time,collisions=True):
        acceleration = force / self.mass
        delta_v = acceleration * time

        if collisions:
            velocity = self.velocity.copy() + delta_v
            pose = self.pose.copy() + (velocity * time)
            res,reflect = self.collision_check(pose.reshape(2))
            if res:
                self.velocity[1] = 0.75 * reflect[1] * self.velocity[1]
                self.velocity[0] = 0.75 * reflect[0] * self.velocity[0]
                delta_x = self.rotational_acceleration(torque,time,collisions=True)
                self.pose[0] = self.pose[0] + delta_x
            else:
                self.velocity = self.velocity + delta_v
                self.pose = self.pose + (self.velocity * time)
        else:
            self.velocity = self.velocity + delta_v
            self.pose = self.pose + (self.velocity * time)

        # TODO: cap the velocity so that the direction stays the same
        if abs(self.velocity[0]) > self.max_velocity:
            self.velocity[0] = self.max_velocity * np.sign(self.velocity[0])
        if abs(self.velocity[1]) > self.max_velocity:
            self.velocity[1] = self.max_velocity * np.sign(self.velocity[1])

        return self.pose.copy()
