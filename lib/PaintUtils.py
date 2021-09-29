#!/usr/bin/env python3

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

import random

class PaintUtils(object):
    def __init__(self):
        self.colors = {
            "black":"#000000",
            "gray":"#353535",
            "light_gray":"#BDBDBD",
            "white":"#FFFFFF",
            "brown":"#996633",
            "sky_blue":"#1BADDE",
            "midnight_blue":"#051962",
            "star_gold":"#F7D31E",
            "forest_green":"#38690E",
            "light_green":"#00FF00",
            "red":"#DF0101",
            "maroon":"#B40431"
        }

    def random_color(self):
        num = len(self.colors)-1
        index = random.randint(0,num)
        key = list(self.colors.keys())[index]
        while key in ['black','brown']:
            num = len(self.colors)-1
            index = random.randint(0,num)
            key = list(self.colors.keys())[index]
        return self.colors[key]

    def ball(self,color):
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(color))

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(color))
        brush.setStyle(Qt.SolidPattern)

        return pen,brush

    def ground(self):
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.colors['brown']))

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.colors['brown']))
        brush.setStyle(Qt.SolidPattern)

        return pen,brush

    def set_color(self,color,fill):
        pen = QtGui.QPen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.colors[color]))

        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.colors[color]))
        if fill:
            brush.setStyle(Qt.SolidPattern)
        else:
            brush.setStyle(Qt.NoBrush)

        return pen,brush