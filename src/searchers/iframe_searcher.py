from iframe import Iframe
from containers.container_element import ContainerElement
from searchers.image_searcher import ImageSearcher
from page import Page
import numpy as np
import hashlib
from log import Log


class FrameSearcher(ContainerElement):
	"""
	Search and extract main document elements(iframes, images, etc...)
	"""

	def __init__(self, driver, datasource):

		super().__init__(driver, datasource)

		self.log = Log()

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

		# Loop over the elements
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


		for i, iframe in enumerate(iframes):


			result = self.switch_to_iframe(iframe)
			if not result:
				continue

			# Find images inside an iframe
			iframe.images = self.find_images()

			# Recursive - it is calling itself
			iframe.iframes = self.find_iframes(iframe)


		return iframes


	def find_images(self):
		"""
		"""
		return ImageSearcher(self.driver, self.config).find_containers()



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
		self.driver.switch_to_default_content()


		for iframe in reversed(iframes):


			element = self.driver.find_element_by_xpath(iframe.xpath)
			if element:

				#self.log.debug('Found frame {} using xpath {}'.format(iframe.hashref, iframe.xpath))

				if not self.driver.switch_to_iframe(element):
					#self.log.debug('Unable to switch to the iframe document')
					return False


			else:

				element = self.find_element_by_hash(iframe.hashref)
				if element:
					#self.log.debug('Found iframe {} using hash xpath {}'.format(iframe.hashref, iframe.xpath))

					if not self.driver.switch_to_iframe(element):
						#self.log.debug('Unable to switch to iframe document')
						return False

				else:
					#self.log.debug('Unable to find iframe {} using xpath or hash'.format(iframe.hashref))
					return False

		return True


	def process_iframe_ref(self, iframe, element):
		"""
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



