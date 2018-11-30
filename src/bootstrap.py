from log import Log
from config import Config
from datasource import Datasource
from handler import Handler
from connector.mysql_connector import MysqlConn
import sys



config_yml_file_path = [
	'/home/sisco/PycharmProjects/hunpy/config/hunpy.yml',
]


datasource_paths = {
	"adservers": 		  "/home/sisco/PycharmProjects/hunpy/datasource/adservers.txt",
	"ignore_domain_path": "/home/sisco/PycharmProjects/hunpy/datasource/ignore_domain_path.txt",
	"ignore_domain": 	  "/home/sisco/PycharmProjects/hunpy/datasource/ignore_domain.txt",
	"ignore_path": 		  "/home/sisco/PycharmProjects/hunpy/datasource/ignore_path.txt"
}



class Bootstrap:


	def __init__(self):

		# Get a log instance
		self.log = Log()

		# Get configuration list
		self.config = self.get_yaml_conf_file()

		# Get connector
		self.dbconn = self.get_connector(self.config['connection.parameters'])

		# Get datasource from files & database
		self.datasource = self.get_datasource(self.dbconn)


	def start(self):

		# Open log
		self.log.open(self.config)
		self.log.info('Hunpy started')


		handler = Handler(self.config, self.datasource)
		if handler.search():
			self.start()


	def get_connector(self, connect_param):
		"""
		Connect to the database and retrieves the connector

		:param connect_param:
		:return: connector object
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
			config.load(config_yml_file_path)

		except Exception as e:
			sys.exit('Error loading yaml configuration file: {}'.format(e))

		return config.data


	def get_datasource(self, dbconn):
		"""
		Load datasource text files into the system

		:param dbconn:
		:return: datasource object
		"""

		try:
			ds = Datasource(dbconn)
			ds.config_datasource_abs_path(datasource_paths)

		except Exception as e:
			sys.exit('Error loading datasource files: {}'.format(e))

		return ds




##########################################
if __name__ == '__main__' :
	boot = Bootstrap()
	boot.start()








