from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect_cond
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchFrameException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchAttributeException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.chrome.options import Options
import time
import io
from PIL import Image
# from selenium.webdriver.common.keys import Keys




def ewe(func):
	"""
	Execute without exceptions
	"""

	def wrapper(self, *args, **kwargs):
		"""
		Some functions do not return anything unless is an exception.
		We could assume that if None is True. E.g. switch_to_frame()

		:param self:
		:param args:
		:param kwargs:
		:return:
		"""
		try:

			#print('Driver::{}'.format(func))
			result = func(self, *args, **kwargs)

			# switch_to_element() -> returns None if switched, otherwise throws

			if result is None:
				return True
			else:
				return result

		# Timeout! what can do with this?
		except TimeoutException as e:
			#print('Exception: {} Executed function::{}'.format(e.msg, func))
			return False

		except NoSuchWindowException as e:
			#print('Exception: {} Executed function::{}'.format(e.msg, func))
			return False

		except NoSuchFrameException as e:
			#print('Exception: {} Executed function::{}'.format(e.msg, func))
			return False

		# Thrown when element could not be found.
		except NoSuchElementException as e:
			#print('Exception: {} Executed function::{}'.format(e.msg, func))
			return False

		# Thrown when the attribute of element could not be found.
		except NoSuchAttributeException as e:
			#print('Exception: {} Executed function::{}'.format(e.msg, func))
			return False

		# Stale means the element no longer appears on the DOM of the page.
		except StaleElementReferenceException as e:
			#print('Exception: {} Executed function::{}'.format(e.msg, func))
			return False

		# Thrown when an element is present on the DOM, but
		# it is not visible, and so is not able to be interacted with.
		except ElementNotVisibleException as e:
			#print('Exception: {} Executed function::{}'.format(e.msg, func))
			return False

		# For debugging purposes:
		except WebDriverException as e:
			print(e)


	return wrapper



class Driver:


	def __init__(self):
		self.driver = None
		self.chrome_options = None


	@ewe
	def start(self):
		"""

		:return:
		"""

		self.set_chrome_options()
		self.driver = webdriver.Chrome(chrome_options=self.chrome_options)
		self.driver.set_window_size(1366, 768)
		self.driver.set_page_load_timeout(10)
		self.driver.implicitly_wait(0)
		#self.driver.maximize_window()


	def set_chrome_options(self):

		user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64_59.0.3071.86 Safari/537.36'
		prefs = {'profile.default_content_setting_values.notifications': 2}

		self.chrome_options = Options()
		self.chrome_options.add_argument('--user-data-dir=/home/sisco/PycharmProjects/hunpy/profile')
		self.chrome_options.add_argument('--window-size=1366x768')
		self.chrome_options.add_argument('--user-agent=' + user_agent)
		self.chrome_options.add_argument('--ignore-ssl-errors=true')

		self.chrome_options.add_experimental_option(
			'prefs', prefs
		)

		# self.chrome_options.arguments(
		# 	'--window-size=1366x768',
		# 	'--user-agent=' + self.user_agent,
		# 	'--ignore-certificate-errors',
		# 	'--ignore-ssl-errors=true',
		# 	'--dns-prefetch-disable',
		# 	'--disable-infobars',
		# 	'--disable-session-crashed-bubble',
		# 	'--disable-notifications',
		# 	'--no-sandbox',
		# 	#'--headless',
		# 	#'--disable-gpu',
		# )

	@ewe
	def get_driver(self):
		"""

		:return:
		"""
		if self.driver is None:
			self.start()
		return self.driver


	def reset_driver(self):
		"""

		:return:
		"""
		self.driver = None


	@ewe
	def open(self, url, wait=None):
		"""

		:param wait:
		:param url:
		:return:
		"""
		self.get_driver().get(url)

		if wait:
			time.sleep(wait)


	def quit(self):
		"""

		:return:
		"""
		self.driver.quit()


	@ewe
	def find_elements_by_xpath(self, xpath):
		"""

		:param xpath:
		:return:
		"""
		return self.get_driver().find_elements_by_xpath(xpath)


	@ewe
	def find_element_by_xpath(self, xpath):
		"""

		:param xpath:
		:return:
		"""
		return self.get_driver().find_element_by_xpath(xpath)


	@ewe
	def find_element_parent_by_child(self, child_element, xpath):
		"""

		:param child_element:
		:param xpath:
		:return:
		"""
		return child_element.find_element_by_xpath(xpath)



	@ewe
	def get_element_size(self, element):
		"""

		:param element:
		:return:
		"""
		return element.size['width'], element.size['height']


	@ewe
	def get_element_location(self, element):
		"""

		:param element:
		:return:
		"""
		return element.location['x'], element.location['y']


	@ewe
	def get_element_attribute(self, element, attr):
		"""

		:param element:
		:param attr:
		:return:
		"""

		# val = element.get_attribute(attr)
		# if val is None:
		# 	return ''
		# return val

		return element.get_attribute(attr) or ''


	@ewe
	def close(self):
		"""

		:return:
		"""
		self.driver.close()


	@ewe
	def get_window_size(self):
		"""

		:return:
		"""
		return self.driver.get_window_size()


	@ewe
	def switch_to_main_document(self):
		"""

		:return:
		"""
		self.get_driver().switch_to.default_content()


	@ewe
	def switch_to_iframe(self, element):
		"""

		:param element:
		:return:
		"""
		self.get_driver().switch_to.frame(element)


	@ewe
	def find_child_element_by_xpath(self, xpath, parent_element):
		"""

		:param xpath:
		:param parent_element:
		:return:
		"""
		result = parent_element.find_element_by_xpath(xpath)
		return result


	@ewe
	def is_element_displayed(self, element):
		"""
		Whether the element is visible to a user

		:param element:
		:return: Boolean
		"""
		return element.is_displayed()


	@ewe
	def is_visibility_of_element_located(self, xpath):
		"""
		Given the generated xpath reference find the element of an element
		previously seen.
		Does not work at the moment!!
		:param xpath:
		:return:
		"""
		WebDriverWait(self.get_driver(), 2, 0.2).until \
			(expect_cond.visibility_of_element_located(self.get_driver().find_element_by_xpath(xpath)))


	@ewe
	def wait_for_element_visibility(self, element):
		"""

		:param element:
		:return: the (same) WebElement once it is visible
		"""
		return WebDriverWait(self.get_driver(), 2, 0.2).until(expect_cond.visibility_of(element))


	@ewe
	def click_on_element(self, element):
		"""
		On chrome, pressing the middle button of the mouse links are forced
		to open a new tab. (Appears that so not work anymore)

		Open links in a new tab -> Send Keys -> Ctrl + Shift + click


		:return None
		"""

		# Is element visible?
		element = self.wait_for_element_visibility(element)
		if not element:
			return None

		# This method can open more than one tab
		#ActionChains(self.get_driver()).move_to_element(element).send_keys \
		#	(Keys.CONTROL + Keys.SHIFT).click().perform()

		ActionChains(self.get_driver()).move_to_element(element).click().perform()

		time.sleep(2)




	@ewe
	def get_window_handle(self):
		"""
		Returns the handles of all windows within the current session.
		:return:
		"""
		return self.get_driver().window_handles


	@ewe
	def switch_to_window(self, window_name):
		"""

		:param window_name:
		:return:
		"""
		self.get_driver().switch_to.window(window_name)



	def open_new_tab(self):
		"""
		There is a bug in chromedriver that prevent chrome
		to open a new tab sending keys (CONTROL + "t")

		"""
		#element = self.find_element_by_xpath('.//body')

		#ActionChains(self.get_driver()).send_keys(Keys.COMMAND + "t").click(element).perform()

		# ActionChains(self.get_driver()).key_down(Keys.CONTROL).click(element)\
		# 	.send_keys('t').perform()
		pass

	@ewe
	def execute_script(self, script):
		"""
		Opens a new tab on browser window.

		"""
		self.get_driver().execute_script(script)



	def save_screenshot(self, filename):

		# Gets the screenshot of the current element as a binary data.

		self.get_driver().save_screenshot(filename)


	@ewe
	def close_window_except_main(self):
		"""
		Close all tabs opened except (0)

		:return: None
		"""

		# Get windows instances
		windows = self.get_window_handle()


		for i, window in enumerate(windows):
			if i != 0:
				self.switch_to_window(window)
				self.close()
		self.switch_to_window(windows[0])


	@ewe
	def get_current_url(self):
		"""
		Get current url from windows in focus

		:return: current url
		"""
		return self.get_driver().current_url


	def get_screenshot_element(self):

		element = self.driver.find_element_by_xpath('.//img')
		location = self.driver.get_element_location(element)
		size = self.driver.get_element_size(element)
		self.driver.save_screenshot('page_image.png')

		x = location[0]
		y = location[1]

		width = x + size[0]
		height = y + size[1]

		image = Image.open(io.FileIO('page_image.png'))
		image = image.crop((int(x), int(y), int(width), int(height)))
		image_rgb = image.convert('RGB')
		image_rgb.save('sample_screenshot_3.jpeg', format('JPEG'))


##########################################
# if __name__ == '__main__':
# 	url_web = 'http://siscopuig.com'
# 	driver = Driver()
# 	driver.create()
# 	driver.open(url_web)
# 	size = driver.get_window_size()
# 	driver.close()
# 	print('Stop')

