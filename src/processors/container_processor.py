
from src.item import Item
from src.advert import Advert
from src.utils.utils_requests import get_http_request
from src.processor import Processor
import numpy as np
import uuid
from src.utils.utils_strings import UtilsString
from src.utils.utils_requests import process_http_requests
from src.utils.utils_date import UtilsDate
import asyncio
import time
from src.log import Log

class ContainerProcessor(Processor):
	"""
	"""

	def __init__(self, driver, config, datasource):

		super().__init__(driver, config, datasource)

		self.log = Log()
		self.driver = driver
		self.config = config
		self.http_bad_request = self.config['http_bad_request']
		self.placements = datasource.datasource['placements']
		self.adservers = datasource.datasource['adservers']
		self.ignore_domain_and_path = datasource.datasource['ignore_domain_and_path']
		self.ignore_domain = datasource.datasource['ignore_domain']
		self.ignore_path = datasource.datasource['ignore_path']
		self.src_ignored_landing = self.config['src.ignore.landing']

		# page_domain

		print(0)


	def get_items(self, containers):
		"""
		
		:param containers: 
		:return: items 
		"""
		if not containers.size:
			return np.array([], dtype=np.object)


		items = np.empty(len(containers), dtype=np.object)
		for i, container in enumerate(containers):
			item = Item()
			self.set_item(item, container)
			items[i] = item

		return items


	def get_containers(self, page):
		"""

		:param page:
		:return:
		"""

		return []


	def set_item(self, item, container): # fill_item()
		"""
		Is overriding in:
			IframeExtractor
			ImageExtractor
		"""
		return False


	def process(self, page):
		"""


		"""

		containers = self.get_containers(page)

		if len(containers) <= 0:
			self.log.debug('No containers found')
			return True


		items = self.get_items(containers)


		if not self.process_items(items, page):
			return False

		return True


	def process_items(self, items, page):
		"""

		:param items:
		:param page:
		:return:
		"""

		for i, item in enumerate(items):

			advert = Advert()
			advert.url_id = self.page.url_id

			# Check that source is valid
			if not self.process_source(item, advert):
				continue

			# Process whether an advert has been seen in page already


			# Process landing



			page.adverts.append(advert)

		return True


	def process_source(self, item, source):
		"""

		:param item:
		:param source:
		:return:
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





















