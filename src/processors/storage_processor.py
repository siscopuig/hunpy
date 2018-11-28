from processor import Processor
from utils.utils_date import UtilsDate



class StorageProcessor(Processor):



	def __init__(self, driver, config, datasource):


		super().__init__(driver, config, datasource)


		self.date = UtilsDate.get_date()



	def process(self, page):


		if not self.page.adverts:
			return False


		for advert in self.page.adverts:


			if advert.state.name == 'NEW':

				# Add new advert
				self.datasource.insert_new_advert(advert)

				# Add instance
				self.datasource.insert_new_instance(
					self.set_new_instance(advert.uid, self.page.url_id, advert.instances, self.date))

			else:
				# Update instance
				self.update_existing_advert(advert)



	def update_existing_advert(self, advert):



		instance_id = self.datasource.is_new_instance(advert.uid, self.page.url_id, self.date)


		if instance_id:
			# there is an existing instance record today (Update instance).
			# Update existing instance record today.
			self.datasource.update_existing_instance(
				self.set_update_instance(instance_id, advert.instances, self.date))

		else:
			# Store new instance record for today
			self.datasource.insert_new_instance(
				self.set_new_instance(advert.uid, self.page.url_id, advert.instances, self.date))



	def set_new_instance(self, uid, url_id, instances, date):

		return {
			"uid": uid,
			"url_id": url_id,
			"counter": instances,
			"date": date
		}



	def set_update_instance(self, id, instances, date):

		return {
			"id": id,
			"date": date,
			"counter": instances
		}