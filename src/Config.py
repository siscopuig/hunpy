

class Config(object):

	config_data = {}

	def __init__(self, name):

		if name not in Config.config_data:
			Config.config_data[name] = {}
		self.data = Config.config_data[name]


	def load(self, file_paths):
		"""
		Loads multiple file paths into the config, merging them in order.

		:param file_paths:
		:return:
		"""

		if file_paths:

			if not isinstance(file_paths, list):
				file_paths = [file_paths]

			for file_path in file_paths:
				with open(path_utils.get_abs_path(file_path), 'r') as yml_file:
					self.update(yaml.load(yml_file))

