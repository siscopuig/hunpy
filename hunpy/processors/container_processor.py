# -*- coding: utf-8 -*-

import numpy as np
import uuid
import asyncio
import time
from selenium.common.exceptions import TimeoutException
from hunpy.utils.utils_strings import UtilsString
from hunpy.utils.utils_url import encode_url
from hunpy.item import Item
from hunpy.advert import Advert, AdvertState
from hunpy.processor import Processor
from hunpy.log import Log
from hunpy.utils.utils_requests import UtilsRequest


class ContainerProcessor(Processor):

	def __init__(self, driver, config, datasource):

		super().__init__(driver, config, datasource)

		self.log = Log()
		self.driver = driver
		self.config = config
		self.datasource = datasource
		self.src_ignore_iframe = self.config['src.ignore.iframe']
		self.src_ignore_landing = self.config['src.ignore.landing']
		self.max_src_chars = int(self.config['max.source.len'])
		self.utilrequest = UtilsRequest(self.config['http_bad_request'], self.config['headers'])


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

		return []


	def set_item(self, item, container):
		"""
		Is overriding IframeExtractor & ImageExtractor
		"""
		return False


	def process(self, page):

		containers = self.get_containers(page)

		if len(containers) <= 0:
			self.log.debug('No containers found')
			return True

		items = self.get_items(containers)

		if not self.process_items(items, page):
			return False

		return True


	def process_source(self, item, advert):

		return False


	def process_items(self, items, page):

		for item in items:

			advert = Advert()

			# Goes to (IframeProcessor & ImageProcessor)
			# Sets parts of Advert object
			if not self.process_source(item, advert):
				continue

			# If an advert is duplicated in the same page continue the loop.
			# At this point info has been gathered previously and there is
			# no need to process some elements again.
			if self.process_duplicate_advert_in_page(advert):
				continue

			# Process existing advert in database.
			if not self.process_existing_advert(advert):
				continue

			# Process links from anchors or clicking elements.
			if not self.process_advertiser(item, advert):
				continue

			# Add advert in list.
			page.adverts.append(advert)

			self.log.info(advert.__str__())

		return True


	def process_duplicate_advert_in_page(self, advert):

		# Update current advert seen on page
		for page_advert in self.page.adverts:

			if page_advert.src == advert.src:
				page_advert.instances += 1

				self.log.info('Advert instance incremented +1 for source: {}'.format(page_advert.src))

				return True

		return False


	def process_existing_advert(self, advert):

		existing = self.datasource.is_source_in_database(advert.src)

		if existing:

			advert.state = AdvertState.EXISTING

			if not existing['id']:
				self.log.debug('Advert not found in database, source: ({})'.format(advert.src))
				return False
			advert.id = existing['id']

			if not existing['uid']:
				self.log.debug('Advert not found in database, source: ({})'.format(advert.src))
				return False
			advert.uid = existing['uid']

			if existing['advertiser']:
				advert.advertiser = existing['advertiser']
			else:
				self.log.debug('Advertiser not found, id: ({}) url_id: ({})'.format(existing['id'], self.page.url_id))

		else:
			advert.state = AdvertState.NEW
			advert.uid = self.get_uid()

		return True


	def set_advert(self, advert, item):

		advert.src = encode_url(item.src)
		advert.url_id = self.page.url_id
		advert.size = item.size
		advert.location = item.location
		advert.finfo = item.finfo
		advert.iframe_element = item.element
		advert.xpath = item.xpath
		advert.is_known_placement = item.is_known_placement

		if not advert.src:
			print('stop')


	def is_src_matching_invalid_pattern(self, src, domain):
		"""
		Validates source
		"""

		# Ignore source if greater than config value
		# if len(src) > self.max_src_chars:
		# 	self.log.debug('Exceed max number of characters: ({}), source: ({})'.format(self.max_src_chars, src))
		# 	return True

		# Ignore dummy source
		if src in self.src_ignore_iframe:
			self.log.debug('Invalid source ({}) '.format(src))
			return True

		# Ignore domain
		if UtilsString.match_string_in_list(domain, self.datasource.get_ignore_domain()):
			self.log.debug('Domain src ({}) is in source ignore domain'.format(domain))
			return True

		apply_ignore_path = False
		if domain in self.config['src.ignore.path.domain.exceptions']:
			self.log.debug('Ignore path validation skipped, adserver domain: ({})'.format(domain))
			apply_ignore_path = True

		# Ignore path
		source_paths = UtilsString.get_paths_from_source(src)
		if not apply_ignore_path and UtilsString.match_string_parts_in_list(source_paths,
																			self.datasource.get_ignore_path()):
			self.log.debug('Ignored source by ignore path, src: ({})'.format(src))
			return True

		return False


	def process_stripped_source(self, src):

		stripped_source = UtilsString.strip_query_in_source(src)

		response = self.utilrequest.get_http_response(stripped_source)

		if response:
			return response
		else:
			response = self.utilrequest.get_http_response(src)
			if response:
				return response

		return False


	def process_advertiser(self, item, advert):

		if not advert.advertiser:

			# Anchors
			link = self.get_link_from_anchors(item)
			if link:
				self.log.debug('Link obtained from img hrefs: {}'.format(link))
				item.landing = link

			# Clicking
			else:
				landing = self.process_landing(item)
				if not landing:
					return False

			if item.landing:
				advert.landing = item.landing
				advert.advertiser = UtilsString.get_domain(item.landing)

		return True


	def find_advertiser_by_click(self, item):

		element = item.element
		if item.xpath:
			element = self.driver.find_element_by_xpath(item.xpath)
			if not element:
				self.log.debug('Unable to find landing element by item.xpath: {}'.format(item.xpath))
				return False

		result = self.driver.click_on_element(element)
		if result is None:
			self.log.debug('Item element not visible to click on it')
			return False

		return True


	def process_landing(self, item):

		# Switch to main document
		if not self.driver.switch_to_window_default_content(self.page.main_window_handle):
			self.log.error('Unable to switch to the main window document')

		# New modification
		if not self.find_advertiser_by_click(item):
			return False

		# Wait a bit for the new tab to be loaded
		time.sleep(2)

		# Did it open a new window?
		windows = self.driver.get_window_handle()
		if len(windows) == 1:
			self.log.debug('CLicking on element did not open a new tab')

			# Check that the main window did not redirect to another page
			current_url = self.driver.get_current_url()
			if current_url != self.page.url:
				self.log.debug('Main window redirected to: {}'.format(current_url))
				return False

		try:
			# Retrieve landing from new tab and validate it
			landing = self.get_landing_source()

		except TimeoutException as e:
			self.log.warning('Timeout error accessing url on tab: ({})'.format(e))
			self.driver.close_window_except_main(windows)
			return False

		if not landing:
			return False

		# Set landing in item
		item.landing = landing
		item.advertiser = UtilsString.get_domain(landing)
		return True


	def get_landing_source(self, landing=None):

		landings = []

		windows = self.driver.get_window_handle()

		self.log.debug('Number of windows: ({})'.format(len(windows)))

		for window in windows:

			if window != self.page.main_window_handle:

				self.driver.switch_to_window(window)

				# Get landing url
				landing = self.driver.get_current_url()
				if landing:
					landings.append(landing)
				else:
					self.log.debug('Not possible to get landing url from tab.')
					self.driver.switch_to_window(self.page.main_window_handle)

		# Switch back to the main window
		self.driver.switch_to_window(self.page.main_window_handle)
		self.driver.close_window_except_main(windows)
		self.log.debug('Switched to main window: ({})'.format(self.page.main_window_handle))

		# Validate landings
		if landings:
			for landing in landings:
				if self.is_landing_invalid(landing):
					continue
		return landing


	def get_link_from_anchors(self, item):

		if item.img_hrefs:

			for source in item.img_hrefs:

				link = UtilsString.get_url_from_string(source)
				if not link:
					continue

				if self.is_landing_invalid(link):
					continue
				return link

		return False


	def is_landing_invalid(self, landing):

		# Is landing source already invalid
		if landing in self.src_ignore_landing:
			self.log.debug('Ignored invalid landing: ({})'.format(landing))
			return True

		# Is landing domain a known ad server
		domain = UtilsString.get_domain(landing)
		if UtilsString.match_string_in_list(domain, self.datasource.get_adservers()):
			self.log.debug('Landing domain ({}) in adservers'.format(domain))
			return True

		# Is landing domain in ignore domain
		if UtilsString.match_string_in_list(domain, self.datasource.get_ignore_domain()):
			self.log.debug('Landing domain {} in ignore domain'.format(domain))
			return True

		return False


	def get_uid(self):
		"""
		Generate a random UUID
		:return: 3c3f9dc8-3491-46d3-aa63-fcd4af556276
		"""
		return uuid.uuid4().__str__()


	def process_anchors(self, item, advert):

		if not advert.advertiser:

			link = self.get_link_from_anchors(item)
			if link:
				advert.landing = link
				advert.advertiser = UtilsString.get_domain(link)

		return True


	def is_valid_http_response(self, items):
		"""
		Experimental. Not in use for now.

		:param items:
		:return:
		"""

		start = time.time()
		loop = asyncio.get_event_loop()
		loop.run_until_complete(self.utilrequest.process_http_requests(items))
		loop.run_until_complete(asyncio.sleep(0))
		print('Total requests: {}'.format(len(items)))
		print("--- %s seconds ---" % (round(time.time() - start, 2)))
