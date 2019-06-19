class Container:

	"""
	Base class for extracted containers.

	"""

	def __init__(self):

		self.element = None

		self.size = (-1, -1)

		self.location = (-1, -1)

		self.path = ''

		self.hashref = ''


	def __str__(self):

		return (

			' element:      {element}\n'
			' size:         {size}\n'
			' location:     {location}\n'

		).format(
			element=self.element,
			size=self.size,
			location=self.location,
		)