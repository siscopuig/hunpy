from src.config import Config



class ContainerElement:

	"""
	Base class for extracted containers.

	"""

	def __init__(self, driver, config):
		"""
		:param driver:
		"""

		self.driver = driver
		self.conf = Config('hunpy')
		self.min_pixels = self.conf['advert.min_pixels']
		self.min_dimension = self.conf['advert.min_dimension']

		# Attributes.
		self.txt_id 	= self.conf['txt.id']
		self.txt_name 	= self.conf['txt.name']
		self.txt_src 	= self.conf['txt.src']
		self.txt_title 	= self.conf['txt.title']
		self.txt_style 	= self.conf['txt.style']
		self.txt_onclick = self.conf['txt.onclick']
		self.txt_href 	= self.conf['txt.href']

		# Xpath
		self.x_body 		= self.conf['x.body']		# .//body
		self.x_iframe 		= self.conf['x.iframe']		# .//iframe
		self.x_iframe_n 	= self.conf['x.iframe_n']	# .//iframe[{}]
		self.x_equals 		= self.conf['x.equals']		# '@{}="{}"'
		self.x_contains 	= self.conf['x.contains']	# contains(@{}, "{}")
		self.x_and 			= self.conf['x.and']		# ' and '
		self.x_img 			= self.conf['x.img']		# .//img
		self.x_aimg 		= self.conf['x_aimg']		# .//a/img
		self.x_a_img 	  	= self.conf['x.a_img']		# .//a//img
		self.x_ancestor_a 	= self.conf['x.ancestor_a'] # ./ancestor::a


	def is_valid_container(self, container):

		if not self.is_visible(container):
			return False

		# The *args and **keywordargs forms are used for passing lists
		# of arguments and dictionaries of arguments, respectively
		return self.is_valid_size(*container.size)


	def is_visible(self, container):

		if not container.element:
			return False

		return self.driver.is_element_displayed(container.element)


	def is_valid_size(self, width, height):

		# If width, height greater that min_dimension AND
		# max_pixels greater or equal than min_pixels
		return (width > self.min_dimension) and (height > self.min_dimension) and \
			   ((width * height) >= self.min_pixels)