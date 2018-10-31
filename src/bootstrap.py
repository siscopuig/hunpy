from src.config import Config
from src.handler import Handler
# from src.log import Log
# import datetime
# import os


class Bootstrap:


	def __init__(self):
		self.config = None



	def start(self):

		self.config = Config('hunpy')
		self.config.load('../config/hunpy.yml')
		self.config.set_datasource_properties()

		handler = Handler(self.config)
		handler.search()


	# def load_configuration_from_file(self):
	# 	self.config = Config('hunpy')
	# 	self.config.load('../config/hunpy.yml')
	# 	self.config.set_datasource_properties()


##########################################
obj = Bootstrap()
obj.start()

# driver.click_using_middle_button(element)
#
# windows = driver.get_windows_handler()
# driver.get_driver().switch_to_window(windows[1])
# landing = driver.get_driver().current_url
# print(landing)
# driver.get_driver().close()
# driver.get_driver().switch_to_window(windows[0])
# element = driver.find_element_by_xpath('.//img')






