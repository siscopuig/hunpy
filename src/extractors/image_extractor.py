from src.extractors.container_extractor import ContainerExtractor
from src.advert import Advert
from src.searchers.image_searcher import ImageSearcher
from src.utils.utils_date import UtilsDate
from src.utils.utils_strings import UtilsString




class ImageExtractor(ContainerExtractor):


	def __init__(self, driver, config):

		super().__init__(driver, config)




	def set_item(self, item, container):

		item.element 		= container.element
		item.size 			= container.size
		item.location 		= container.location
		item.img_src 		= container.src
		item.img_onclick 	= container.onclick
		item.img_style 		= container.style
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

			if not self.process_source(item):
				continue

			self.set_advert(advert, item)

			adverts.append(advert)



	def get_landing_link_from_item(self, item, link=''):



		pass

###############################################










