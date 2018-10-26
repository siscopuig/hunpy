#from src.hunpy_exception import HunpyException
from src.config import Config
from src.driver import Driver
from src.page import Page
from src.searchers.iframe_searcher import FrameSearcher
from src.extractors.iframe_extractor import IframeExtractor
from src.extractors.container_extractor import ContainerExtractor
from src.extractors.image_extractor import ImageExtractor
import datetime
from connector.mysql_connector import MysqlConn
from src.searchers.image_searcher import ImageSearcher


class Bootstrap:

	def __init__(self):
		self.config = None
		self.conn = MysqlConn()


	def test(self):
		url = 'http://localhost:63342/hunpy/lab/html_templates/html_main_document.html'
		# url = 'https://www.trustnet.com/'
		# url = 'http://www.ftadviser.com/'
		# url = 'http://www.europeanpensions.net/ep/index.php'
		# url = 'https://www.theguardian.com/uk'

		self.load_configuration(url)


		driver = Driver()
		driver.open(url)
		page = Page(url)


		# Frame searcher
		#f = FrameSearcher(driver)
		#containers = f.find_containers(page)
		# Frame Extractor
		#fe = IframeExtractor(driver, self.config)
		#adverts = fe.iframes_extractor(containers)
		#print(adverts)


		# Images Searcher
		img = ImageSearcher(driver)
		containers = img.find_images()
		# Images Extractor
		foo = ImageExtractor(driver, self.config)
		foo.images_extractor(containers)

		# for key, advert in enumerate(adverts):
		#	self.conn.insert_advert(advert)




	def test2(self):
		# '%Y%m%d%H%M%S%f'
		time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		# time = time
		print(time)


	def load_configuration(self, page):
		self.config = Config('hunpy')
		self.config.set_datasource_properties()
		self.config.load('../config/hunpy.yml')
		self.config.__setitem__('page', page)




##########################################
obj = Bootstrap()
obj.test()
#obj.test2()

# driver.click_using_middle_button(element)
#
# windows = driver.get_windows_handler()
# driver.get_driver().switch_to_window(windows[1])
# landing = driver.get_driver().current_url
# print(landing)
# driver.get_driver().close()
# driver.get_driver().switch_to_window(windows[0])
# element = driver.find_element_by_xpath('.//img')






