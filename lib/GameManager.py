#!/usr/bin/env python3

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from lib.Logger import Logger, FilePaths
from lib.PaintUtils import PaintUtils
from lib.Camera import Camera
from lib.Scene import Scene
import lib.Geometry as geom

import numpy as np
import time

class GameManager(QLabel):
    shutdown_signal = QtCore.pyqtSignal()
    resize_signal = QtCore.pyqtSignal(int,int)

    def __init__(self,keys_pressed):
        super().__init__()
        self.keys_pressed = keys_pressed
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.file_paths = FilePaths()
        self.settings = None

        self.debug_mode = False
        self.fps = 60.0
        self.max_fps = 0.0
        self.prev_fps = 0.0
        self.average_fps = 0.0

        self.resize_flag = False
        self.resize_size = []
        self.scene = Scene(self.fps,self)
        self.scene.shutdown_signal.connect(self.shutdown_event)
        self.resize_canvas(1400,800)
        self.camera = Camera(self.frame_size,self.painter,self.scene,self)
        self.scene.camera = self.camera

        self.prev_mouse_pose = None
        self.control_force = np.array([0,0])
        self.control_torque = 0

        self.game_timer = QtCore.QTimer()
        self.game_timer.timeout.connect(self.game_loop)

        self.health_logger_timer = QtCore.QTimer()
        self.health_logger_timer.timeout.connect(self.health_logger)

        self.average_fps_timer = QtCore.QTimer()
        self.average_fps_timer.timeout.connect(self.average_fps_calculator)

        self.paused = False
        self.start_simulation()

    def shutdown_event(self):
        self.shutdown_signal.emit()
        QApplication.processEvents()

    def resize_canvas(self,width,height):
        try:
            self.painter.end()
        except:
            pass
        self.frame_size = np.array([width,height])
        self.canvas_pixmap = QtGui.QPixmap(self.frame_size[0],self.frame_size[1])
        self.setPixmap(self.canvas_pixmap)
        self.painter = QtGui.QPainter(self.pixmap())
        try:
            self.camera.painter = self.painter
            self.camera.frame_size = self.frame_size
        except:
            pass
        self.resize_flag = False
        self.resize_signal.emit(width,height)

    def resizeEvent(self, e):
        self.logger.log(f"Window resized to: [{e.size().width()},{e.size().height()}]")
        self.resize_flag = True
        self.resize_size = [e.size().width(),e.size().height()]

    def start_simulation(self):
        self.logger.insert_blank_lines(2)
        self.logger.log('Game starting...',color='g')
        self.game_timer.start(1000/self.fps)
        self.average_fps_timer.start(1000)

    def mousePressEvent(self, e):
        self.logger.log(f'Mouse press [{e.button()}] at: ({e.x()},{e.y()})',color='g')
        point = np.array([e.x(),e.y()])
        self.scene.mouse_press(point,e.button())
    
    def mouseMoveEvent(self, e):
        point = np.array([e.x(),e.y()])
        self.scene.mouse_move(point,e.button())

    def mouseReleaseEvent(self,e):
        point = np.array([e.x(),e.y()])
        self.scene.mouse_release(point,e.button())
        
    def process_keys(self):
        self.control_force = np.array([0,0])
        self.control_torque = 0.0
        for key in self.keys_pressed:
            if key == Qt.Key_D:
                # self.control_force[0] = 1
                self.control_torque = 1
            elif key == Qt.Key_A:
                # self.control_force[0] = 1
                self.control_torque = -1
            elif key == Qt.Key_Right:
                self.camera.translate(np.array([5,0]))
            elif key == Qt.Key_Left:
                self.camera.translate(np.array([-5,0]))
            elif key == Qt.Key_Up:
                self.camera.translate(np.array([0,-5]))
            elif key == Qt.Key_Down:
                self.camera.translate(np.array([0,5]))

    def toggle_pause(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def health_logger(self):
        self.logger.log(f'Average FPS: {self.average_fps}')
        self.logger.log(f'Number of Static Entities: {len(self.scene.static_entities)}')
        self.logger.log(f'Number of Dynamic Entities: {len(self.scene.dynamic_entities)}')
        self.logger.log(f'Keys pressed: {self.keys_pressed}')
        if self.debug_mode:
            self.logger.log('Debug Mode...')
    
    def average_fps_calculator(self):
        self.average_fps = (self.max_fps + self.prev_fps) / 2.0
        self.prev_fps = self.max_fps
        if self.max_fps < self.fps:
            self.logger.log(f'FPS has dropped below the set value!',color='r')

    def game_loop(self):
        tic = time.time()
        self.process_keys()
        self.camera.clear_display(self.average_fps)
        
        if not self.paused:
            self.scene.update(self.control_force*100.0,self.control_torque)
        self.camera.update()

        self.camera.paint_launch_controls()
        self.repaint()
        toc = time.time()
        try:
            self.max_fps = 1.0/(toc-tic)
        except:
            pass

        if self.resize_flag:
            self.resize_canvas(self.resize_size[0],self.resize_size[1])