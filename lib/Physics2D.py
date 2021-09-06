#!/usr/bin/env python3

import lib.Geometry as geom
import numpy as np

class Physics2D(object):
    def __init__(self,config,mass,frame_size,collision_bodies=None):
        self.config = config
        self.frame_size = frame_size
        self.collision_bodies = collision_bodies
        self.pose = np.array([20.0,20.0])
        self.velocity = np.array([0.0,0.0])
        self.angle = 0.0
        self.mass = mass #kg
        self.gravity_force = np.array([0.0,self.mass * geom.meters_to_pixels(9.8)])
        self.obstacles = []

    def collision_check(self,pose):
        for body in self.collision_bodies:
            if body.config['type']=='rect':
                edges = []
                edges.append([np.array([body.pose[0],body.pose[1]]),np.array([body.pose[0]+body.config['width'],body.pose[1]])])
                edges.append([np.array([body.pose[0]+body.config['width'],body.pose[1]]),np.array([body.pose[0]+body.config['width'],body.pose[1]+body.config['height']])])
                edges.append([np.array([body.pose[0]+body.config['width'],body.pose[1]+body.config['height']]),np.array([body.pose[0],body.pose[1]+body.config['height']])])
                edges.append([np.array([body.pose[0],body.pose[1]+body.config['height']]),np.array([body.pose[0],body.pose[1]])])
                for edge in edges:
                    min_dist,C = geom.min_dist_point_to_line(pose,edge[0],edge[1])
                    if  min_dist <= self.config['radius']:
                        if edge[0][0] == edge[1][0]:
                            reflect = np.array([-1,1])
                        else:
                            reflect = np.array([1,-1])
                        return True,reflect
        self.walls = []
        self.walls.append([np.array([0,0]),np.array([self.frame_size[0],0])])
        self.walls.append([np.array([self.frame_size[0],0]),np.array([self.frame_size[0],self.frame_size[1]])])
        self.walls.append([np.array([self.frame_size[0],self.frame_size[1]]),np.array([0,self.frame_size[1]])])
        self.walls.append([np.array([0,self.frame_size[1]]),np.array([0,0])])
        for wall in self.walls:
            min_dist,C = geom.min_dist_point_to_line(pose,wall[0],wall[1])
            if  min_dist <= self.config['radius']:
                if wall[0][0] == wall[1][0]:
                    reflect = np.array([-1,1])
                else:
                    reflect = np.array([1,-1])
                return True,reflect
        
        return False,np.array([1,1])

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
