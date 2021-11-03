#!/usr/bin/env python3

from lib.Logger import Logger, FilePaths
from lib.Entity import Entity, DynamicEntity

import os, json, ctypes
import numpy as np
from numpy.ctypeslib import ndpointer

class Scene(object):
    def __init__(self,fps):
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.fps = fps

        self.entity_configs = []
        self.static_entities = []
        self.dynamic_entities = []
        self.load_entities()
        self.init_scene()

        self.entity_spawn_type = None
        self.mode = None

        self.item_selected = None
        self.launch_origin = None
        self.launch_point = None
        self.spawn_count = 1

        # C library for collision checking
        self.cc_fun = ctypes.CDLL(f'{self.file_paths.lib_path}{self.file_paths.cc_lib_path}')
        # Circle Circle collision check
        self.cc_fun.circle_circle.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double]
        self.cc_fun.circle_circle.restype = ctypes.c_int
        # Circle Rect collision check
        self.cc_fun.circle_rect.argtypes = [ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),ctypes.c_double,ctypes.c_double]
        self.cc_fun.circle_rect.restype = ctypes.c_double
        res = self.cc_fun.get_library_version()
        self.logger.log(f"C collision checking library version: {res}")

        self.logger.log(f"Scene initialized...")

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

        self.static_entities.append(Entity(self.entity_configs['ground'],np.array([0.0,0.0]),self.fps))
        self.static_entities[-1].teleport(np.array([250.0,200.0]))
        self.ground_entity = self.static_entities[-1]

        self.static_entities.append(Entity(self.entity_configs['boundary'],np.array([0.0,0.0]),self.fps))
        self.boundary_entity = self.static_entities[-1]
    
    def spawn_ball(self,pose,velocity):
        spawn = self.entity_configs[self.entity_spawn_type]
        self.dynamic_entities.append(DynamicEntity(spawn,pose,self.fps,self.static_entities,self.cc_fun))
        self.dynamic_entities[-1].physics.velocity = velocity

    def update(self,force,torque):
        for entity in self.dynamic_entities:
            entity.update_physics(force,torque)
