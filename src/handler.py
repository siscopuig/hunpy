
from connector.mysql_connector import MysqlConn
from src.driver import Driver
from src.page import Page
from src.searchers.iframe_searcher import FrameSearcher
from src.extractors.iframe_extractor import IframeExtractor
from src.searchers.image_searcher import ImageSearcher
from src.extractors.image_extractor import ImageExtractor
from src.log import Log



class Handler:
	"""
	- Get all the config data at this point.
	- Loop over the urls and process url (page)
	-
	"""

	driver = None
	page   = None


	def __init__(self, conf_data):
		self.urls = conf_data['urls']
		self.config = conf_data
		self.conn = MysqlConn()
		self.adverts = []
		self.log = Log()


	def search(self):
		

		for url in self.urls:


			# For debugging purposes:
			url = 'http://localhost:63342/hunpy/lab/html_templates/html_main_document.html'
			# url = 'https://www.trustnet.com/'
			#url = 'http://www.ftadviser.com/'
			# url = 'http://www.europeanpensions.net/ep/index.php'
			# url = 'https://www.theguardian.com/uk'
			#url = url[1]

			# @todo: do not set an item in config. Change approach
			self.config.__setitem__('main_document', url)

			self.manage_driver()

			self.process_page(url)




	def process_page(self, url):
		"""

		:param url:
		:return:
		"""

		self.driver.open(url, 1)

		self.process_frames(self.driver, url)

		self.process_images(self.driver)

		self.store_in_database()


	def process_frames(self, driver, url):
		"""

		:param driver:
		:param url:
		:return:
		"""

		page = Page(url)

		containers = FrameSearcher(driver).find_containers(page)


		if not containers:
			self.log.debug('No iframe containers found')
			return False

		frame_extractor = IframeExtractor(driver, self.config)
		adverts = frame_extractor.iframes_extractor(containers)

		if not adverts:
			return False

		for advert in adverts:
			page.adverts.append(advert)


	def process_images(self, driver):

		image_searcher = ImageSearcher(driver)
		containers = image_searcher.find_images()

		if not containers:
			self.log.debug('No image containers found in main document')
			return False

		image_extractor = ImageExtractor(driver, self.config)
		adverts = image_extractor.images_extractor(containers)

		if not adverts:
			return False

		for advert in adverts:
			self.adverts.append(advert)


	def store_in_database(self):

		for key, advert in enumerate(self.adverts):
			self.conn.insert_advert(advert)


	def manage_driver(self):
		"""

		:return:
		"""
		if self.driver is None:
			self.driver = Driver()
			self.driver.start()







#################################
# try:
# 	self.driver.open(url, 4)
# 	height = self.driver.driver.execute_script("return document.body.parentNode.scrollHeight")
# 	self.driver.driver.set_window_size(1366, height)
# 	self.driver.driver.save_screenshot('/home/sisco/PycharmProjects/hunpy/screenshot.png')
# except Exception as e:
# 	print(e)

