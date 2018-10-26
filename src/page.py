
from src.html_element import HtmlElement
from src.utils.utils_strings import UtilsString


class Page(HtmlElement):
	"""
	Main document
	"""

	def __init__(self, url):


		HtmlElement.__init__(self)

		# Url is the main source
		self.src = url

		self.page_domain = UtilsString.get_domain(url)

		self.main_window_handle = None



