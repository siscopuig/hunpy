
from urllib.parse import quote
from functools import reduce

chars = {
	'%3A': ':',
	'%2F': '/',
	'%3F': '?',
	'%23': '#',
	'%5B': '[',
	'%5D': ']',
	'%40': '@',
	'%21': '!',
	'%24': '$',
	'%26': '&',
	'%27': '\'',
	'%28': '(',
	'%29': ')',
	'%2A': '*',
	'%2B': '+',
	'%2C': ',',
	'%3B': ';',
	'%3D': '=',
	'%25': '%'
}

def encode_url(url):

	# Apply a function of two arguments cumulatively to the items of a sequence,
	# from left to right, so as to reduce the sequence to a single value.
	# For example, reduce(lambda x, y: x+y, [1, 2, 3, 4, 5]) calculates
	# ((((1+2)+3)+4)+5).  If initial is present, it is placed before the items
	# of the sequence in the calculation, and serves as a default when the
	# sequence is empty.
	#
	# reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
	# Output: 15


	# bad  -> http://www.gestiondefortune.com/gestion-d’actifs.html
	# good -> http://www.gestiondefortune.com/gestion-d%E2%80%99actifs.html

	return reduce(lambda x, y: x.replace(y, chars[y]), chars, quote(url))
