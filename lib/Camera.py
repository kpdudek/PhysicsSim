#!/usr/bin/env python3

from PyQt5 import QtCore

from lib.PaintUtils import PaintUtils
from lib.Logger import Logger

import numpy as np

class Camera(object):
    def __init__(self,frame_size,painter,pose,scene):
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.frame_size = frame_size
        self.painter = painter
        self.scene = scene
        self.pose = pose
        self.zoom_level = 1.0

        self.display_fps_overlay = True

    def translate(self,vec):
        self.pose = self.pose + vec

    def zoom(self,multiplier):
        self.zoom_level = multiplier

    def transform(self,point,frame='world'):
        '''
        Transforms a point in a given frame to the camera frame
        '''
        coord = point - self.pose
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
        if type(self.scene.launch_origin)==np.ndarray:
            pen,brush = self.paint_utils.set_color('white',1)
            self.painter.setPen(pen)
            self.painter.setBrush(brush)
            self.painter.drawEllipse(self.scene.launch_origin[0]-2,self.scene.launch_origin[1]-2,5,5)
            slope = np.array([-1*(self.scene.launch_point[0]-self.scene.launch_origin[0]),-1*(self.scene.launch_point[1]-self.scene.launch_origin[1])])
            val = self.scene.launch_origin + slope
            self.painter.drawLine(self.scene.launch_origin[0],self.scene.launch_origin[1],val[0],val[1])

    def update(self):
        for entity in self.scene.entities:
            if entity.config['color'] == "None":
                pass
            
            elif entity.config['type'] == 'circle':
                pen,brush = self.paint_utils.set_color(entity.default_color,1)
                self.painter.setPen(pen)
                self.painter.setBrush(brush)
                self.painter.drawEllipse(int(entity.pose[0])-10+self.pose[0],int(entity.pose[1])-10+self.pose[1],20,20)
            
            elif entity.config['type'] == 'rect':
                pen,brush = self.paint_utils.set_color(entity.config['color'],entity.config['fill'])
                self.painter.setPen(pen)
                self.painter.setBrush(brush)
                self.painter.drawRect(int(entity.pose[0]+self.pose[0]),int(entity.pose[1]+self.pose[1]),entity.config['width'],entity.config['height'])
