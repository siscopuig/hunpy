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



