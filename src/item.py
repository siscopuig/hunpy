


class Item:

	"""
	Candidate
	"""

	def __init__(self):

		# Main parent container
		self.element = None
		self.size = None
		self.location = None

		self.is_known_placement = None
		self.is_known_adserver = None
		self.is_page_domain = None


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
		self.is_advert = None



