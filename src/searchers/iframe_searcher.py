from src.iframe import Iframe
from src.containers.container_element import ContainerElement
from src.searchers.image_searcher import ImageSearcher
from src.image import Image
from src.page import Page
import numpy as np
import hashlib
from src.log import Log


class FrameSearcher(ContainerElement):
	"""
	Search and extract main document elements(iframes, images, etc...)
	"""

	def __init__(self, driver):

		ContainerElement.__init__(self, driver)

		self.log = Log()

		self.driver = driver

		self.attri_tags = np.array([
			['id', 		self.txt_id],
			['name', 	self.txt_name],
			['src', 	self.txt_src],
			['title', 	self.txt_title],
			['style', 	self.txt_style]
		])


	def find_containers(self, page=None):
		"""
		"""
		containers = np.array(self.find_iframes(page), dtype=np.object)
		if containers.size == 0:
			return []

		return containers


	def find_iframes(self, parent):
		"""
		"""

		refs = []

		iframes = []

		elements = self.driver.find_elements_by_xpath(self.x_iframe)

		for element in elements:

			iframe = Iframe(parent)

			# Set iframe element
			iframe.element = element

			# Set element dimensions
			iframe.size = self.driver.get_element_size(element)
			if not iframe.size:
				continue

			# If focus still in main document continue
			if isinstance(parent, Page) and not self.is_valid_container(iframe):
				continue

			iframe.location = self.driver.get_element_location(element)
			if not iframe.location:
				continue

			# Process iframe attributes and store xpath hash references
			ref = self.process_iframe_ref(iframe, element)
			if not ref:
				continue

			if parent.is_invalid_child(iframe):
				continue

			if iframe.hashref in refs:
				continue

			# Add hash reference
			refs.append(iframe.hashref)


			iframes.append(iframe)


			self.log.debug(iframe.__str__())

		for i, iframe in enumerate(iframes):

			result = self.switch_to_iframe(iframe)
			if not result:
				continue

			# Find images inside an iframe
			iframe.images = self.find_images()

			# Recursive - it is calling itself
			iframe.iframes = self.find_iframes(iframe)

		self.driver.switch_to_main_document()

		return iframes


	# Reuse this find images for images in main document
	def find_images(self):
		"""
		"""
		img = ImageSearcher(self.driver)
		return img.find_images()


	def switch_to_iframe(self, iframe):
		"""

		:param iframe:
		:return:
		"""

		iframes = []

		while iframe.parent:
			iframes.append(iframe)
			iframe = iframe.parent

		# Switch to the main document.
		self.driver.switch_to_main_document()

		for iframe in reversed(iframes):

			element = self.driver.find_element_by_xpath(iframe.xpath)

			if element:
				if not self.driver.switch_to_iframe(element):
					return False

			else:
				element = self.find_element_by_hash(iframe.hashref)

				if element:
					if not self.driver.switch_to_iframe(element):
						return False
				else:
					return False

		return True


	def process_iframe_ref(self, iframe, element):
		"""
		setattr():
			We use setattr to add an attribute to our class instance.
			We pass the class instance, the attribute name, and the value.
			With getattr we retrieve these values.

		hashlib module - A common interface to many hash functions.

		A hash is a small refactoring of data that destroys virtually all
		of the information in the data. It is used to identify a revision
		of the data and can be used later to see if the data has changed.
		A good hash algorithm changes its output dramatically with even a
		1 character change in the data.

		md5():
			This hash function accepts sequence of bytes and returns 128 bit
			hash value, usually used to check data integrity but has security issues.

			Functions associated:
				encode() : Converts the string into bytes to be acceptable by hash function.
				digest() : Returns the encoded data in byte format.
				hexdigest() : Returns the encoded data in hexadecimal format.

		"""

		data = []
		for attr in self.attri_tags:
			val = self.driver.get_element_attribute(element, attr[1])
			if val:
				setattr(iframe, attr[0], val)
				data.append(self.x_equals.format(attr[1], val))

		if not data:
			return False

		iframe.xpath = self.x_iframe_n.format(self.x_and.join(data))
		iframe.hashref = hashlib.md5(iframe.xpath.encode()).hexdigest()

		return True


	def find_element_by_hash(self, hashref):
		"""

		"""

		# Try and find an element with the hash.
		elements = self.driver.find_elements_by_xpath(self.x_iframe)
		for element in elements:

			# Create a frame object and set the info.
			iframe = Iframe()

			# var iframe
			result = self.process_iframe_ref(iframe, element)

			if result and (hashref == iframe.hashref):
				return element

		return False



