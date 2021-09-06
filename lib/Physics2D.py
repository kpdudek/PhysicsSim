#!/usr/bin/env python3

import lib.Geometry as geom
import numpy as np

class Physics2D(object):
    def __init__(self,config,mass,collision_bodies=None):
        self.config = config
        self.collision_bodies = collision_bodies
        self.pose = np.array([20.0,20.0])
        self.velocity = np.array([0.0,0.0])
        self.angle = 0.0
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

    def accelerate(self,force,time,collisions=True):
        acceleration = force / self.mass
        delta_v = acceleration * time

        if collisions:
            velocity = self.velocity.copy() + delta_v
            pose = self.pose.copy() + (velocity * time)
            res,reflect = self.collision_check(pose.reshape(2))
            if res:
                self.velocity[1] = 0.75 * reflect[1] * self.velocity[1]
                self.velocity[0] = 0.75 * reflect[0] * self.velocity[0]
            else:
                self.velocity = self.velocity + delta_v
                self.pose = self.pose + (self.velocity * time)
        else:
            self.velocity = self.velocity + delta_v
            self.pose = self.pose + (self.velocity * time)

        return self.pose.copy()
