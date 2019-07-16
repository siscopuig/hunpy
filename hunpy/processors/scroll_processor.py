# -*- coding: utf-8 -*-

import time
from hunpy.processor import Processor


class ScrollProcessor(Processor):

	def __init__(self, driver, config, datasource):

		super().__init__(driver, config, datasource)

		self.total_height = config['js.total.height']

		self.scroll_top = config['js.scroll.top']

		self.scroll_max_num = config['js.scroll.max.number']

		self.window_height = config['chrome.window.height']

		self.scroll_down = config['js.scroll.down']

		self.time_wait_scroll = config['js.time.wait.scroll']


	def process(self, page):

		try:
			total_height = self.driver.execute_javascript(self.total_height)
			max_scroll = int(self.scroll_max_num)
			scroll_down = self.window_height
			height_counted  = 0
			counter = -1

			while height_counted <= total_height:

				counter += 1
				height_counted = height_counted + scroll_down
				remaining_height = total_height - height_counted

				if remaining_height > scroll_down:
					self.driver.execute_javascript(self.scroll_down.format(scroll_down))
					time.sleep(self.time_wait_scroll)

				# Stops at certain amount of scrolls
				if counter >= max_scroll:
					break

			# Scroll top
			self.driver.execute_javascript(self.scroll_top)

		except Exception as exception:
			self.log.error('Exception in ScrollProcessor: {}'.format(exception))












