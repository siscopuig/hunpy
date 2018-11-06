
from src.html_element import HtmlElement
from src.utils.utils_strings import UtilsString


class Page(HtmlElement):
	"""
	This class tries to represent the main document (a complete url)

	Properties:
		- The page itself (src) E.g. (http://www.europeanpensions.net/ep/index.php)
		- The page domain (page_domain) E.g. (europeanpensions.net)
		- adverts from iframes & images from main document
	"""

	def __init__(self, id, url):

		HtmlElement.__init__(self)
		
		# Url id
		self.url_id = id

		# Url page is the main source
		self.src = url

		self.page_domain = UtilsString.get_domain(url)

		self.main_window_handle = None

		# Adverts candidates
		self.adverts = []

		# A list advert sources taken from the page
		self.advert_source_list = []






