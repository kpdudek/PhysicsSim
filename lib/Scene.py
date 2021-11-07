#!/usr/bin/env python3

from PyQt5 import QtCore, QtWidgets
from lib.Logger import Logger, FilePaths
from lib.Entity import Entity, DynamicEntity

import os, json, ctypes
import numpy as np
import lib.Geometry as geom
from numpy.ctypeslib import ndpointer

class Scene(QtWidgets.QWidget):
    shutdown_signal = QtCore.pyqtSignal()

    def __init__(self,fps,game_manager):
        super().__init__()
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.fps = fps
        self.game_manager = game_manager

        self.entity_configs = []
        self.static_entities = []
        self.dynamic_entities = []
        self.load_entities()
        self.init_scene()

        self.entity_spawn_physics = None
        self.entity_spawn_type = None
        self.mode = None

        self.item_selected = None
        self.launch_origin = None
        self.launch_point = None
        self.spawn_count = 1

        # C library for collision checking
        try:
            self.cc_fun = ctypes.CDLL(f'{self.file_paths.lib_path}{self.file_paths.cc_lib_path}')
        except:
            self.logger.log('Failed to initialize collision checking library!',color='r')
            self.shutdown_timer = QtCore.QTimer()
            self.shutdown_timer.timeout.connect(self.shutdown_event)
            self.shutdown_timer.start(500)
            return
        # Circle Circle collision check
        self.cc_fun.circle_circle.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double]
        self.cc_fun.circle_circle.restype = ctypes.c_int
        # Circle Rect collision check
        self.cc_fun.circle_rect.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ctypes.c_double]
        self.cc_fun.circle_rect.restype = ctypes.c_double
        # Rect Rect collision check
        self.cc_fun.rect_rect.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ctypes.c_double,ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ctypes.c_double]
        self.cc_fun.rect_rect.restype = ctypes.c_double
        # Point Rect collision check
        self.cc_fun.point_rect.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ctypes.c_double]
        self.cc_fun.point_rect.restype = ctypes.c_double
        # Point Circle collision check
        self.cc_fun.point_circle.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double]
        self.cc_fun.point_circle.restype = ctypes.c_double

        res = self.cc_fun.get_library_version()
        self.logger.log(f"C collision checking library version: {res}")

        self.logger.log(f"Scene initialized...")

    def shutdown_event(self):
        self.shutdown_signal.emit()

    def load_entities(self):
        self.entity_configs = {}
        entities = os.listdir(self.file_paths.entity_path)
        self.logger.log(f'Entities found: {entities}')
        for idx,entity in enumerate(entities):
            fp = open(f'{self.file_paths.entity_path}{entity}','r')
            entity_object = json.load(fp)
            self.entity_configs.update({f"{entity_object['name']}":entity_object})
            fp.close()
    
    def get_entity_types(self):
        entity_types = list(self.entity_configs.keys())
        return entity_types

    def init_scene(self):
        self.static_entities = []
        self.dynamic_entities = []

        self.static_entities.append(Entity(self.entity_configs['ground'],self.fps))
        self.ground_entity = self.static_entities[-1]
    
    def spawn_entity(self,pose,velocity):
        spawn = self.entity_configs[self.entity_spawn_type]
        if self.entity_spawn_physics == 'Static':
            self.static_entities.append(Entity(spawn,self.fps,pose=pose))
            self.static_entities[-1].config['static'] = 1
        elif self.entity_spawn_physics == 'Dynamic':
            self.dynamic_entities.append(DynamicEntity(spawn,self.fps,self.static_entities+self.dynamic_entities,self.cc_fun,pose=pose))
            self.dynamic_entities[-1].physics.velocity = velocity
            self.static_entities[-1].config['static'] = 0

    def point_is_collision(self,pose,entity):
        if entity.config['type']=='circle':
            if self.cc_fun.point_circle(pose,entity.pose,entity.config['radius']):
                return True
        elif entity.config['type']=='rect':
            if self.cc_fun.point_rect(pose,entity.pose,entity.config['width'],entity.config['height']):
                return True
        else:
            return False

    def mouse_press(self,pose,id):
        if id == 1: # Left click
            for entity in self.static_entities+self.dynamic_entities:
                if self.point_is_collision(self.camera.transform(pose),entity):
                    self.logger.log(f'Selected entity: {entity}')
                    self.item_selected = entity
                    self.prev_mouse_pose = pose
                    self.item_selected.physics_lock = True
                    return
            self.launch_origin = pose
            self.launch_point = pose
        elif id == 2: # Right click
            for entity in self.dynamic_entities:
                if self.point_is_collision(self.camera.transform(pose),entity):
                    self.logger.log(f'Removing entity: {entity}')
                    self.dynamic_entities.remove(entity)
                    return
            for entity in self.static_entities:
                if self.point_is_collision(self.camera.transform(pose),entity):
                    self.logger.log(f'Removing entity: {entity}')
                    self.static_entities.remove(entity)
                    return

    def mouse_move(self,pose,id):
        if self.item_selected:
            curr_mouse_pose = pose
            translate = curr_mouse_pose - self.prev_mouse_pose
            self.item_selected.translate(translate)
            self.prev_mouse_pose = curr_mouse_pose
            if not self.item_selected.config['static']:
                self.item_selected.physics.velocity = np.array(translate*150)
            return
        self.launch_point = pose

    def mouse_release(self,pose,id):
        if self.item_selected:
            self.item_selected.physics_lock = False
            self.item_selected = None
            self.prev_mouse_pose = None
            return
        elif id == 1:
            self.launch_point = pose
            launch_vel = (self.launch_origin-self.launch_point)*10.0
            launch_point = self.camera.transform(self.launch_origin)
            if self.mode == 'Spawn':
                self.spawn_entity(launch_point,launch_vel)
            self.launch_origin = None
            self.launch_point = None

    def update(self,force,torque):
        for entity in self.dynamic_entities:
            entity.update_physics(force,torque)
