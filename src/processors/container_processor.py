
from src.item import Item
from src.advert import Advert, AdvertState
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
		self.datasource = datasource
		self.http_bad_request = self.config['http_bad_request']
		self.src_ignored_landing = self.config['src.ignore.landing']


	def get_items(self, containers):

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


	def process_source(self, item, advert):
		"""

		:param item:
		:param advert:
		:return:
		"""

		return False


	def process_items(self, items, page):
		"""
		@todo:
		-	Process whether an advert has been seen in page already.
		"""

		for i, item in enumerate(items):

			advert = Advert()

			# Goes to (IframeProcessor & ImageProcessor)
			if not self.process_source(item, advert):
				continue

			# If an advert is duplicated in the same page continue the loop.
			# All info has been gathered previously and there is no need to
			# process some elements again
			if self.count_duplicate_advert_in_page(advert):
				continue


			if not self.process_existing_advert(advert):
				continue


			self.process_advertiser(item, advert)

			# Set advert
			self.set_advert(advert, item)

			# Append advert in
			page.adverts.append(advert)

		return True


	def count_duplicate_advert_in_page(self, advert):

		# - At this point the source is in advert object.
		# - If current advert.src is in page.adverts list, if true,
		#	increment instance

		# Update current advert seen on page
		for page_advert in self.page.adverts:

			if page_advert.src == advert.src:

				page_advert.instances += 1

				self.log.info('Advert instance incremented +1 for source: {}'.format(page_advert.src))

				return True

		return False


	def process_existing_advert(self, advert):

		# - Check in database for an existing source.
		# - Request id, uid, advertiser
		# - Check if advertiser domain is not blank, if blank, retrieve it.


		existing = self.datasource.is_source_in_database(advert.src)
		if existing:

			advert.state = AdvertState.EXISTING

			if not existing['id']:
				self.log.info('Advert not found in database, source: ({})'.format(advert.src))
				return False

			# @todo:
			# advert.id is not defined in Adverts yet

			advert.id  = existing['id']
			advert.uid = existing['uid']

			if existing['advertiser']:
				advert.advertiser = existing['advertiser']
			else:
				self.log.info('Advertiser not found, id: ({}) url_id: ({})'.format(existing['id'], self.page.url_id))

		return True


	def process_advertiser(self, item, advert):

		if not advert.advertiser:

			if self.get_link_from_anchors(item):
				return True

			self.process_landing(item)

		return True


	def set_advert(self, advert, item):
		"""

		:param advert:
		:param item:
		:return:
		"""
		advert.url_id  	= self.page.url_id
		advert.width 	= item.size[0]
		advert.height 	= item.size[1]
		advert.finfo 	= item.finfo


		if not advert.uid:
			advert.uid = self.get_uid()

		if item.landing:
			advert.landing = item.landing
			advert.advertiser = UtilsString.get_domain(item.landing)
		else:
			advert.landing = item.landing
			advert.advertiser = item.advertiser

		advert.datetime = UtilsDate.get_datetime()
		advert.is_iframe = item.is_iframe


		# For debugging purposes only:
		self.log.debug(advert.__str__())


	def is_src_matching_invalid_pattern(self, src, domain):

		# @todo:
		# Improve source validation

		if UtilsString.match_string_in_list(domain, self.datasource.get_ignore_domain(), 'ignore_domain'):
			self.log.debug('Domain src ({}) is in source ignore domain'.format(domain))
			return True

		if UtilsString.match_string_parts_in_list(src, self.datasource.get_ignore_path(), 'ignore_path'):
			self.log.debug('Source path from src: ({}) in src ignore path list'.format(src))
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


		main_window_handle = self.driver.get_main_window_handle()
		if main_window_handle != self.page.main_window_handle:
			self.driver.switch_to_window(self.page.main_window_handle)
			self.log.info('Switched to main window: {}'.format(self.page.main_window_handle))


		# Click on item element
		result = self.driver.click_on_element(item.element)
		if result is None:
			self.log.debug('Item element not visible to click on it')
			return False

		# Did it open a new window?
		windows = self.driver.get_window_handle()
		if len(windows) == 1:
			self.log.info('CLicking on element did not open a new tab')
			if self.page.main_window_handle == windows[0]:
				#self.log.info('Page main window: {} equal to :{}'.format(self.page.main_window_handle, windows[0]))
				return False

		# Check that the main window did not redirect to another page
		current_url = self.driver.get_current_url()
		if current_url != self.page.url:
			self.log.info('Main window redirected to: {}'.format(current_url))
			return False


		# Retrieve landings
		landing = self.get_landing_source()
		if not landing:
			return False


		# Set landing in item
		item.landing = landing
		item.advertiser = UtilsString.get_domain(landing)
		return True


	def get_landing_source(self, landing=None):

		# An element could be broken when clicking on an element could redirect
		# to another address without open a new tab. Solutions:
		# 	- Improve different click on element methods and checks.
		#
		#
		# We arrived at this point being clicked on element. We expect to have
		# 1,2 or more windows

		landings = []

		windows = self.driver.get_window_handle()
		self.log.info('Number of windows: ({})'.format(len(windows)))

		for i, window in enumerate(windows):

			if window != self.page.main_window_handle:
				self.driver.switch_to_window(window)
				self.log.debug('Switched to new window: Switched to window ({})'.format(window))

				# Get landing url
				landing = self.driver.get_current_url()
				if landing:
					landings.append(landing)
				else:
					self.log.debug('Not possible to get landing url from tab.')
					self.driver.switch_to_window(self.page.main_window_handle)


		# Switch back to the main window
		self.driver.close_window_except_main(windows)
		self.driver.switch_to_window(self.page.main_window_handle)
		self.log.info('Switched to main window: ({})'.format(self.page.main_window_handle))


		if landings:

			for landing in landings:

				# Check if landing is not an invalid source
				if landing in self.src_ignored_landing:
					self.log.debug('Landing ({}) path in src ignored landing'.format(landing))
					continue

				# Check if landing domain is equal to page domain
				domain = UtilsString.get_domain(landing)
				if domain == self.page.page_domain:
					self.log.info('Landing domain ({}) equal to page domain {}'.format(domain, self.page.page_domain))


		return landing


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


	def get_link_from_anchors(self, item):

		if item.img_hrefs:

			for source in reversed(item.img_hrefs):

				link = UtilsString.get_url_from_string(source)

				if not link:
					continue

				# Is landing source already invalid
				if link in self.src_ignored_landing:
					self.log.debug('Landing source {} in ignored landing list'.format(link))
					continue

				# Is landing domain in ignore domain
				domain = UtilsString.get_domain(link)
				if domain in self.datasource.get_ignore_domain():
					self.log.debug('Landing domain {} in ignore domain list'.format(domain))
					continue


				item.landing = link
				item.advertiser = UtilsString.get_domain(link)
				self.log.info('Link obtained from img hrefs: {}'.format(link))
				return True

		return False


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




















