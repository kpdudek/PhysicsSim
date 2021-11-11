#!/usr/bin/env python3

from lib.Physics2D import Physics2D
from lib.PaintUtils import PaintUtils
from lib.Logger import Logger
import numpy as np

class Entity(object):
    def __init__(self,config,fps,pose=None):
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.config = config
        self.pose = np.array([self.config['pose'][0],self.config['pose'][1]])
        if type(pose)==np.ndarray:
            self.pose = pose
        self.theta = 0.0
        self.fps = float(fps)
        self.default_color = self.paint_utils.random_color()   
    
    def translate(self,vec):
        self.pose = self.pose + vec
    
    def teleport(self,pose):
        self.pose = pose

class DynamicEntity(Entity):
    def __init__(self,config,fps,cc_fun,pose=None):
        super().__init__(config,fps)
        self.physics = None
        self.physics_lock = False
        self.cc_fun = cc_fun
        if type(pose)==np.ndarray:
            self.pose = pose
        
        self.mass = self.config['mass']
        self.physics = Physics2D(self.config,self.mass,self.cc_fun,self)
        self.physics.pose = self.pose.copy()

        self.tail_step = 0
        self.tail_step_max = 2
        self.tail = np.ones((2,10))
        self.tail[0,:] = self.tail[0,:]*self.pose[0]
        self.tail[1,:] = self.tail[1,:]*self.pose[1]

    def translate(self,vec):
        self.pose = self.pose + vec
        self.physics.pose = self.physics.pose + vec
    
    def teleport(self,pose):
        self.pose = pose
        self.physics.pose = pose

    def update_physics(self,collision_bodies,forces,torques):
        if self.physics and not self.physics_lock:
            t = 1.0/self.fps
            pose,theta = self.physics.accelerate(self.physics.gravity_force,torques,t,collision_bodies)
            self.pose = pose
            self.theta = theta
        
        if self.tail_step == self.tail_step_max:
            self.tail = self.tail[:,1:]
            append = self.pose.copy()
            self.tail = np.hstack((self.tail,append.reshape(2,1)))
            self.tail_step = 0
        else:
            self.tail_step += 1
