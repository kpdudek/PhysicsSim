#!/usr/bin/env python3

from PyQt5 import QtCore
from lib.Entity import DynamicEntity

from lib.PaintUtils import PaintUtils
from lib.Logger import Logger
import lib.Errors as errors
import numpy as np

class Camera(object):
    def __init__(self,frame_size,painter,scene):
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.frame_size = frame_size
        self.painter = painter
        self.scene = scene
        self.zoom_level = 1.0

        self.frames = {
            'camera':np.array([0.0,0.0]),
            'scene':np.array([0.0,0.0])
            }

        self.display_fps_overlay = True
        self.display_tails = False

    def translate(self,vec):
        self.frames['scene'] = self.frames['scene'] + vec

    def zoom(self,multiplier):
        self.zoom_level = multiplier

    def transform(self,point,parent_frame='camera',child_frame='scene'):
        '''
        Transforms a point from the parent frame to the child frame.
        Default behavior is camera frame -> scene frame.
        '''
        if child_frame not in list(self.frames.keys()):
            raise errors.FrameNotFound(child_frame)
        if parent_frame not in list(self.frames.keys()):
            raise errors.FrameNotFound(child_frame)
        
        coord = point + (self.frames[parent_frame] - self.frames[child_frame])
        return coord

    def clear_display(self,fps):
        pen,brush = self.paint_utils.set_color('light_gray',1)
        self.painter.setPen(pen)
        self.painter.setBrush(brush)
        self.painter.drawRect(0,0,self.frame_size[0],self.frame_size[1])

        if self.display_fps_overlay:
            pen,brush = self.paint_utils.set_color('black',1)
            self.painter.setPen(pen)
            self.painter.setBrush(brush)
            self.painter.drawText(3,13,200,75,QtCore.Qt.TextWordWrap,str(int(fps)))
    
    def paint_launch_controls(self):
        '''
            Draws an arrow indicator for the launch origin and velocity.
            Drawn in camera frame, so no transform is needed.
        '''
        if type(self.scene.launch_origin)==np.ndarray:
            pen,brush = self.paint_utils.set_color('white',1)
            self.painter.setPen(pen)
            self.painter.setBrush(brush)
            self.painter.drawEllipse(self.scene.launch_origin[0]-2,self.scene.launch_origin[1]-2,4,4)
            slope = np.array([-1*(self.scene.launch_point[0]-self.scene.launch_origin[0]),-1*(self.scene.launch_point[1]-self.scene.launch_origin[1])])
            val = self.scene.launch_origin + slope
            self.painter.drawLine(self.scene.launch_origin[0],self.scene.launch_origin[1],val[0],val[1])

    def paint_entity(self,entity):
        '''
            Draws both static and dynamic entities from the scene.
            Drawn in camera frame, so no transform is needed.
        '''
        if entity.config['type'] == 'circle':
            pen,brush = self.paint_utils.set_color(entity.default_color,entity.config['fill'])
            self.painter.setPen(pen)
            self.painter.setBrush(brush)
            pose = self.transform(entity.pose,parent_frame='scene',child_frame='camera')
            rad = entity.config['radius']
            self.painter.drawEllipse(pose[0]-rad,pose[1]-rad,rad*2,rad*2)
        
        elif entity.config['type'] == 'rect':
            pen,brush = self.paint_utils.set_color(entity.config['color'],entity.config['fill'])
            self.painter.setPen(pen)
            self.painter.setBrush(brush)
            pose = self.transform(entity.pose,parent_frame='scene',child_frame='camera')
            self.painter.drawRect(pose[0],pose[1],entity.config['width'],entity.config['height'])

        if type(entity)==DynamicEntity:
            if self.display_tails and np.linalg.norm(entity.physics.velocity)>20.0:
                pen,brush = self.paint_utils.set_color('green',3)
                self.painter.setPen(pen)
                self.painter.setBrush(brush)
                r,c = entity.tail.shape
                for idx in range(0,c-1):
                    p1 = self.transform(entity.tail[:,idx],parent_frame='scene',child_frame='camera')
                    p2 = self.transform(entity.tail[:,idx+1],parent_frame='scene',child_frame='camera')
                    self.painter.drawLine(p1[0],p1[1],p2[0],p2[1])

    def update(self):
        '''
            Draws all entities in the scene.
        '''
        for entity in self.scene.static_entities:
            self.paint_entity(entity)

        for entity in self.scene.dynamic_entities:
            self.paint_entity(entity)
                
