from .log import Log
from .hunpy_exception import HunpyException
from .utils.utils_strings import UtilsString
from .utils.utils_files import get_project_root_abs_path
import numpy as np


class Datasource:

    def __init__(self, dbconn):

        self.log = Log()
        self.dbconn = dbconn
        self.ds_paths = {}
        self.urls = None
        self.datasource = {}
        self.placements = None
        self.adservers = None
        self.ignore_domain = None
        self.ignore_path = None


    def config_datasource_abs_path(self, ds_paths):

        for key, value in ds_paths.items():
            self.ds_paths[key] = get_project_root_abs_path(value)


    def get_urls(self):

        self.urls = self.dbconn.select_urls()

        if not self.urls:
            raise HunpyException('Error getting urls from database')

        return self.urls


    def get_placements(self):

        if self.placements is None:

            placements = self.dbconn.select_placements()

            self.placements = np.zeros((len(placements), 2), dtype=np.int)

            for i, placement in enumerate(placements):
                self.placements[i] = [placement['width'], placement['height']]

        return self.placements

    def get_adservers(self):

        if self.adservers is None:

            # Get datasource list from txt file
            filelines = self.read_file_in_lines(self.ds_paths['adservers'])

            # Create a numpy array to store the list
            self.adservers = np.array(filelines, dtype=np.object)

        return self.adservers

    def get_ignore_domain(self):

        if self.ignore_domain is None:

            # Get datasource list from txt file
            filelines = self.read_file_in_lines(self.ds_paths['ignore.domain'])

            # Create a numpy array to store the list
            self.ignore_domain = np.array(filelines, dtype=np.object)

        return self.ignore_domain

    def get_ignore_path(self):

        if self.ignore_path is None:

            # Get datasource list from txt file
            filelines = self.read_file_in_lines(self.ds_paths['ignore.path'])

            # Create a numpy array to store the list
            self.ignore_path = np.array(filelines, dtype=np.object)

        return self.ignore_path

    def read_file_in_lines(self, filepath):

        with open(filepath, 'rt', encoding='utf-8') as f:
            data = f.readlines()

        # Return a copy of the line with trailing whitespace removed.
        return [line.rstrip('\n') for line in data]

    def __setitem__(self, key, value):

        self.datasource[key] = value

    def __getitem__(self, item):

        return self.datasource[item]

    def __contains__(self, key):

        return key in self.datasource

    # ------------------------------------------------

    def match_placement(self, width, height):

        for size in self.get_placements():
            if size[0] == width and size[1] == height:
                return True
        return False

    # ------------------------------------------------

    def insert_new_advert(self, advert):

        # @todo:
        # - Make sure that record has been inserted successfully.
        # - If an error it thrown during the operation, catch it!
        # - Check that landing is not bigger than 512 character -> done

        landing = advert.landing
        if landing:
            if len(landing) > 512:
                landing = UtilsString.strip_landing(landing)
                if len(landing) > 512:
                    landing = landing[:512]
                    self.log.info(
                        'landing has been truncated to have 512 characters')
                else:
                    self.log.info('landing has been sanitised')

        finfo = advert.finfo
        if 'text/html' in finfo:
            advert.finfo = finfo[:-15]

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
        }

        self.dbconn.insert_new_advert(data)

    def is_source_in_database(self, src):

        # @TODO:
        # Select all the values needed in one call (id, uid, src, advertiser).
        # It will return a list dict. E.g.
        # [{'id': 1, 'uid': '06e7fe57-c21d-4f40-9afa-f441361349be',
        # 'advertiser': 'events.marcusevans-events.com'}]

        # Select uid from adverts where src is equal to src
        result = self.dbconn.select_existing_source(src)
        if not result:
            return False

        if len(result) >= 2:
            self.log.info(
                'Number ({}) of duplicated source ({}) found in database'.
                format(len(result), src))

        return result[0]

    def is_new_instance(self, uid, url_id, date):

        result = self.dbconn.select_instance_record_by_date(
            'id', 'Instances', uid, url_id, date)
        if not result:
            return False

        return result[0]['id']

    def insert_new_instance(self, data):

        # @TODO: Log if an error or successful
        self.dbconn.insert_new_instance_record(data['uid'], data['url_id'],
                                               data['counter'], data['date'])

    def update_existing_instance(self, data):

        # @TODO: Log if an error or successful
        self.dbconn.update_existing_instance_record(data['id'], data['date'],
                                                    data['counter'])

    def count_cycle(self, url_id, date):

        result = self.dbconn.today_new_cycle(url_id, date)
        if not result:
            self.dbconn.insert_cycle(url_id, 1, date)
        else:
            self.dbconn.update_cycle(result[0]['id'], date)
