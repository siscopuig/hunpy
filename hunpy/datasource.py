# -*- coding: utf-8 -*-

import numpy as np
from hunpy.log import Log
from hunpy.utils.utils_strings import UtilsString
from hunpy.utils.utils_files import get_project_root_abs_path


class Datasource:


    def __init__(self, dbconn):

        self.log = Log()
        self.dbconn = dbconn
        self.ds_paths = {}
        self.datasource = {}
        self.placements = None
        self.adservers = None
        self.ignore_domain = None
        self.ignore_path = None


    def config_datasource_abs_path(self, ds_paths):

        for key, value in ds_paths.items():
            self.ds_paths[key] = get_project_root_abs_path(value)


    def get_urls(self, arg_url):

        urls = {}

        if arg_url:
            urls[1] = arg_url

        if not urls:

            file = self.read_file_in_lines(self.ds_paths['sources'])

            counter = 1
            for line in file:
                urls[counter] = line
                counter += 1

        return urls


    def get_placements(self):

        # @todo: Get placements from a text file in folder datasources.

        if self.placements is None:

            placements = self.dbconn.select_placements()

            self.placements = np.zeros((len(placements), 2), dtype=np.int)

            for i, placement in enumerate(placements):
                self.placements[i] = [placement['width'], placement['height']]

        return self.placements


    def get_adservers(self):

        if self.adservers is None:

            file = self.read_file_in_lines(self.ds_paths['adservers'])

            self.adservers = np.array(file, dtype=np.object)

        return self.adservers


    def get_ignore_domain(self):

        if self.ignore_domain is None:

            file = self.read_file_in_lines(self.ds_paths['ignore.domain'])

            self.ignore_domain = np.array(file, dtype=np.object)

        return self.ignore_domain


    def get_ignore_path(self):

        if self.ignore_path is None:

            file = self.read_file_in_lines(self.ds_paths['ignore.path'])

            self.ignore_path = np.array(file, dtype=np.object)

        return self.ignore_path


    def read_file_in_lines(self, filepath):

        with open(filepath, 'rt', encoding='utf-8') as f:
            data = f.readlines()

        # Return a copy of the line with trailing whitespace removed.
        return [line.rstrip('\n') for line in data]


    def match_placement(self, width, height):

        for size in self.get_placements():
            if size[0] == width and size[1] == height:
                return True
        return False


    def insert_new_advert(self, advert):

        landing = advert.landing
        if landing:
            if len(landing) > 512:
                landing = UtilsString.strip_landing(landing)
                if len(landing) > 512:
                    landing = landing[:512]
                    self.log.debug('landing has been truncated to have 512 characters')
                else:
                    self.log.debug('landing has been sanitised')

        data = {
            "uid": advert.uid,
            "src": advert.src,
            "width": advert.size[0],
            "height": advert.size[1],
            "finfo": advert.finfo,
            "isframe": advert.isframe,
            "x": advert.location[0],
            "y": advert.location[1],
            "landing": landing if landing else None,
            "advertiser": advert.advertiser if advert.advertiser else None,
            # "filepath": advert.filepath
        }

        self.dbconn.insert_new_advert(data)


    def is_source_in_database(self, src):

        # Select uid from adverts where src is equal to src
        result = self.dbconn.select_existing_source(src)
        if not result:
            return False

        if len(result) >= 2:
            self.log.debug(
                'Number ({}) of duplicated source ({}) found in database'.
                format(len(result), src))

        return result[0]


    def __setitem__(self, key, value):

        self.datasource[key] = value


    def __getitem__(self, item):

        return self.datasource[item]


    def __contains__(self, key):

        return key in self.datasource
