# -*- coding: utf-8 -*-

from hunpy.processors.container_processor import ContainerProcessor
from hunpy.searchers.image_searcher import ImageSearcher
from hunpy.utils.utils_strings import UtilsString
from hunpy.log import Log


class ImageProcessor(ContainerProcessor):

	def __init__(self, driver, config, datasource):

		super().__init__(driver, config, datasource)

		self.imagesearcher = ImageSearcher(driver, config)

		self.log = Log()


	def set_item(self, item, container):

		item.element 		= container.element
		item.size 			= container.size
		item.location 		= container.location
		item.src 			= container.src
		item.onclick 		= container.onclick
		item.style 			= container.style
		item.a_href 		= container.a_href
		item.a_onclick 		= container.a_onclick
		item.a_style 		= container.a_style


	def get_containers(self, page):

		return self.imagesearcher.find_containers()


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

		if not self.process_image_source(item):
			return False

		# Source taken outside of an iframe, set to false
		advert.isframe = 0

		self.set_advert(advert, item)

		return True


	def process_image_source(self, item):

		if not item.src:
			return False

		domain = UtilsString.get_domain(item.src)
		if self.is_src_matching_invalid_pattern(item.src, domain):
			return False

		if self.datasource.match_placement(item.size[0], item.size[1]):
			item.is_known_placement = True

		if UtilsString.match_string_in_list(domain, self.datasource.get_adservers()):
			item.is_known_adserver = True

		if domain == self.page.page_domain:
			item.is_page_domain = True

		if item.is_page_domain and not item.is_known_placement:
			self.log.debug('Invalid source: is page domain ({}) and not a known placement source: ({})'
						   .format(self.page.page_domain, item.src))
			return False

		if not item.is_known_placement and not item.is_known_adserver:
			self.log.debug('Not known placement ({}), ({}) and not a known placement source: ({})'
						   .format(item.size[0], item.size[1], item.src))
			return False

		result = self.process_stripped_source(item.src)
		if not result['valid']:
			return False

		item.src = result['url']
		item.finfo = result['finfo']

		return True


	def get_link_from_anchors(self, item, link=''):

		if item.a_href:
			self.log.debug('ImageExtractor: Item value on a_href: {}'.format(item.a_href))
			link = UtilsString.get_url_from_string(item.a_href)

		elif item.a_onclick:
			self.log.debug('ImageExtractor: Item value on a_href: {}'.format(item.a_onclick))
			link = UtilsString.get_url_from_string(item.a_onclick)

		elif item.style:
			self.log.debug('ImageExtractor: Item value on a_href: {}'.format(item.style))
			link = UtilsString.get_url_from_string(item.style)

		elif item.onclick:
			self.log.debug('ImageExtractor: Item value on a_href: {}'.format(item.onclick))
			link = UtilsString.get_url_from_string(item.onclick)

		if link and not self.is_landing_invalid(link):
			self.log.debug('Link obtained from img hrefs: {}'.format(link))
			return link

		return False