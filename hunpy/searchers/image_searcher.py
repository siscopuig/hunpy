# -*- coding: utf-8 -*-

import numpy as np
from hunpy.searchers.container_searcher import ContainerSearcher
from hunpy.log import Log
from hunpy.image import Image


class ImageSearcher(ContainerSearcher):
	"""
	Search for images in main document
	"""

	def __init__(self, driver, config):

		super().__init__(driver, config)

		self.log = Log()


	def find_containers(self):

		containers = np.array(self.find_images(), dtype=np.object)
		if containers.size == 0:
			return []

		return containers


	def find_images(self):

		img_elements = self.driver.find_elements_by_xpath(self.x_img)
		if not img_elements:
			return []

		n_containers = len(img_elements)
		containers = np.empty(n_containers, dtype=np.object)

		i = 0
		for img_element in img_elements:

			anchors = set()

			# Image container
			img_cont = Image()

			img_cont.src = self.driver.get_element_attribute(img_element, self.txt_src)
			if not img_cont.src:
				continue

			img_cont.element = img_element
			img_cont.size = self.driver.get_element_size(img_cont.element)
			img_cont.location = self.driver.get_element_location(img_cont.element)

			if not self.is_valid_container(img_cont):
				continue

			# Find the anchor element of the image element if any. Looks for the relative anchor ancestor:
			# ./ancestor::a
			img_cont.a_element = self.driver.find_child_element_by_xpath(self.x_ancestor_a, img_element)

			if img_cont.a_element in anchors:
				continue

			anchors.add(img_cont.a_element)
			img_cont.onclick = self.driver.get_element_attribute(img_element, self.txt_onclick)
			img_cont.style   = self.driver.get_element_attribute(img_element, self.txt_style)

			if img_cont.a_element:
				img_cont.a_href = self.driver.get_element_attribute(img_cont.a_element, self.txt_href)
				img_cont.a_onclick = self.driver.get_element_attribute(img_cont.a_element, self.txt_onclick)
				img_cont.a_style = self.driver.get_element_attribute(img_cont.a_element, self.txt_style)

			# For debugging purposes only
			self.log.debug(img_cont.__str__())

			containers[i] = img_cont
			i += 1
			if i >= n_containers:
				break

		return containers[:i]


