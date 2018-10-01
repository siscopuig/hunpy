from selenium import webdriver
from src import driveroptions

class Driver(driveroptions.DriverOptions):

	driver = ''


	def __init__(self):
		super().__init__()


	def create(self):

		self.driver = webdriver.Chrome(
			chrome_options=self.chrome_options,
		)
		self.driver.set_page_load_timeout(10)
		self.driver.implicitly_wait(0)


	def get_driver(self):
		return self.driver


	def start(self):

		self.driver.get('http://siscopuig.com')
		self.driver.quit()




if __name__ == '__main__':
	driver = Driver()
	driver.create()
	driver.start()



