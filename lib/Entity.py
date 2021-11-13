#!/usr/bin/env python3

from lib.Physics2D import Physics2D
from lib.PaintUtils import PaintUtils
from lib.Logger import Logger
import numpy as np

class Entity(object):
    def __init__(self,config,fps,cc_fun,pose=None):
        super().__init__()
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.config = config
        self.fps = float(fps)
        self.default_color = self.paint_utils.random_color()
        self.physics_lock = False
        self.cc_fun = cc_fun

        self.mass = self.config['mass']
        self.physics = Physics2D(self.config,self.mass,self.cc_fun,self)
        if type(pose)==np.ndarray:
            self.physics.pose = pose
        else:
            self.physics.pose = np.array([self.config['pose'][0],self.config['pose'][1]])
        self.theta = 0.0

        self.tail_step = 0
        self.tail_step_max = 2
        self.tail = np.ones((2,10))
        self.tail[0,:] = self.tail[0,:]*self.physics.pose[0]
        self.tail[1,:] = self.tail[1,:]*self.physics.pose[1]

    def translate(self,vec):
        self.physics.pose = self.physics.pose + vec
    
    def teleport(self,pose):
        self.physics.pose = pose

    def update_physics(self,collision_bodies,forces,torques):
        if self.physics and not self.physics_lock:
            t = 1.0/self.fps
            resultant_force = self.physics.gravity_force
            for force in forces:
                resultant_force += force
            pose,theta = self.physics.accelerate(resultant_force,torques,t,collision_bodies)
            self.physics.pose = pose
            self.theta = theta
        
        if self.tail_step == self.tail_step_max:
            self.tail = self.tail[:,1:]
            append = self.physics.pose.copy()
            self.tail = np.hstack((self.tail,append.reshape(2,1)))
            self.tail_step = 0
        else:
            self.tail_step += 1
