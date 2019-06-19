from .container_processor import ContainerProcessor
from ordered_set import OrderedSet
from ..utils.utils_strings import UtilsString
from ..log import Log
from ..searchers.iframe_searcher import FrameSearcher


class IframeProcessor(ContainerProcessor):

	def __init__(self, driver, config, datasource):

		super().__init__(driver, config, datasource)

		self.framesearcher = FrameSearcher(driver, config)

		self.log = Log()


	def get_containers(self, page):

		return self.framesearcher.find_containers(page)


	def process_source(self, item, advert):

		if not self.process_frame_sources(item) and not \
				self.process_image_sources(item):
			return False

		# Set source taken inside an iframe to true
		advert.isframe = 1

		self.set_advert(advert, item)

		return True


	def process_frame_sources(self, item):

		for i, src in enumerate(item.iframe_srcs):

			domain = UtilsString.get_domain(src)
			if self.is_src_matching_invalid_pattern(src, domain):
				continue

			# Is a known placement
			if self.datasource.match_placement(item.size[0], item.size[1]):
				item.is_known_placement = True

			# Is a known ad server
			if UtilsString.match_string_in_list(domain, self.datasource.get_adservers()):
				item.is_known_adserver = True

			# Is page domain equal to source domain
			if domain == self.page.page_domain:
				item.is_page_domain = True

			# If domain source is equal to domain page and not a known placement
			# most probably is not an ad.
			if item.is_page_domain and not item.is_known_placement:
				self.log.debug('Invalid source: is page domain ({}) and not a known '
							   'placement source: ({})'.format(self.page.page_domain, src))
				continue

			# Unknown placement and unknown adserver needs to be discarded
			if not item.is_known_placement and not item.is_known_adserver:
				self.log.debug('Not known placement ({}), ({}) and not a known '
							   'placement source: ({})'.format(item.size[0], item.size[1], src))
				continue

			source, finfo = self.process_stripped_source(src)
			if not finfo:
				continue

			item.src = source
			item.finfo = finfo
			return True

		return False


	def process_image_sources(self, item):

		for i, src in enumerate(item.img_srcs):

			domain = UtilsString.get_domain(src)
			if self.is_src_matching_invalid_pattern(src, domain):
				continue

			# Is a known placement
			if self.datasource.match_placement(item.size[0], item.size[1]):
				item.is_known_placement = True

			# Is a known ad server
			if UtilsString.match_string_in_list(domain, self.datasource.get_adservers()):
				item.is_known_adserver = True

			# Is page domain equal to source domain
			if domain == self.page.page_domain:
				item.is_page_domain = True

			# If source domain is equal
			if item.is_page_domain and not item.is_known_placement:
				self.log.debug('Invalid source: is page domain ({}) and not a known placement source: ({})'
							   .format(self.page.page_domain, src))
				continue

			if not item.is_known_placement and not item.is_known_adserver:
				self.log.debug('Not known placement ({}), ({}) and not a known placement source: ({})'
							   .format(item.size[0], item.size[1], src))
				continue

			source, finfo = self.process_stripped_source(src)
			if not finfo:
				continue

			item.src = source
			item.finfo = finfo
			return True

		return False


	def set_item(self, item, container):
		"""
		An OrderedSet is a custom MutableSet that remembers its order,
		so that every entry has an index that can be looked up.
		"""

		item.element = container.element
		item.location = container.location
		item.size = container.size
		item.xpath = container.xpath
		item.iframe_srcs = OrderedSet()
		item.img_srcs = OrderedSet()
		item.img_hrefs = OrderedSet()
		item.img_onclicks = OrderedSet()
		item.ids = OrderedSet()
		item.names = OrderedSet()
		item.titles = OrderedSet()
		item.styles = OrderedSet()
		self.append_item_properties(item, container)

		# Convert sets to list for better handle
		item.iframe_srcs = list(item.iframe_srcs)
		item.img_srcs = list(item.img_srcs)
		item.img_hrefs = list(item.img_hrefs)
		item.img_onclicks = list(item.img_onclicks)
		item.ids = list(item.ids)
		item.names = list(item.names)
		item.titles = list(item.titles)
		item.styles = list(item.styles)


	def append_item_properties(self, item, container):

		# Append frame source.
		if container.src:
			item.iframe_srcs.add(container.src)

		# Append frame id.
		if container.id:
			item.ids.add(container.id)

		# Append frame name.
		if container.name:
			item.names.add(container.name)

		# Append frame title.
		if container.title:
			item.titles.add(container.title)

		# Append frame style.
		if container.style:
			item.styles.add(container.style)

		# Append image info.
		for img in container.images:

			if img.src:
				item.img_srcs.add(img.src)

			if img.onclick:
				item.img_onclicks.add(img.onclick)

			if img.style:
				item.styles.add(img.style)

			if img.a_href:
				item.img_hrefs.add(img.a_href)

			if img.a_onclick:
				item.img_onclicks.add(img.a_onclick)

			if img.a_style:
				item.styles.add(img.a_style)

		for iframe in container.iframes:
			self.append_item_properties(item, iframe)

		return True



	def extract_link_from_attributes(self, item, link=''):

		if item.img_hrefs:
			link = self.get_link_from_list(item.img_hrefs)
			if link:
				print('Link: ({link}) extracted from img_hrefs'.format(link=link))
		elif item.img_onclicks:
			link = self.get_link_from_list(item.img_onclicks)
			if link:
				print('Link: ({link}) extracted from img_onclicks'.format(link=link))
		elif item.styles:
			link = self.get_link_from_list(item.styles)
			if link:
				print('Link: ({link}) extracted from styles'.format(link=link))

		return link


	def get_link_from_list(self, list):

		for string in list:
			url = UtilsString.get_url_from_string(string)
			if url:
				return url

		return ''