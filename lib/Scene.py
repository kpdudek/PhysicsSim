#!/usr/bin/env python3

from lib.Logger import Logger, FilePaths

import os, json

class Scene(object):
    def __init__(self):
        self.logger = Logger()
        self.file_paths = FilePaths()

        self.entities = []
        self.entity_configs = []

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

    def update(self,force,torque):
        for entity in self.entities:
            entity.update_physics(force,torque)
