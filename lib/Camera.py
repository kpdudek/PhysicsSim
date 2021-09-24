#!/usr/bin/env python3

from lib.PaintUtils import PaintUtils
from lib.Logger import Logger

class Camera(object):
    def __init__(self,painter,pose,size,scene):
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.painter = painter
        self.pose = pose
        self.scene = scene

    def update():
        pass