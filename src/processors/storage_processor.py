from src.processor import Processor


class StorageProcessor(Processor):


	def __init__(self, driver, config, datasource):

		# Call parent class Processor
		super().__init__(driver, config, datasource)



	def process(self, page):


		self.store_adverts_in_database()



	# IN CONSTRUCTION...
	def store_adverts_in_database(self):


		if not self.page.adverts:
			return False

		for advert in self.page.adverts:

			if advert.state.name == 'EXISTING':
				# Update instances
				self.update_existing_advert(advert)

			if advert.state.name == 'NEW':
				# Insert new advert in Adverts
				self.store_new_advert(advert)

				# Create new instance record
				self.store_new_instance(advert)



	# IN CONSTRUCTION...
	def store_new_advert(self, advert):

		# Insert new advert record in database
		self.datasource.insert_new_advert_in_database(advert)



	# IN CONSTRUCTION...
	def store_new_instance(self, advert):

		# First, gather the values needed to do the process
		result = advert.datetime.split(' ')
		uid = advert.uid
		url_id = self.page.url_id
		date = result[0]
		instances = advert.instances

		data = self.set_new_instance(uid, url_id, date, instances)
		self.datasource.insert_new_instance_record(data['uid'], data['url_id'], data['counter'], data['date'])


	# IN CONSTRUCTION...
	def update_existing_advert(self, advert):

		# First, find whether the advert instance is a new record today:
		# 	- query the database in order to find it.

		result = advert.datetime.split(' ')

		uid = advert.uid
		url_id = self.page.url_id
		date = result[0]
		instances = advert.instances

		instance_id = self.datasource.is_new_instance_record_in_database(uid, url_id, date)

		if instance_id:
			# there is an existing instance record today (Update instance).
			# Update existing instance record today.
			data = self.set_update_instance(instance_id, date, instances)
			self.datasource.update_existing_instance_record(data['id'], data['date'], data['counter'])

		else:
			# Store new instance record for today
			data = self.set_new_instance(advert.uid, self.page.url_id, date, instances)
			self.datasource.insert_new_instance_record(data['uid'], data['url_id'], data['counter'], data['date'])


	def set_new_instance(self, uid, url_id, date, instances):

		return {
			"uid": uid,
			"url_id": url_id,
			"counter": instances,
			"date": date
		}


	def set_update_instance(self, id, date, instances):

		return {
			"id": id,
			"date": date,
			"counter": instances
		}

























