from processor import Processor

# Filesystem
# captures/2018-12-01/trustnet/96a2f3df-2c52-4b0b-8b69-24de3bcd6259


class CapturesProcessor(Processor):


	def __init__(self, driver, config, datasource):

		super().__init__(driver, config, datasource)


	def process(self, page):
		pass