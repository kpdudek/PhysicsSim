#!/usr/bin/env python3

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from lib.Logger import Logger, FilePaths
from lib.Entity import Entity
from lib.PaintUtils import PaintUtils
from lib.Camera import Camera
from lib.Scene import Scene
import lib.Geometry as geom

import numpy as np
import time

class GameManager(QLabel):
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self,keys_pressed,debug_mode):
        super().__init__()
        self.keys_pressed = keys_pressed
        self.debug_mode = debug_mode
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.file_paths = FilePaths()

        self.fps = 60.0
        self.max_fps = 0.0
        self.prev_fps = 0.0
        self.average_fps = 0.0

        self.scene = Scene(self.fps)
        self.resize_canvas(1600,900)
        self.camera = Camera(self.frame_size,self.painter,np.array([0,0]),self.scene)

        self.prev_mouse_pose = None
        self.control_force = np.array([0,0])
        self.control_torque = 0

        self.game_timer = QtCore.QTimer()
        self.game_timer.timeout.connect(self.game_loop)

        self.health_logger_timer = QtCore.QTimer()
        self.health_logger_timer.timeout.connect(self.health_logger)
        self.average_fps_timer = QtCore.QTimer()
        self.average_fps_timer.timeout.connect(self.average_fps_calculator)

        self.paused = True
        self.scene.load_entities()
        self.start_simulation()

    def resize_canvas(self,width,height):
        self.frame_size = np.array([width,height])
        self.canvas_pixmap = QtGui.QPixmap(self.frame_size[0],self.frame_size[1])
        self.setPixmap(self.canvas_pixmap)
        self.painter = QtGui.QPainter(self.pixmap())

    def resizeEvent(self, e):
        self.logger.log(f"Window resized to: [{e.size().width()},{e.size().height()}]")
        # self.resize_canvas(e.size().width(),e.size().height())

    def start_simulation(self):
        self.logger.insert_blank_lines(2)
        self.logger.log('Game starting...',color='g')
        self.scene.init_scene()
        self.game_timer.start(1000/self.fps)
        self.health_logger_timer.start(1000)
        self.average_fps_timer.start(1000/5)

    def mousePressEvent(self, e):
        self.logger.log(f'Mouse press [{e.button()}] at: ({e.x()},{e.y()})',color='g')
        point = np.array([e.x(),e.y()])
        if e.button() == 1:
            for entity in self.scene.entities:
                if geom.point_is_collision(self.camera.transform(point.copy()),entity):
                    self.logger.log(f'Selected entity: {entity}')
                    self.scene.item_selected = entity
                    self.prev_mouse_pose = point
                    self.scene.item_selected.physics_lock = True
                    return
            self.scene.launch_origin = point
            self.scene.launch_point = point
        elif e.button() == 2:
            for entity in self.scene.entities:
                if geom.point_is_collision(self.camera.transform(point.copy()),entity):
                    self.logger.log(f'Removing entity: {entity}')
                    self.scene.entities.remove(entity)
                    return
    
    def mouseMoveEvent(self, e):
        if self.scene.item_selected:
            curr_mouse_pose = np.array([e.x(),e.y()])
            translate = curr_mouse_pose - self.prev_mouse_pose
            self.scene.item_selected.translate(translate)
            self.prev_mouse_pose = curr_mouse_pose
            self.scene.item_selected.physics.velocity = np.array([0.0,0.0])
            return
        self.scene.launch_point = np.array([e.x(),e.y()])

    def mouseReleaseEvent(self,e):
        if self.scene.item_selected:
            self.scene.item_selected.physics_lock = False
            self.scene.item_selected = None
            self.prev_mouse_pose = None
            return
        if e.button() == 1:
            self.scene.launch_point = np.array([e.x(),e.y()])
            launch_vel = (self.scene.launch_origin-self.scene.launch_point)*10.0
            launch_point = self.camera.transform(self.scene.launch_origin)
            self.scene.spawn_ball(launch_point,launch_vel)
            self.scene.launch_origin = None
            self.scene.launch_point = None
        
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
        self.logger.log(f'Number of Entities: {len(self.scene.entities)}')
        self.logger.log(f'Keys pressed: {self.keys_pressed}')
    
    def average_fps_calculator(self):
        self.average_fps = (self.max_fps + self.prev_fps) / 2.0
        self.prev_fps = self.max_fps

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
        self.max_fps = 1.0/(toc-tic)