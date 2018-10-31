from src.extractors.container_extractor import ContainerExtractor
from ordered_set import OrderedSet
from src.advert import Advert
from src.utils.utils_strings import UtilsString
from src.log import Log
# from src.utils.utils_date import UtilsDate


class IframeExtractor(ContainerExtractor):
	"""
	item.iframe_srcs can have one or many sources
	"""


	def __init__(self, driver, config):
		ContainerExtractor.__init__(self, driver, config)
		self.log = Log()


	def set_item(self, item, container):

		item.element = container.element
		item.location = container.location
		item.size = container.size

		# Convert to an ordered list
		# An OrderedSet is a custom MutableSet that remembers its order,
		# so that every entry has an index that can be looked up.
		item.iframe_srcs = OrderedSet()
		item.img_srcs = OrderedSet()
		item.img_hrefs = OrderedSet()
		item.img_onclicks = OrderedSet()
		item.ids = OrderedSet()
		item.names = OrderedSet()
		item.titles = OrderedSet()
		item.styles = OrderedSet()
		self.append_item_info(item, container)

		# Convert sets to list for better handle
		item.iframe_srcs = list(item.iframe_srcs)
		item.img_srcs = list(item.img_srcs)
		item.img_hrefs = list(item.img_hrefs)
		item.img_onclicks = list(item.img_onclicks)
		item.ids = list(item.ids)
		item.names = list(item.names)
		item.titles = list(item.titles)
		item.styles = list(item.styles)
		item.is_iframe = True


	def append_item_info(self, item, container):

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
			# Attributes come from Image class
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


		# Append iframes into iframe
		for iframe in container.iframes:
			self.append_item_info(item, iframe)

		return True


	def iframes_extractor(self, containers):
		"""
		Process iframes & images inside
		"""

		# item_extractor method call
		items = self.get_items(containers)


		adverts = []
		for i, item in enumerate(items):

			advert = Advert()

			# Function to process iframes sources
			if not self.process_iframes(item) and not self.process_images(item):
				print('No iframes sources found')
				continue

			self.set_advert(advert, item)

			adverts.append(advert)


		# Adverts list
		return adverts


	def process_iframes(self, item):
		"""
		This approach returns first src processed

		:param item:
		:return:
		"""

		# On here instance `item properties needs to be filled`
		# @TODO: match source in database

		for i, src in enumerate(item.iframe_srcs):


			if not self.process_source(src, item):
				continue

			link = self.extract_link_from_attributes(item)
			if not link:
				item.landing = self.process_landing(item)
			else:
				item.landing = link

			if not item.is_content:
				return False

			return True


	def process_images(self, item):
		"""
		This approach returns first src processed
		:param item:
		:return:
		"""

		for i, src in enumerate(item.img_srcs):

			if not self.process_source(src, item):
				continue

			link = self.extract_link_from_attributes(item)
			if not link:
				item.landing = self.process_landing(item)
			else:
				item.landing = link

			if not item.is_content:
				return False

			return True


	def extract_link_from_attributes(self, item, link=''):
		"""

		:param item:
		:param link:
		:return:
		"""
		if item.img_hrefs:
			link = self.get_link(item.img_hrefs)
			if link:
				print('Link: ({link}) extracted from img_hrefs'.format(link=link))
		elif item.img_onclicks:
			link = self.get_link(item.img_onclicks)
			if link:
				print('Link: ({link}) extracted from img_onclicks'.format(link=link))
		elif item.styles:
			link = self.get_link(item.styles)
			if link:
				print('Link: ({link}) extracted from styles'.format(link=link))

		return link


	def get_link(self, list):

		for string in list:
			url = UtilsString.get_url_from_string(string)
			if url:
				return url

		return ''



































