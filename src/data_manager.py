
from src.connector.mysql_connector import MysqlConn
from src.log import Log
from src.hunpy_exception import HunpyException
import numpy as np

class DataManager:
	"""
	"""



	def __init__(self):

		self.dbconn = MysqlConn()
		self.log = Log()
		self.urls = None
		self.datasource = {}
		self.placements = None
		self.adservers = None
		self.ignore_domain_path = None
		self.ignore_domain = None
		self.ignore_path = None



	def get_urls(self):

		self.urls = self.dbconn.select_urls()

		if not self.urls:
			raise HunpyException('Error getting the urls from database')

		return self.urls


	def set_placements(self):
		"""

		:return:
		"""
		placements = self.dbconn.select_placements()

		self.placements = np.zeros((len(placements), 2), dtype=np.int)

		for i, placement in enumerate(placements):
			self.placements[i] = [placement[0], placement[1]]

		self.datasource['placements'] = self.placements


	def set_adservers(self, filepath):
		"""

		:return:
		"""
		# Get datasource list from txt file
		filelines = self.read_file_in_lines(filepath)

		# Create a numpy array to store the list
		self.datasource['adservers'] = np.array(filelines, dtype=np.object)


	def set_ignore_domain_and_path(self, filepath):

		# Get datasource list from txt file
		filelines = self.read_file_in_lines(filepath)

		# Create a numpy array to store the list
		self.ignore_domain_path = np.array(filelines, dtype=np.object)

		# Set ad server list in data source
		self.__setitem__('ignore_domain_and_path', self.ignore_domain_path)


	def set_ignore_domain(self, filepath):

		# Get datasource list from txt file
		filelines = self.read_file_in_lines(filepath)

		# Create a numpy array to store the list
		self.ignore_domain = np.array(filelines, dtype=np.object)

		# Set ad server list in data source
		self.__setitem__('ignore_domain', self.ignore_domain_path)


	def set_ignore_path(self, filepath):

		# Get datasource list from txt file
		filelines = self.read_file_in_lines(filepath)

		# Create a numpy array to store the list
		self.ignore_path = np.array(filelines, dtype=np.object)

		# Set ad server list in data source
		self.__setitem__('ignore_path', self.ignore_domain)



	def read_file_in_lines(self, filepath):
		"""

		:param filepath:
		:return:
		"""

		with open(filepath, 'rt', encoding='utf-8') as f:
			data = f.readlines()

		# Return a copy of the line with trailing whitespace removed.
		return [line.rstrip('\n') for line in data]


	def __setitem__(self, key, value):

		"""

		:param key:
		:param value:
		:return:
		"""

		self.datasource[key] = value


	def __getitem__(self, item):
		"""

		:param item:
		:return:
		"""
		return self.datasource[item]


	def __contains__(self, key):
		"""

		:param key:
		:return:
		"""
		return key in self.datasource


#######################
# for width, height in placements:
# 	print('width: ({}), height: ({})'.format(width, height))

# for line in placements:
# 	with open('extracted.txt', 'a') as f:
# 		print(line, sep='#', file=f)