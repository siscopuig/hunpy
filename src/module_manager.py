import importlib
from log import Log


class ModuleManager:

	def __init__(self, driver, config, datasource):

		self.log = Log()
		self.driver = driver
		self.config = config
		self.datasource = datasource
		self.processors = {}


	def create_processors(self, processors):


		module_dir   = 'processors'

		for module_name in processors:
			cls = self.import_class(self.get_class_name(module_name), module_name, module_dir)
			if cls:
				self.processors[module_name] = cls(self.driver, self.config, self.datasource)


	def get_processors(self):

		return self.processors


	def import_class(self, cls_name, module_name, module_dir):
		"""

		:return:
		"""
		try:

			module = importlib.import_module(module_dir + '.' + module_name)
			return getattr(module, cls_name)
		except Exception as error:
			self.log.debug('Exception importing class: {}'.format(error))


	def get_class_name(self, module_name, cls_name=''):
		"""
		Get class name by module name:
		 - Split module name (iframe_processor -> ['iframe', 'processor']
		 - Uppercase first character + string with first character removed
		"""

		for name_part in module_name.split('_'):
			cls_name += ''.join([name_part[:1].upper() + name_part[1:]])
		return cls_name


