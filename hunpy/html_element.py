

class HtmlElement:
	"""
	Represents any DOM structure
	"""

	def __init__(self, parent=None):

		self.parent = parent

		# Does count level of nested within html element
		self.level = 0
		document = self
		while document.parent:
			self.level += 1
			document = document.parent

		self.element = None
		self.size = None
		self.location = None

		self.id = ''
		self.name = ''
		self.src = ''
		self.title = ''
		self.style = ''

		# Content.
		self.anchor_imgs = []
		self.img_srcs = []
		self.onclicks = []
		self.iframes = []
		self.images = []

		# Referencing.
		self.xpath = ''
		self.hashref = ''


	def is_invalid_child(self, document):

		if not self.is_recursive(document):
			return False
		return True


	def is_recursive(self, document):
		"""
		Checks that child source is not the same as the parent in order to avoid duplicates.
		"""
		ancestor = document.parent
		while ancestor:
			if (document.src or ancestor.src) and (document.src == ancestor.src):
				return True
			ancestor = ancestor.parent

		return False
