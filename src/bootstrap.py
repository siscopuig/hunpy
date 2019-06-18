from log import Log
from config import Config
from datasource import Datasource
from handler import Handler
from connector.mysql_connector import MysqlConn
from utils.utils_files import create_directory
import sys
import os

# Configuration filepath
config_yml_file_path = ['config/hunpy.yml']


class Bootstrap:
    """puta"""

    def __init__(self):
        self.log = Log()

    def start(self):

        # Get configuration list
        config = self.get_yaml_conf_file()

        # Creates chrome profile folder if doesn't exist
        create_directory(config['chrome.option.profile.path'])

        # Get connector
        dbconn = self.get_connector(config['connection.parameters'])

        # Get datasource from files & database
        datasource = self.get_datasource(dbconn,
                                         config['datasource.relative.paths'])

        # Open log
        self.log.open_log(config, debug=True)
        self.log.info('Hunpy started')

        # Start processing
        handler = Handler(config, datasource)
        handler.search()

    def get_connector(self, connect_param):
        """
        Connect to the database and retrieves the connector
        """
        try:
            conn = MysqlConn(connect_param)
            conn.connect()
        except Exception as e:
            sys.exit('MySQL exception: {}'.format(e))
        return conn

    def get_yaml_conf_file(self):
        """
        Load yaml config file

        :return: a config list
        """
        try:
            config = Config()
            config.load_config(config_yml_file_path)
        except Exception as e:
            sys.exit('Error loading yaml configuration file: {}'.format(e))
        return config.data

    def get_datasource(self, dbconn, datasource_relative_paths):
        """
        Load datasource text files into the system

        :param datasource_relative_paths:
        :param dbconn:
        :return: datasource object
        """

        try:
            ds = Datasource(dbconn)
            ds.config_datasource_abs_path(datasource_relative_paths)

        except Exception as e:
            sys.exit('Error loading datasource files: {}'.format(e))
        return ds


##########################################
if __name__ == '__main__':
    boot = Bootstrap()
    while True:
        boot.start()
