#!/usr/bin/env python3

from lib.Physics2D import Physics2D
from lib.PaintUtils import PaintUtils
from lib.Logger import Logger

class Entity(object):
    def __init__(self,config,painter,pose,fps):
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.config = config
        self.painter = painter
        self.pose = pose
        self.fps = float(fps)
        self.default_color = self.paint_utils.random_color()
        self.physics = None
        self.physics_lock = False

    # TODO: move physics to the dynamic obstacle child class
    def add_physics(self,mass,collision_bodies=None):
        self.physics = Physics2D(self.config,mass,collision_bodies=collision_bodies)
        self.physics.pose = self.pose.copy()

    def update_physics(self,forces,torques):
        if self.physics and not self.physics_lock:
            time = 1.0/self.fps
            pose = self.physics.accelerate(self.physics.gravity_force,torques,time,collisions=True)
            self.pose = pose
    
    def translate(self,vec):
        self.pose = self.pose + vec
        if self.physics:
            self.physics.pose = self.physics.pose + vec
    
    def teleport(self,pose):
        self.pose = pose
        if self.physics:
            self.physics.pose = pose
    
    # def paint(self):
    #     if self.config['color'] == "None":
    #         return
        
    #     if self.config['type'] == 'circle':
    #         pen,brush = self.paint_utils.ball(self.default_color)
    #         self.painter.setPen(pen)
    #         self.painter.setBrush(brush)
    #         self.painter.drawEllipse(int(self.pose[0])-10,int(self.pose[1])-10,20,20)
        
    #     elif self.config['type'] == 'rect':
    #         pen,brush = self.paint_utils.ground()
    #         self.painter.setPen(pen)
    #         self.painter.setBrush(brush)
    #         self.painter.drawRect(int(self.pose[0]),int(self.pose[1]),self.config['width'],self.config['height'])

class DynamicEntity(Entity):
    def __init__(self,keys_pressed,debug_mode):
        super().__init__(keys_pressed,debug_mode)
 