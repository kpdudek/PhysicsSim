#!/usr/bin/env python3

from lib.Logger import Logger, FilePaths
from lib.Entity import Entity

import os, json
import numpy as np

class Scene(object):
    def __init__(self,fps):
        self.logger = Logger()
        self.file_paths = FilePaths()
        self.fps = fps

        self.entities = []
        self.entity_configs = []

        self.item_selected = None
        self.launch_origin = None
        self.launch_point = None

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
            elif entity_object['name'] == 'boundary':
                self.boundary_config_idx = idx

    def init_scene(self):
        self.entities.append(Entity(self.entity_configs[self.ground_config_idx],np.array([0,0]),self.fps))
        self.entities[-1].teleport(np.array([400,200]))
        self.ground_entity = self.entities[-1]

        self.entities.append(Entity(self.entity_configs[self.boundary_config_idx],np.array([0,0]),self.fps))
        self.boundary_entity = self.entities[-1]
    
    def spawn_ball(self,pose,velocity):
        self.entities.append(Entity(self.entity_configs[self.ball_config_idx],pose,self.fps))
        self.entities[-1].add_physics(1.0,collision_bodies=[self.ground_entity,self.boundary_entity])
        self.entities[-1].physics.velocity = velocity

    def update(self,force,torque):
        for entity in self.entities:
            entity.update_physics(force,torque)
