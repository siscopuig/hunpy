# -*- coding: utf-8 -*-

class Item:
	"""
	Candidate
	"""

	def __init__(self):

		self.element = None  # Main parent container

		self.size = None

		self.location = None

		self.isframe = None

		self.is_known_placement = None

		self.is_known_adserver = None

		self.is_page_domain = None

		self.is_advertiser_missing = True

		self.instance = {}

		self.iframe_srcs = []

		self.img_srcs = []

		self.img_hrefs = []

		self.img_onclicks = []

		self.ids = []

		self.names = []

		self.titles = []

		self.styles = []

		# Processed data
		self.src = None

		self.advertiser = None

		self.landing = None

		self.xpath = ''

		self.finfo = None