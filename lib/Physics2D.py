#!/usr/bin/env python3

from lib.Logger import Logger
import lib.Geometry as geom
import numpy as np
from math import pi

class Physics2D(object):
    def __init__(self,config,mass,collision_bodies):
        self.config = config
        self.collision_bodies = collision_bodies
        self.logger = Logger()

        self.pose = np.array([20.0,20.0])
        self.velocity = np.array([0.0,0.0])
        self.max_velocity = 2000.0
        self.theta = 0.0
        self.theta_dot = 0.0

        self.I = 5.0
        self.mass = mass #kg
        self.gravity_force = np.array([0.0,self.mass * geom.meters_to_pixels(9.8)])
        self.obstacles = []

    def collision_check(self,pose):
        collision,reflect = False,np.array([1,1])

        if self.config['type'] == 'circle':
            for body in self.collision_bodies:
                collision,reflect = geom.circle_collision_check(pose,self.config['radius'],body)
                if collision:
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
            # self.logger.log(f'Delta X: {delta_x}')
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
