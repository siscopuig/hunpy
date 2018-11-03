from src.config import Config
from src.data_manager import DataManager
from src.handler import Handler
from src.hunpy_exception import HunpyException
from src.utils.utils_files import get_abs_path
from src.log import Log
import datetime
import os

config_file_path = '../config/hunpy.yml'

class Bootstrap:
	"""
	config_file_path	=

	adservers 			= /home/sisco/PycharmProjects/hunpy/datasource/adserver_domain_list.txt
	ignore_domain_path 	= '/home/sisco/PycharmProjects/hunpy/datasource/source_ignore_domain_and_path.txt'
	ignore_domain		= '/home/sisco/PycharmProjects/hunpy/datasource/source_ignored_domains.txt'
	ignore_path		   	= '/home/sisco/PycharmProjects/hunpy/datasource/source_ignore_path.txt'
	"""

	def __init__(self):

		self.log = Log()

		self.config = Config('hunpy')
		self.config.load(config_file_path)
		ds_paths = self.config.__getitem__('datasource.relative.paths')

		self.dt = DataManager()
		self.config_datasource(ds_paths)

		print(0)


	def config_datasource(self, ds_paths):

		# Get absolute path (Do NOT work!!)
		# file_paths = {}
		# for key, path in ds_paths.items():
		# 	file_paths[key] = get_abs_path(path)
		# 	print(file_paths[key])

		try:

			self.dt.set_placements()
			self.dt.set_adservers_domains(ds_paths['adservers'])
			self.dt.set_ignore_domain_and_path(ds_paths['ignore.domain.path'])
			self.dt.set_ignore_domain(ds_paths['ignore.domain'])
			self.dt.set_ignore_path(ds_paths['ignore.path'])
			self.dt.__setitem__('src.ignored.subdomains', self.config.__getitem__('src.ignored.subdomains'))
			self.dt.__setitem__('src.ignore.landing', self.config.__getitem__('src.ignore.landing'))

		except HunpyException as e:
			self.log.critical(e)


	def start(self):

		handler = Handler(self.config)
		handler.search()



##########################################
obj = Bootstrap()
obj.start()







