# -*- coding: utf-8 -*-

import sys
from yaml import YAMLError
from hunpy.bootstrap import Bootstrap
from hunpy.log import Log
from hunpy.connector.mysql_connector import MysqlConn
from hunpy.utils.utils_files import create_directory
from hunpy.datasource import Datasource
from hunpy.config import Config


class Hunpy:


    def __init__(self, yml_config_path):

        self.yml_config_path = yml_config_path

        self.log = None

        self.arg_url = None

        self.arg_headless = False

        self.arg_verbose = False


    def start(self, args):

        if args.url:
            self.arg_url = args.url

        if args.headless:
            self.arg_headless = True

        if args.debug:
            self.arg_verbose = True


        # Get configuration list
        try:
            config = Config()
            config.load_config(self.yml_config_path)
            cnf_data = config.get_config()

        except YAMLError as exception:
            sys.exit('Error loading yaml configuration file: {}'.format(exception))


        if self.log is None:
            self.log = Log()
            self.log.open_log(cnf_data, self.arg_verbose)
            self.log.info('Hunpy started')

        # Creates chrome profile folder if doesn't exist
        create_directory(cnf_data['chrome.option.profile.path'])

        # Get connector
        dbconn = self.get_connector(cnf_data['connection.parameters'])

        # Get datasource from files & database
        datasource = self.get_datasource(dbconn, cnf_data['datasource.relative.paths'])

        # Get urls to process
        urls = datasource.get_urls(self.arg_url)
        if not urls:
            self.log.error('No urls found to process')
            exit(1)

        # Start processing
        handler = Bootstrap(cnf_data, datasource)
        handler.search(urls, self.arg_headless)


    def get_connector(self, connect_param):
        """
        Connect to the database and retrieves the connector
        """
        try:
            conn = MysqlConn(connect_param)
            conn.connect()
        except Exception as exception:
            sys.exit('MySQL exception: {}'.format(exception))
        return conn


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



def main(args, yml_config_path):

    __version__ = "0.0.1"
    print("Executing hunpy version %s." % __version__)
    hunpy = Hunpy(yml_config_path)
    while True:
        hunpy.start(args)



