# -*- coding: utf-8 -*-

from hunpy.processor import Processor
from hunpy.utils.utils_date import UtilsDate


class StorageProcessor(Processor):

	def __init__(self, driver, config, datasource):

		super().__init__(driver, config, datasource)

		self.date = UtilsDate.get_date()


	def process(self, page):

		if not self.page.adverts:
			return False

		for advert in self.page.adverts:

			if advert.state.name == 'NEW':

				self.datasource.insert_new_advert(advert)
