from src.config import Config
from src.data_manager import DataManager
from src.handler import Handler
from src.hunpy_exception import HunpyException
from src.log import Log


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

		try:

			# Get a log instance
			self.log = Log()
			self.log.debug('Hunpy started')

			# Load config file
			self.config = Config('hunpy')
			self.config.load(config_file_path)
			ds_paths = self.config.__getitem__('datasource.relative.paths')

			# Get datasource from files & database
			self.dm = DataManager()
			self.config_datasource(ds_paths)

			handler = Handler(self.config, self.dm)
			handler.search()


		except Exception as error:
			self.log.critical('Problem configuring datasource: {}'.format(error))
			print(0)


	def config_datasource(self, ds_paths):

		self.dm.set_placements()
		self.dm.set_adservers(ds_paths['adservers'])
		self.dm.set_ignore_domain_and_path(ds_paths['ignore.domain.path'])
		self.dm.set_ignore_domain(ds_paths['ignore.domain'])
		self.dm.set_ignore_path(ds_paths['ignore.path'])





##########################################
obj = Bootstrap()








