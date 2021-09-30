#!/usr/bin/env python3

from lib.PaintUtils import PaintUtils
from lib.Logger import Logger

import numpy as np

class Camera(object):
    def __init__(self,painter,pose,size,scene):
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.painter = painter
        self.scene = scene
        self.pose = pose
        self.zoom_level = 1.0

    def translate(self,vec):
        self.pose = self.pose + vec

    def zoom(self,multiplier):
        self.zoom_level = multiplier

    def transform(self,point,frame='world'):
        '''
        Transforms a point in a given frame to the camera frame
        '''
        coord = self.pose - point
        return coord

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
