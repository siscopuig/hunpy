
class Processor:



	def __init__(self, driver, config, datasource):

		self.driver = driver
		self.config = config
		self.datasource = datasource
		self.page = None



	def process_start(self, page):
		"""
		Here time completion could be logged


		"""
		self.page = page


		# Action
		self.process(page)



	def process(self, page):
		"""

		:param page:
		:return:
		"""

		return True



