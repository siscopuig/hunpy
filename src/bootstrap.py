from src.log import Log
from src.config import Config
from src.datasource import Datasource
from src.handler import Handler
from src.connector.mysql_connector import MysqlConn
import sys

config_yml_file_path = [
	'config/hunpy.yml',
]


datasource_paths = {
	"adservers": 		  "datasource/adservers.txt",
	"ignore_domain_path": "datasource/ignore_domain_path.txt",
	"ignore_domain": 	  "datasource/ignore_domain.txt",
	"ignore_path": 		  "datasource/ignore_path.txt"
}



class Bootstrap:

	# @todo:
	# - In theory this class will start the program and handle
	# 	all the configuration needed to run.


	"""
	config_file_path	=

	adservers 			= /home/sisco/PycharmProjects/hunpy/datasource/adservers.txt
	ignore_domain_path 	= '/home/sisco/PycharmProjects/hunpy/datasource/ignore_domain_path.txt'
	ignore_domain		= '/home/sisco/PycharmProjects/hunpy/datasource/ignore_domain.txt'
	ignore_path		   	= '/home/sisco/PycharmProjects/hunpy/datasource/ignore_path.txt'
	"""

	def __init__(self):

		# Open log
		self.log = Log()
		self.log.open()
		self.log.info('Hunpy started')



	def start(self):

		conf = self.get_yaml_conf_file()

		dbconn = self.get_connector(conf['connection.parameters'])

		# Get datasource from files & database
		datasource = self.get_datasource(dbconn)

		handler = Handler(conf, datasource)
		handler.search()


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
			self.log.error('MySQL exception: {}'.format(e))
			sys.exit(1)

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
			self.log.error('Error loading yaml configuration file: {}'.format(e))
			sys.exit(1)

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
			self.log.error('Error loading datasource files: {}'.format(e))
			sys.exit(1)

		return ds




##########################################
if __name__ == '__main__' :
	boot = Bootstrap()
	boot.start()








