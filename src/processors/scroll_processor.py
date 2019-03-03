from processor import Processor
import time


class ScrollProcessor(Processor):

	def __init__(self, driver, config, datasource):

		super().__init__(driver, config, datasource)


	def process(self, page):

		try:
			total_height = self.driver.execute_javascript(self.config['jcs.total.height'])
			max_scroll = int(self.config['jcs.scroll.max.number'])
			scroll_down = self.config['chrome.window.height']
			height_counted  = 0
			counter = -1

			while height_counted <= total_height:

				counter += 1
				height_counted = height_counted + scroll_down
				remaining_height = total_height - height_counted

				if remaining_height > scroll_down:
					self.driver.execute_javascript(self.config['jcs.scroll.down'].format(scroll_down))
					time.sleep(0.2)

				# Stops at certain amount of scrolls
				if counter >= max_scroll:
					break

			# Scroll top
			self.driver.execute_javascript(self.config['jcs.scroll.top'])

		except Exception as e:
			self.log.error('Error on scroll processor: {}'.format(e))












