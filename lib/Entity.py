#!/usr/bin/env python3

from lib.Physics2D import Physics2D
from lib.PaintUtils import PaintUtils
from lib.Logger import Logger
import numpy as np
import time

class Entity(object):
    def __init__(self,config,pose,fps):
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.config = config
        self.pose = pose
        self.fps = float(fps)
        self.default_color = self.paint_utils.random_color()   
    
    def translate(self,vec):
        self.pose = self.pose + vec
        if self.physics:
            self.physics.pose = self.physics.pose + vec
    
    def teleport(self,pose):
        self.pose = pose
        if not self.config['static']:
            self.physics.pose = pose

class DynamicEntity(Entity):
    def __init__(self,config,pose,fps,collision_bodies,cc_fun):
        super().__init__(config,pose,fps)
        self.physics = None
        self.physics_lock = False
        self.collision_bodies = collision_bodies
        self.cc_fun = cc_fun
        
        self.mass = self.config['mass']
        self.physics = Physics2D(self.config,self.mass,self.collision_bodies,self.cc_fun)
        self.physics.pose = self.pose.copy()

        self.tail_step = 0
        self.tail_step_max = 2
        self.tail = np.ones((2,10))
        self.tail[0,:] = self.tail[0,:]*self.pose[0]
        self.tail[1,:] = self.tail[1,:]*self.pose[1]

    def update_physics(self,forces,torques):
        if self.physics and not self.physics_lock:
            t = 1.0/self.fps
            pose = self.physics.accelerate(self.physics.gravity_force,torques,t,collisions=True)
            self.pose = pose
        
        if self.tail_step == self.tail_step_max:
            self.tail = self.tail[:,1:]
            append = self.pose.copy()
            self.tail = np.hstack((self.tail,append.reshape(2,1)))
            self.tail_step = 0
        else:
            self.tail_step += 1
