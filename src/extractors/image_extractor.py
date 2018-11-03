from src.extractors.container_extractor import ContainerExtractor
from src.advert import Advert
from src.searchers.image_searcher import ImageSearcher
from src.utils.utils_strings import UtilsString
from src.log import Log
# from src.utils.utils_date import UtilsDate



class ImageExtractor(ContainerExtractor):


	def __init__(self, driver, config):

		super().__init__(driver, config)

		self.log = Log()




	def set_item(self, item, container):
		"""

		:param item:
		:param container:
		:return:
		"""
		item.element 		= container.element
		item.size 			= container.size
		item.location 		= container.location
		item.src 			= container.src
		item.onclick 		= container.onclick
		item.style 			= container.style
		item.a_href 		= container.a_href
		item.a_onclick 		= container.a_onclick
		item.a_style 		= container.a_style


	def search_images(self):

		img = ImageSearcher(self.driver)
		return img.find_images()


	def images_extractor(self, containers):


		items = self.get_items(containers)

		adverts = []
		for i, item in enumerate(items):

			advert = Advert()

			if not self.process_source(item.src, item):
				continue

			link = self.get_landing_link_from_item(item)
			if not link:
				item.landing = self.process_landing(item)
			else:
				item.landing = link

			if not item.is_content:
				return False

			self.set_advert(advert, item)

			adverts.append(advert)

		return adverts


	def get_landing_link_from_item(self, item, link=''):

		# a_href, a_onclick, a_style,
		# src, onclick, style

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

		return link













