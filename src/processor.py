from log import Log
import time

class Processor:



	def __init__(self, driver, config, datasource):

		self.log = Log()
		self.driver = driver
		self.config = config
		self.datasource = datasource
		self.page = None


	def process_start(self, page, processor_name):
		"""
		"""

		# Get current timestamp
		start = time.time()


		self.log.info('Processor {} started'.format(processor_name))


		self.page = page


		if not self.driver.switch_to_window_default_content(self.page.main_window_handle):
			self.log.error('Unable to switch to main window default content')
			return False


		# Action
		self.process(page)

		# Log processor completion time
		self.log.info('Processor {} finished in {} seconds'.format(processor_name, round(time.time() - start, 2)))



	def process(self, page):
		"""

		:param page:
		:return:
		"""

		return True



