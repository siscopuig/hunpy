from driver import Driver
from page import Page
from log import Log
from utils.utils_date import UtilsDate
import importlib
import traceback
import subprocess
import sys


class Handler:


	processors = None


	def __init__(self, config, datasource):

		self.log = Log()
		self.config = config
		self.datasource = datasource
		self.driver = None
		self.page = None


	def search(self):

		date = UtilsDate.get_date()

		urls = self.datasource.get_urls()

		for url in urls:

			# For debugging purposes:
			# url['url'] = 'http://localhost:63342/hunpy/lab/html_templates/html_main_document.html'
			# url['id'] = 1

			try:

				# Get driver instance
				if self.driver is None:
					self.driver = Driver()
					self.log.info('Chromedriver started')
					self.driver.start()

				# Open url in browser
				self.driver.open(url['url'], 4)
				self.log.info('Page opened: {}'.format(url['url']))

				# Open a page instance
				self.page = Page(self.driver, url['id'], url['url'])

				# Create processors (tuple)
				self.processors = self.create_processors(self.driver, self.config, self.datasource)

				# Iterate processors (tuple)
				for name, processor in self.processors.items():
					processor.process_start(self.page, processor_name=name)

				# Count cycle
				self.datasource.count_cycle(url['id'], date)


			except Exception as e:
				print(traceback.format_exc())

				exception = str(e).replace('\n', '')
				if 'timeout' in exception:
					self.handle_timeout()

				self.log.error(exception)
				self.driver.close()
				self.driver = None



	def handle_timeout(self):

		try:

			retcode = subprocess.call(["pkill", "-f", "chrome"])
			if retcode < 0:
				self.log.warning('Child was terminated by signal, -retcode: ({})'.format(-retcode, file=sys.stderr))
			else:
				self.log.warning('Child returned, retcode:({})'.format(retcode, file=sys.stderr))

		except OSError as e:
			self.log.error('Execution failed: OSError: {}'.format(e, file=sys.stderr))



	def create_processors(self, driver, config, datasource):
		"""

		:param driver:
		:param config:
		:param datasource:
		:return:
		"""

		module_names = [
			'image_processor',
			'iframe_processor',
			'storage_processor'
		]
		module_dir   = 'processors'

		objects = {}
		for module_name in module_names:
			cls = self.import_class(self.get_class_name(module_name), module_name, module_dir)
			if cls:
				objects[module_name] = cls(driver, config, datasource)

		return objects



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

