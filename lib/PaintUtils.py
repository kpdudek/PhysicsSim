#!/usr/bin/env python3

from PyQt5 import QtGui
from PyQt5.QtCore import Qt

import random

class PaintUtils(object):
    def __init__(self):
        self.colors = {
            "black":"#000000",
            "gray":"#353535",
            "light_gray":"#ABABAB",
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
        self.reserved_colors = ['black','brown']

    def random_color(self):
        '''
        Returns a random color hex code.
        Will not return a color in the reserved colors list.
        Arguments:
            None
        Returns:
            color [str]: A hex code for a random color.
        '''
        num = len(self.colors)-1
        index = random.randint(0,num)
        key = list(self.colors.keys())[index]
        while key in self.reserved_colors:
            num = len(self.colors)-1
            index = random.randint(0,num)
            key = list(self.colors.keys())[index]
        return self.colors[key]

    def set_color(self,color,fill):
        '''
        Arguments:
            color [str]: Sets the color of what's being painted. Can be either a hex code for a color or the name
            fill [int]: Sets the fill for what's being painted. Either 1 for filled or 0 for outline only.
        Returns:
            pen [QtGui.QPen]: A QPen object with the specified color. Fixed width of 1px.
            brush [QtGui.QBrush]: A QBrush object with the specified color and fill.
        '''
        # TODO: Instead of returning the pen and brush, change the callers passed in pen and brush
        # TODO: Add an argument for pen width
        pen = QtGui.QPen()
        pen.setWidth(1)
        brush = QtGui.QBrush()
        if fill:
            brush.setStyle(Qt.SolidPattern)
        else:
            brush.setStyle(Qt.NoBrush)

        if color in list(self.colors.keys()):
            pen.setColor(QtGui.QColor(self.colors[color]))
            brush.setColor(QtGui.QColor(self.colors[color]))
        else:
            pen.setColor(QtGui.QColor(color))
            brush.setColor(QtGui.QColor(color))

        return pen,brush