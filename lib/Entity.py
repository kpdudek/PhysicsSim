#!/usr/bin/env python3

from lib.Physics2D import Physics2D
from lib.PaintUtils import PaintUtils
from lib.Logger import Logger

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
    def __init__(self,config,pose,fps,collision_bodies):
        super().__init__(config,pose,fps)
        self.physics = None
        self.physics_lock = False
        
        self.mass = self.config['mass']
        self.physics = Physics2D(self.config,self.mass,collision_bodies)
        self.physics.pose = self.pose.copy()

    def update_physics(self,forces,torques):
        if self.physics and not self.physics_lock:
            time = 1.0/self.fps
            pose = self.physics.accelerate(self.physics.gravity_force,torques,time,collisions=True)
            self.pose = pose
 