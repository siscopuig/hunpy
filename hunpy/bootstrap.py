import sys
from hunpy.log import Log
from hunpy.config import Config
from hunpy.datasource import Datasource
from hunpy.handler import Handler
from hunpy.connector.mysql_connector import MysqlConn
from hunpy.utils.utils_files import create_directory

config_yml_file_path = ['config/hunpy.yml']


class Bootstrap:
    """"""
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

    @staticmethod
    def get_connector(connect_param):
        """
        Connect to the database and retrieves the connector
        """
        try:
            conn = MysqlConn(connect_param)
            conn.connect()
        except Exception as exception:
            sys.exit('MySQL exception: {}'.format(exception))
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
