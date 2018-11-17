from src.driver import Driver
from src.page import Page
from src.log import Log
import importlib



class Handler:
	"""
	- Get all the config data at this point.
	- Loop over the urls and process url (page)
	-
	"""

	processors = None


	def __init__(self, config, datasource):


		self.config = config
		self.datasource = datasource
		self.log = Log()
		self.driver = None
		self.page = None


	def search(self):

		urls = self.datasource.get_urls()

		for url in urls:

			# For debugging purposes:
			# url = 'http://localhost:63342/hunpy/lab/html_templates/html_main_document.html'
			# url_id = 1

			# url = 'https://www.trustnet.com/'
			# url = 'http://www.ftadviser.com/'
			# url = 'http://www.europeanpensions.net/ep/index.php'
			# url = 'https://www.theguardian.com/uk'


			url_id = url[0]
			url = url[1]

			try:

				# Get driver instance
				if self.driver is None:
					self.driver = Driver()
					self.log.info('Chromedriver started')
					self.driver.start()

				self.driver.open(url)

				# Open a page instance
				self.page = Page(self.driver, url_id, url)

				# Create processors (tuple)
				self.processors = self.create_processors(self.driver, self.config, self.datasource)

				# Iterate processors (tuple)
				for name, processor in self.processors.items():
					processor.process_start(self.page)

				#print(self.page.adverts)

			except Exception as error:
				print(error)
				#self.log.error(error)
				self.driver.close()
				self.driver = None



	def create_processors(self, driver, config, datasource):
		"""

		:param driver:
		:param config:
		:param datasource:
		:return:
		"""

		module_names = ['image_processor', 'iframe_processor', 'storage_processor']
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


#################################
# try:

# 	self.driver.open(url, 4)
# 	height = self.driver.driver.execute_script("return document.body.parentNode.scrollHeight")
# 	self.driver.driver.set_window_size(1366, height)
# 	self.driver.driver.save_screenshot('/home/sisco/PycharmProjects/hunpy/screenshot.png')
# except Exception as e:
# 	print(e)

