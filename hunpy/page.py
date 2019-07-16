# -*- coding: utf-8 -*-

from hunpy.html_element import HtmlElement
from hunpy.utils.utils_strings import UtilsString


class Page(HtmlElement):
	"""
	This class tries to represent the main document (a complete url).
	"""

	def __init__(self, driver, id, url):

		HtmlElement.__init__(self)

		# Url id
		self.url_id = id

		# Url page from datasource
		self.origin_url = url

		# Current url
		self.url = driver.get_current_url()

		# Url page is the main source
		self.src = url

		# Main page domain
		self.page_domain = UtilsString.get_domain(url)

		# Main window handle id
		self.main_window_handle = driver.get_main_window_handle()

		# Adverts candidates
		self.adverts = []

		# A list advert sources taken from the page
		self.advert_source_list = []






