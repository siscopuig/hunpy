from src.containers.container_element import ContainerElement
from src.image import Image
import numpy as np


class ImageSearcher(ContainerElement):
	"""
	Search for images in main document
	"""

	def __init__(self, driver):
		super().__init__(driver)


	def find_images(self):
		"""
		"""

		img_elements = self.driver.find_elements_by_xpath(self.x_img)
		if not img_elements:
			return []

		n_containers = len(img_elements)
		containers = np.empty(n_containers, dtype=np.object)

		i = 0
		for img_element in img_elements:

			anchors = set()

			container = Image()

			container.src = self.driver.get_element_attribute(img_element, self.txt_src)
			if not container.src:
				continue

			container.element 	= img_element
			container.size 		= self.driver.get_element_size(container.element)
			container.location 	= self.driver.get_element_location(container.element)


			if not self.is_valid_container(container):
				continue

			# Find the anchor element of the image element if any. Looks for the relative anchor ancestor:
			# ./ancestor::a
			container.a_element = self.driver.find_child_element_by_xpath(self.x_ancestor_a, img_element)

			if container.a_element in anchors:
				continue

			anchors.add(container.a_element)

			container.onclick = self.driver.get_element_attribute(img_element, self.txt_onclick)
			container.style   = self.driver.get_element_attribute(img_element, self.txt_style)

			# Does it need to check for and anchor inside a container at this point?
			if container.a_element:
				container.a_href 	= self.driver.get_element_attribute(container.a_element, self.txt_href)
				container.a_onclick = self.driver.get_element_attribute(container.a_element, self.txt_onclick)
				container.a_style	= self.driver.get_element_attribute(container.a_element, self.txt_style)

			containers[i] = container
			i += 1
			if i >= n_containers:
				break

		return containers[:i]




	# def find_images(self):
	#
	# 	images = []
	#
	# 	elements = self.driver.find_elements_by_xpath(self.x_img)
	#
	# 	for element in elements:
	#
	#
	# 		image = Image()
	#
	# 		image.element = element
	# 		image.location = self.driver.get_element_location(element)
	# 		image.size = self.driver.get_element_size(element)
	#
	# 		if not self.is_valid_size(image.size[0], image.size[1]):
	# 			continue
	#
	# 		image.img_src = self.driver.get_element_attribute(element, self.txt_src)
	# 		image.img_onclick = self.driver.get_element_attribute(element, self.txt_onclick)
	# 		image.img_style = self.driver.get_element_attribute(element, self.txt_style)
	#
	#
	# 		ancestor = self.driver.find_element_parent_by_child(element, self.x_ancestor_a)
	# 		if ancestor:
	# 			image.a_href = self.driver.get_element_attribute(ancestor, self.txt_href)
	# 			image.a_onclick = self.driver.get_element_attribute(ancestor, self.txt_onclick)
	# 			image.a_style = self.driver.get_element_attribute(ancestor, self.txt_style)
	# 			# print('<a href: {}'.format(image.a_href))
	# 			# print('<img src: {}'.format(image.img_src))
	#
	# 		images.append(image)
	#
	# 	# Return list of objects
	# 	return images


#################################
# No needed for now
# self.img_attr_tags = np.array([
# 	['src', self.txt_src],
# 	['onclick', self.txt_title],
# 	['style', self.txt_style]
# ])
#
# self.a_attr_tags = np.array([
# 	['href', self.txt_src],
# 	['onclick', self.txt_onclick],
# 	['style', self.txt_style]
# ])

# self.element = None
# self.xpath = None
# self.hashref = None
# self.size = (-1, -1)
# self.location = (-1, -1)

# self.img_src = None
# self.img_onclick = None
# self.img_style = None
#
# self.a_href = None
# self.a_onclick = None
# self.a_style = None



