from connector.mysql_connector import MysqlConn
from src.hunpy_exception import HunpyException
from src.utils.utils_strings import UtilsString
import yaml

"""
__getitem__():
	Implementing __getitem__ in a class allows its instances to use
	the [] (indexer) operators.
	The __getitem__ magic method is usually used for list indexing, dictionary lookups,
	or accessing ranges of values. Considering how versatile it is, it's probably one
	of Python's most underutilized magic methods.
	
	https://docs.python.org/3.4/reference/datamodel.html#object.__getitem__
	http://farmdev.com/src/secrets/magicmethod/index.html
		
The isinstance():
	function returns True if the specified object
	is of the specified type, otherwise False. If the type parameter
	is a tuple, this function will return True if the object is one
	of the types in the tuple.
	
			
"""

class Config:

	"""
	"""

	data = {}
	dbconn = None
	urls = None
	adservers = None
	placements = None


	def __init__(self, name):
		"""
		
		:param name: 
		"""
		if not name in self.data:
			self.data[name] = {}
		self.data = self.data[name]



	def load(self, file_paths):
		"""
		
		:param file_paths: 
		:return: 
		"""
		if file_paths:

			# Checks that `file_paths` is a list
			if not isinstance(file_paths, list):
				file_paths = [file_paths]

			for file_path in file_paths:
				with open(UtilsString.get_abs_path(file_path), 'r') as yml_file:
					self.update(yaml.load(yml_file))



	def update(self, yml_file):
		"""
		
		:param yml_file: 
		:return: 
		"""
		self.merge(self.data, yml_file)



	def merge(self, target, source):
		"""
		Merges the source dictionary into the target.
		Cannot merge arrays, always overwrites.

		:param target: a target dictionary
		:param source: a dictionary
		:return: None
		"""
		for key, value in source.items():
			if (key in target) and isinstance(target[key], dict) \
					and isinstance(value, dict):
				self.merge(target[key], value)
			else:
				target[key] = value



	def __getitem__(self, item):

		try:
			return self.data[item]
		except Exception as e:
			print('Exception -> Config::__getitem__{}'.format(e))
			return None



	def __setitem__(self, key, value):
		"""

		:param key:
		:param value:
		:return:
		"""
		self.data[key] = value



	def set_datasource_properties(self):

		self.dbconn = MysqlConn()

		# Urls
		self.urls = self.dbconn.select_urls()
		if not self.urls:
			raise HunpyException('Urls table might be empty')
		self.data['urls'] = self.urls


		# Adservers
		self.adservers = self.dbconn.select_adservers()
		if not self.adservers:
			raise HunpyException('Adservers table might be empty')
		self.data['adservers'] = self.adservers


		# Placements
		self.placements = self.dbconn.select_placements()
		if not self.placements:
			raise HunpyException('Placements table might be empty')
		self.data['placements'] = self.placements



	def get_url_id_by_value(self, value):
		"""
		Iterate a list of tuples inside a dictionary
		"""
		for key, data in self.data.items():
			if key == 'urls':
				for i, element in data:
					if element == value:
						print(i)




	# def set(self, key, value):
	# 	if key not in self.data:
	# 		self.data[key] = value


	# def get(self, key):
	# 	if key in self.data:
	# 		return self.data[key]



################################################
# conf = Config('hunpy')
# conf.load('../config/hunpy.yml')
# conf.set_datasource_properties()
# chrome_options = conf.__getitem__('chrome.options')
# urls = conf.__getitem__('urls')
# print(chrome_options)
