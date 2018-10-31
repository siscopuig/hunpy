
from src.item import Item
from src.utils.utils_requests import get_http_request
import numpy as np
import uuid
from src.utils.utils_strings import UtilsString
from src.utils.utils_requests import process_http_requests
from src.utils.utils_date import UtilsDate
import asyncio
import time
from src.log import Log

class ContainerExtractor:
	"""
	"""

	def __init__(self, driver, config):

		self.log = Log()
		self.driver = driver
		self.config = config
		self.http_bad_request = self.config['http_bad_request']
		self.adservers = list(self.config['adservers'])
		self.placements = list(self.config['placements'])
		self.src_ignored_domains = self.config['src.ignored_domains']
		self.src_ignored_subdomains = self.config['src.ignored_subdomains']
		self.src_ignored_landing = self.config['src.ignore.landing']
		self.page_domain = UtilsString.get_domain(self.config.__getitem__('main_document'))




	def get_items(self, containers):

		items = np.empty(len(containers), dtype=np.object)
		for i, container in enumerate(containers):
			item = Item()
			self.set_item(item, container)
			items[i] = item

		return items



	def set_item(self, item, container):
		"""
		Is overriding in:
			IframeExtractor
			ImageExtractor
		"""
		return False



	def set_advert(self, advert, item):
		"""

		:param advert:
		:param item:
		:return:
		"""
		advert.src 		= item.src
		advert.width 	= item.size[0]
		advert.height 	= item.size[1]
		advert.uid 		= self.get_uid()
		advert.datetime = UtilsDate.get_datetime()
		advert.finfo 	= item.finfo
		advert.landing 	= item.landing
		advert.is_iframe = item.is_iframe
		if item.landing:
			advert.advertiser = UtilsString.get_domain(item.landing)

		# For debugging purposes only:
		self.log.debug(advert.__str__())



	def process_source(self, src, item):
		"""
		This a generic method to process sources from Iframes & Images

		"""

		domain = UtilsString.get_domain(src)
		if self.is_src_matching_invalid_pattern(src, domain):
			return False


		# Is a known placement
		if UtilsString.match_placement(self.placements, item.size[0], item.size[1]):
			item.is_known_placement = True


		# Is a known ad server
		if UtilsString.match_string_in_list(domain, self.adservers):
			item.is_known_adserver = True


		# Is page domain equal to source domain
		if domain == self.page_domain:
			item.is_page_domain = True


		# If source domain is equal
		if item.is_page_domain and not item.is_known_placement:
			self.log.debug('Invalid source: is page domain ({}) and '
						   'not a known placement source: ({})'.format(self.page_domain, src))
			return False

		if not item.is_known_placement and not item.is_known_adserver:
			self.log.debug('Not known placement ({}), ({}) and not a known placement '
				  'source: ({})'.format(item.size[0], item.size[1], src))
			return False


		source, finfo = self.process_stripped_source(src)
		if not finfo:
			return False

		item.src = source
		item.finfo = finfo
		item.is_content = True

		return True


	def is_src_matching_invalid_pattern(self, src, domain):


		# Checks that domain src is not in src ignored domains list
		if domain in self.src_ignored_domains:
			self.log.debug('Domain src ({}) is in source ignored list'.format(domain))
			return True

		# Checks that any part of the src is not in the list of text paths
		if UtilsString.match_string_list_in_list(src, self.src_ignored_subdomains):
			self.log.debug('Source path from src: ({}) in src ignored subdomains'.format(src))
			return True


	def process_stripped_source(self, src):
		"""
		# @todo: Check effective link by Curl
		# E.g. http://bs.serving-sys.com/Serving/adServer.bs?cn=brd&pli=1074216618&Page=&Pos=1934671096
		# 	-> https://www.clearbridge.com/global-esg.html?cmpid=cbieu18_eur_web_penage_ros_728x90_wtr
		#
		:return:
		"""

		stripped_source = UtilsString.strip_string(src, '?')
		request = self.is_valid_source_http_request(stripped_source)
		if not request:
			self.log.debug('Invalid http response from stripped source, src: ({}) '.format(stripped_source))
			stripped_source = None

			request = self.is_valid_source_http_request(src)
			if not request:
				self.log.debug('Invalid http response, src: ({}) '.format(src))
				return '', ''

		if stripped_source:
			src = stripped_source

		return src, request['content_type']


	def process_landing(self, item):
		"""
		WebElement of top level iframe (item.element)

		:param item
		:return:
		"""

		result = self.driver.click_on_element(item.element)
		if result is None:
			self.log.debug('Process Landing: element not visible')
			return None


		# Check that a new tab is opened and switch
		if not self.switch_to_new_window():
			return None

		# Get landing url
		landing = self.driver.get_current_url()
		if not landing:
			self.log.debug('ContainerExtractor: Not possible to get landing url from tab.')
			self.driver.close_window_except_main()
			return None


		# Validate landing url
		if UtilsString.match_string_list_in_list(landing, self.src_ignored_landing):
			self.log.debug('Process Landing: a landing {} path in src ignored landing'.format(landing))
			return None

		# Close window and switch to main
		self.driver.close_window_except_main()

		return landing


	def switch_to_new_window(self):

		# @todo: Check that url do not change when click on element.
		# An element could be broken when clicking on an element could redirect
		# to another address without open a new tab. Solutions:
		# 	- Improve different click on element methods and checks.
		#
		# current_url = self.driver.get_current_url()
		# url = self.driver.get_current_url()
		# if current_url == url:
		# 	print('Main url: {} equal to landing {}'.format(current_url, url))

		windows = self.driver.get_window_handle()

		if len(windows) > 2:
			self.log.debug('Switch to new window: Opened ({}) more than one tab.'.format(len(windows)))
			return False

		elif len(windows) == 1:
			self.log.debug('Switch to new window: Did not open a new tab.')
			return False

		else:
			self.driver.switch_to_window(windows[1])
			self.log.debug('Switch to new window: Switched to window ({})'.format(windows[1]))
			return True


	def get_uid(self):
		"""
		Generate a random UUID
		:return: 3c3f9dc8-3491-46d3-aa63-fcd4af556276
		"""
		return uuid.uuid4().__str__()


	def is_valid_source_http_request(self, src):

		request = get_http_request(src)
		if not request:
			return False

		if request['status'] in self.http_bad_request:
			return False

		return request


	def get_landing_link_from_item(self, item, link=''):
		"""


		"""

		if item.a_href:
			self.log.debug('Item value on a_href: {}'.format(item.a_href))
			link = UtilsString.get_url_from_string(item.a_href)

		if item.a_onclick:
			self.log.debug('Item value on a_href: {}'.format(item.a_onclick))
			link = UtilsString.get_url_from_string(item.a_onclick)

		if item.img_style:
			self.log.debug('Item value on a_href: {}'.format(item.a_img_style))
			link = UtilsString.get_url_from_string(item.img_style)

		if item.img_onclick:
			self.log.debug('Item value on a_href: {}'.format(item.img_onclick))
			link = UtilsString.get_url_from_string(item.img_onclick)

		return link


	def is_valid_http_response(self, items):
		"""
		Experimental. Not in use for now.

		:param items:
		:return:
		"""

		start = time.time()
		loop = asyncio.get_event_loop()
		loop.run_until_complete(process_http_requests(items))
		loop.run_until_complete(asyncio.sleep(0))
		print('Total requests: {}'.format(len(items)))
		print("--- %s seconds ---" % (round(time.time() - start, 2)))
		# Total requests: 51
		# --- 5.28 seconds - --





















