from src.log import Log
from src.config import Config
from src.datasource import Datasource
from src.handler import Handler
from src.utils.utils_strings import UtilsString

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

	"""
	config_file_path	=

	adservers 			= /home/sisco/PycharmProjects/hunpy/datasource/adservers.txt
	ignore_domain_path 	= '/home/sisco/PycharmProjects/hunpy/datasource/ignore_domain_path.txt'
	ignore_domain		= '/home/sisco/PycharmProjects/hunpy/datasource/ignore_domain.txt'
	ignore_path		   	= '/home/sisco/PycharmProjects/hunpy/datasource/ignore_path.txt'
	"""

	def __init__(self):

		try:

			# Open log
			self.log = Log()
			self.log.open()
			self.log.info('Hunpy started')

			# Load yaml config file
			self.config = Config()
			self.config.load(config_yml_file_path)


			# Get datasource from files & database
			self.datasource = Datasource(self.config.data['connection.parameters'])
			self.datasource.config_datasource_abs_path(datasource_paths)


			handler = Handler(self.config.data, self.datasource)
			handler.search()


		except Exception as error:
			self.log.error('Problem configuring: {}'.format(error))







##########################################
obj = Bootstrap()
# placements = self.datasource.get_placements()
# adservers = self.datasource.get_adservers()
# ignore_domain_path = self.datasource.get_ignore_domain_path()
# ignore_domain = self.datasource.get_ignore_domain()
# ignore_path = self.datasource.get_ignore_path()


# connect_params = {
# 	'user': 'root',
# 	'password': 'pupahit66',
# 	'host': 'localhost',
# 	'database': 'hunpy'
# }

# src = 'https://tpc.googlesyndication.com/simgad/4812493872611183408'
# ds = Datasource(connect_params)
# ds.match_source_paths_in_ignore_path(src)


# TESTING!!!!!
# src = 'https://tpc.googlesyndication.com/simgad/4812493872611183408'
#
# # match adserver
# domain = UtilsString.get_domain(src)
# if UtilsString.match_string_in_list(domain, self.datasource.get_adservers()):
# 	print(domain)
# else:
# 	print(0)
#
# if UtilsString.match_string_parts_in_list(src, self.datasource.get_ignore_domain()):
# 	print(1)
# else:
# 	print(0)







