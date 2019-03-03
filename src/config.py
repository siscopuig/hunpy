from log import Log
from utils.utils_files import get_abs_path
import yaml


class Config:

	def __init__(self):

		self.log = Log()
		self.data = {}


	def load(self, file_paths):

		for path in file_paths:

			try:
				with open(get_abs_path(path), 'r') as yml_file:
					self.fill(yaml.load(yml_file))

			except yaml.YAMLError as ex:
				raise 'Error loading yaml config file: {}'.format(ex)


	def fill(self, yml_file):

		for key, value in yml_file.items():
			self.data[key] = value