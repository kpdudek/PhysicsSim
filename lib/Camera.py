#!/usr/bin/env python3

from PyQt5 import QtCore

from lib.PaintUtils import PaintUtils
from lib.Logger import Logger
import lib.Geometry as geom
import lib.Errors as errors
import numpy as np

class Camera(object):
    def __init__(self,frame_size,painter,scene,game_manager):
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.frame_size = frame_size
        self.painter = painter
        self.scene = scene
        self.zoom_level = 1.0
        self.game_manager = game_manager

        self.frames = {
            'camera':np.array([0.0,0.0]),
            'scene':np.array([0.0,0.0])
            }

        self.display_fps_overlay = True
        self.display_tails = False

    def reset(self):
        self.teleport(np.zeros((2)))

    def teleport(self,pose):
        self.frames['scene'] = pose
    
    def translate(self,vec):
        self.frames['scene'] = self.frames['scene'] + -1*vec

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
        self.paint_utils.set_color(self.painter,'light_gray',True)
        self.painter.drawRect(0,0,self.frame_size[0],self.frame_size[1])

        if self.display_fps_overlay:
            self.paint_utils.set_color(self.painter,'black',True)
            self.painter.drawText(3,13,200,75,QtCore.Qt.TextWordWrap,str(int(fps)))
    
    def paint_launch_controls(self):
        '''
            Draws an arrow indicator for the launch origin and velocity.
            Drawn in camera frame, so no transform is needed.
        '''
        if type(self.scene.launch_origin)==np.ndarray:
            self.paint_utils.set_color(self.painter,'white',True)
            self.painter.drawEllipse(self.scene.launch_origin[0]-2,self.scene.launch_origin[1]-2,4,4)
            slope = np.array([-1*(self.scene.launch_point[0]-self.scene.launch_origin[0]),-1*(self.scene.launch_point[1]-self.scene.launch_origin[1])])
            val = self.scene.launch_origin + slope
            self.painter.drawLine(self.scene.launch_origin[0],self.scene.launch_origin[1],val[0],val[1])

    def paint_entity(self,entity):
        '''
            Draws both static and dynamic entities from the scene.
            Drawn in camera frame, so no transform is needed.
        '''
        pose = self.transform(entity.physics.pose,parent_frame='scene',child_frame='camera')

        if entity.config['type'] == 'circle':
            self.paint_utils.set_color(self.painter,entity.default_color,entity.config['fill'])
            rad = entity.config['radius']
            self.painter.drawEllipse(pose[0]-rad,pose[1]-rad,rad*2,rad*2)
            if self.game_manager.debug_mode:
                self.paint_utils.set_color(self.painter,'black',0)
                self.painter.drawEllipse(pose[0]-rad,pose[1]-rad,rad*2,rad*2)
        
        elif entity.config['type'] == 'rect':
            self.paint_utils.set_color(self.painter,entity.config['color'],entity.config['fill'])            
            self.painter.drawRect(pose[0],pose[1],entity.config['width'],entity.config['height'])
            if self.game_manager.debug_mode:
                self.paint_utils.set_color(self.painter,'black',0)            
                self.painter.drawRect(pose[0],pose[1],entity.config['width'],entity.config['height'])
        elif entity.config['type'] == 'poly':
            self.paint_utils.set_color(self.painter,'black',1,width=3)
            self.painter.drawPoint(pose[0],pose[1])
            verts = entity.config['vertices'].copy()
            r,c = verts.shape
            verts[0,:] = verts[0,:]+pose[0]
            verts[1,:] = verts[1,:]+pose[1]
            for i in range(c):
                self.painter.drawPoint(verts[0,i],verts[1,i])

        if self.game_manager.debug_mode:
            unit_vec = np.array([[15.0,0.0],[0.0,15.0]])
            axes = geom.rotate_2d(unit_vec,entity.theta)
            x_axis = axes[:,0]
            y_axis = axes[:,1]
            self.paint_utils.set_color(self.painter,'red',True,width=3)
            self.painter.drawLine(pose[0],pose[1],pose[0]+x_axis[0],pose[1]+x_axis[1])
            self.paint_utils.set_color(self.painter,'green',True,width=3)
            self.painter.drawLine(pose[0],pose[1],pose[0]+y_axis[0],pose[1]+y_axis[1])

        if not entity.config['static']:
            if self.display_tails and np.linalg.norm(entity.physics.velocity)>20.0:
                self.paint_utils.set_color(self.painter,'orange',True,width=1)
                r,c = entity.tail.shape
                for idx in range(0,c-1):
                    p1 = self.transform(entity.tail[:,idx],parent_frame='scene',child_frame='camera')
                    p2 = self.transform(entity.tail[:,idx+1],parent_frame='scene',child_frame='camera')
                    self.painter.drawLine(p1[0],p1[1],p2[0],p2[1])

    def update(self):
        '''
            Draws all entities in the scene.
        '''
        for entity in self.scene.entities:
            self.paint_entity(entity)
                
