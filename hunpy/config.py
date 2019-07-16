# -*- coding: utf-8 -*-

import yaml
from hunpy.utils.utils_files import get_abs_path


class Config:


    def __init__(self):

        self.data = {}


    def load_config(self, file_paths):

        for path in file_paths:

            with open(get_abs_path(path), 'r') as yml_file:
                self.fill(yaml.safe_load(yml_file))


    def fill(self, yml_file):

        for key, value in yml_file.items():
            self.data[key] = value


    def get_config(self):

        return self.data