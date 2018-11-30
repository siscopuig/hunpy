

class ContainerElement:

	"""
	Base class for extracted containers.

	"""

	def __init__(self, driver, config):
		"""
		:param driver:
		"""

		self.driver = driver
		self.config = config
		self.min_pixels = self.config['advert.min_pixels']
		self.min_dimension = self.config['advert.min_dimension']

		# Attributes.
		self.txt_id = self.config['txt.id']
		self.txt_name = self.config['txt.name']
		self.txt_src = self.config['txt.src']
		self.txt_title = self.config['txt.title']
		self.txt_style = self.config['txt.style']
		self.txt_onclick = self.config['txt.onclick']
		self.txt_href = self.config['txt.href']

		# Xpath
		self.x_body = self.config['x.body']		# .//body
		self.x_iframe = self.config['x.iframe']		# .//iframe
		self.x_iframe_n = self.config['x.iframe_n']	# .//iframe[{}]
		self.x_equals = self.config['x.equals']		# '@{}="{}"'
		self.x_contains = self.config['x.contains']	# contains(@{}, "{}")
		self.x_and = self.config['x.and']		# ' and '
		self.x_img = self.config['x.img']		# .//img
		self.x_aimg = self.config['x_aimg']		# .//a/img
		self.x_a_img = self.config['x.a_img']		# .//a//img
		self.x_ancestor_a = self.config['x.ancestor_a'] # ./ancestor::a


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