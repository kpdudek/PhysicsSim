#!/usr/bin/env python3

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from lib.Logger import Logger, FilePaths
from lib.Entity import Entity
from lib.PaintUtils import PaintUtils
import lib.Geometry as geom

import numpy as np
import os, json, time

class GameWindow(QLabel):
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self,keys_pressed,debug_mode):
        super().__init__()
        self.keys_pressed = keys_pressed
        self.logger = Logger()
        self.paint_utils = PaintUtils()
        self.file_paths = FilePaths()

        self.frame_size = np.array([1400,800])
        self.canvas_pixmap = QtGui.QPixmap(self.frame_size[0],self.frame_size[1])
        self.setPixmap(self.canvas_pixmap)
        self.painter = QtGui.QPainter(self.pixmap())

        self.entity_configs = []
        self.entities = []
        self.item_selected = None
        self.prev_mouse_pose = None

        self.fps = 120
        self.max_fps = 0.0
        self.prev_fps = 0.0
        self.average_fps = 0.0
        self.game_timer = QtCore.QTimer()
        self.game_timer.timeout.connect(self.game_loop)

        self.health_logger_timer = QtCore.QTimer()
        self.health_logger_timer.timeout.connect(self.health_logger)
        self.average_fps_timer = QtCore.QTimer()
        self.average_fps_timer.timeout.connect(self.average_fps_calculator)
        self.launch_origin = None
        self.launch_point = None

        self.debug_mode = debug_mode
        self.paused = True
        self.load_entities()
        self.start_simulation()

    def load_entities(self):
        entities = os.listdir(self.file_paths.entity_path)
        self.logger.log(f'Enties found: {entities}')
        for idx,entity in enumerate(entities):
            fp = open(f'{self.file_paths.entity_path}{entity}','r')
            entity_object = json.load(fp)
            self.entity_configs.append(entity_object)
            fp.close()
            
            if entity_object['name'] == 'ball':
                self.ball_config_idx = idx
            elif entity_object['name'] == 'ground':
                self.ground_config_idx = idx

    def start_simulation(self):
        self.logger.insert_blank_lines(2)
        self.logger.log('Game starting...',color='g')

        self.entities.append(Entity(self.entity_configs[self.ground_config_idx],self.painter,np.array([[0],[0]]),self.fps,self.frame_size))
        self.entities[-1].teleport(np.array([400,400-self.entities[-1].config['height']]))
        self.ground_entity = self.entities[-1]

        self.game_timer.start(1000/self.fps)
        self.health_logger_timer.start(2000)
        self.average_fps_timer.start(1000/5)

    def spawn_ball(self,pose,velocity):
        self.entities.append(Entity(self.entity_configs[self.ball_config_idx],self.painter,pose,self.fps,self.frame_size))
        self.entities[-1].add_physics(1.0,collision_bodies=[self.ground_entity])
        self.entities[-1].physics.velocity = velocity

    def mousePressEvent(self, e):
        self.logger.log(f'Mouse press [{e.button()}] at: ({e.x()},{e.y()})',color='g')
        point = np.array([e.x(),e.y()])
        if e.button() == 1:
            for entity in self.entities:
                if geom.point_is_collision(point,entity):
                    self.logger.log(f'Selected entity: {entity}')
                    self.item_selected = entity
                    self.prev_mouse_pose = point
                    self.item_selected.physics_lock = True
                    return
            self.launch_origin = point
            self.launch_point = point
        elif e.button() == 2:
            for entity in self.entities:
                if geom.point_is_collision(point,entity):
                    self.logger.log(f'Removing entity: {entity}')
                    self.entities.remove(entity)
                    return
    
    def mouseMoveEvent(self, e):
        if self.item_selected:
            curr_mouse_pose = np.array([e.x(),e.y()])
            translate = curr_mouse_pose - self.prev_mouse_pose
            self.item_selected.translate(translate)
            self.prev_mouse_pose = curr_mouse_pose
            self.item_selected.physics.velocity = np.array([0.0,0.0])
            return
        self.launch_point = np.array([e.x(),e.y()])

    def mouseReleaseEvent(self,e):
        if self.item_selected:
            self.item_selected.physics_lock = False
            self.item_selected = None
            self.prev_mouse_pose = None
            return
        if e.button() == 1:
            self.launch_point = np.array([e.x(),e.y()])
            launch_vel = (self.launch_origin-self.launch_point)*10.0
            self.spawn_ball(self.launch_origin,launch_vel)
            self.launch_origin = None
            self.launch_point = None
        
    def process_keys(self):
        for key in self.keys_pressed:
            pass

    def toggle_pause(self):
        if self.paused:
            self.paused = False
        else:
            self.paused = True

    def paint_update(self):
        pen,brush = self.paint_utils.background()
        self.painter.setPen(pen)
        self.painter.setBrush(brush)
        self.painter.drawRect(0,0,1400,800)

        pen,brush = self.paint_utils.set_color('white')
        self.painter.setPen(pen)
        self.painter.setBrush(brush)
        self.painter.drawText(3,13,200,75,QtCore.Qt.TextWordWrap,str(int(self.average_fps)))
    
    def paint_launch_controls(self):
        if type(self.launch_origin)==np.ndarray:
            pen,brush = self.paint_utils.set_color('white')
            self.painter.setPen(pen)
            self.painter.setBrush(brush)
            self.painter.drawEllipse(self.launch_origin[0]-2,self.launch_origin[1]-2,5,5)

            slope = np.array([-1*(self.launch_point[0]-self.launch_origin[0]),-1*(self.launch_point[1]-self.launch_origin[1])])
            val = self.launch_origin + slope
            self.painter.drawLine(self.launch_origin[0],self.launch_origin[1],val[0],val[1])

    def health_logger(self):
        self.logger.log(f'Average FPS: {self.average_fps}')
        self.logger.log(f'Number of Entities: {len(self.entities)}')
    
    def average_fps_calculator(self):
        self.average_fps = (self.max_fps + self.prev_fps) / 2.0
        self.prev_fps = self.max_fps

    def game_loop(self):
        tic = time.time()
        self.process_keys()
        self.paint_update()
        
        for entity in self.entities:
            if not self.paused:
                entity.update_physics()
            entity.paint()

        self.paint_launch_controls()
        self.repaint()
        toc = time.time()
        self.max_fps = 1.0/(toc-tic)