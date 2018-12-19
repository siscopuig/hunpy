import re


class UtilsString:



	@staticmethod
	def match_string_in_list(string, string_list):
		"""

		:param string:
		:param string_list:
		:return: boolean
		"""

		casefold_string = string.casefold()
		for str in string_list:
			if (str is string or string is str) or (str.casefold() in casefold_string):
				return True

		return False


	@staticmethod
	def match_string_parts_in_list(parts, string_list):

		# match_string_parts_in_list(ignore_path) string: ads in str: uploads
		# https://s0.2mdn.net/ads/richmedia/studio/pv2/60817163/20180903024843963/index.html

		# 'is' is used for identity comparison, while == is used for equality comparison

		# So, when you have two string literals (words that are literally typed into your
		# program source code, surrounded by quotation marks) in your program that have
		# the same value, the Python compiler will automatically intern the strings, making
		# them both stored at the same memory location. (Note that this doesn't always happen,
		# and the rules for when this happens are quite convoluted, so please don't rely
		# on this behavior in production code!)
		#
		# Since in your interactive session both strings are actually stored in the same
		# memory location, they have the same identity, so the `is` operator works as expected.
		# But if you construct a string by some other method (even if that string contains
		# exactly the same characters), then the string may be equal, but it is not
		# the same string -- that is, it has a different identity, because it is stored
		# in a different place in memory.

		for part in parts:
			for str in string_list:
				if (part is not '' and part == str) or (part.casefold() == str.casefold()):
					return True
		return False


	@staticmethod
	def strip_query_in_source(source):

		if '?' in source:
			return source.split('?')[0]
		elif '#' in source:
			return source.split('#')[0]

		return source


	@staticmethod
	def get_paths_from_source(source):

		source = UtilsString.strip_query_in_source(source)
		source = UtilsString.strip_scheme_protocol(source)
		domain = source.split('/')[0]
		path = source.replace(domain, '')
		return path.split('/')


	@staticmethod
	def get_domain(url):

		src = UtilsString.strip_scheme_protocol(url)
		return src.split('/')[0]


	@staticmethod
	def match_placement(placements, width, height):
		"""
		"""
		for size in placements:
			if size[0] == width and size[1] == height:
				return True
		return False


	@staticmethod
	def strip_string(string, delimeter=None):
		"""
		Strip any characters after the delimeter char

		:param string:
		:param delimeter:
		:return:
		"""
		exploded = string.split(delimeter)

		if len(exploded) == 1:
			return string

		exploded.pop(-1)

		return exploded[0]


	@staticmethod
	def get_url_from_string(string):
		"""
		Finds a url inside a string

		E.g. https://adclick.g.doubleclick.net/pcs/click?xai=AKAOjsvhOqNiIi3Zv-
		JwQKu7K3VwVXzzhphDRT4O8FZ48g9A3QHmZ0m-m58ugEOY7GrBMuA_T4DfhkyDRm12fX8BlFD
		JK3df8lhzM9kIzjWg2w342TC7S3B1UFUH6qc-qj8ElBwxvEZJ7UiGVqgi5pJHqEVq8i9kNcxDLZ
		FqdmUT4DexaYprDksioGNurfK-RQ2qaFdb21kwvEhJ9x9Px1Wu3kLIRHhIh71kLpOLsLWO7t9vD
		3w1WfmlWrcpuUvLfd31zQy2&sai=AMfl-YSmUDAw5oZbgx8BID9_3GzlxdLUM-sCS7oadMMYImbQ
		YLnlaWVdI9DY0zOTl1zgla8uu9HGyIuv_gQHP2ExfND_6Vbm29FXV3pHLu6_5wQsZ0-mOFLxgssHL
		XUj&sig=Cg0ArKJSzAcOvYMZk5ZOEAE&urlfix=1&adurl=
		https://servedby.flashtalking.com/click/1/98145;3371049;2367840;210;0/
		?ft_impID=6A4E4B98-DA0F-88F7-361E-3BA1078F0145&g=3947060DBD153D&random=55963&ft_width=300&ft_height=600&url=
		https://www.rlam.co.uk/Home/Intermediaries/Products/Fixed-Income/OEICs/Monthly-Income-Bond-Fund/
		?utm_source=FTAdviser&utm_medium=Half%20Page&utm_campaign=MIB%202018

		:param string:
		:return: None or url
		"""

		# Return a list of all non-overlapping matches in the string.
		# urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)

		# Outputs: ['https://adclick.g.doubleclick.net', 'https://servedby.flashtalking.com', 'https://www.rlam.co.uk']
		# urls = re.findall('http[s]?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', string)

		# Outputs: [
		# 	'https://adclick.g.doubleclick.net/pcs/click',
		#	'https://servedby.flashtalking.com/click/1/98145',
		#	'https://www.rlam.co.uk/Home/Intermediaries/Products/Fixed-Income/OEICs/Monthly-Income-Bond-Fund/'
		# ]
		urls = re.findall('http[s]?://(?:(?!http[s]?://)[a-zA-Z]|[0-9]|[$\-_@.&+/]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)

		if not urls:
			return None

		# Returns last element
		return urls.pop(-1)


	@staticmethod
	def return_test():

		request = {
			"status": 200,
			"content_type": "text/html"
		}
		src = 'source'

		return src, request


	@staticmethod
	def get_scheme_protocol_from_url(url):

		schemes = [
			'https://www',
			'http://www',
			'https://',
			'http://'
		]

		for scheme in schemes:
			if scheme in url:
				return scheme


	@staticmethod
	def strip_scheme_protocol(url):

		source = re.compile(r"https?://(www\.)?")
		return source.sub('', url)



	# WORK IN PROGRESS
	@staticmethod
	def strip_landing(source):

		# Strip schema (http://www, https://www, http://, https://)
		# Strip source in parts (/)

		# Returns first split


		return source.split('?', 1)[0]





#############################
# src = 'http://adclick.g.doubleclick.net/pcs/click?xai=AKAOjsvhOqNiIi3Zv-' \
# 	  'JwQKu7K3VwVXzzhphDRT4O8FZ48g9A3QHmZ0m-m58ugEOY7GrBMuA_T4DfhkyDRm12fX8BlFD' \
# 	  'JK3df8lhzM9kIzjWg2w342TC7S3B1UFUH6qc-qj8ElBwxvEZJ7UiGVqgi5pJHqEVq8i9kNcxDL' \
# 	  'ZFqdmUT4DexaYprDksioGNurfK-RQ2qaFdb21kwvEhJ9x9Px1Wu3kLIRHhIh71kLpOLsLWO7t9vD3w' \
# 	  '1WfmlWrcpuUvLfd31zQy2&sai=AMfl-YSmUDAw5oZbgx8BID9_3GzlxdLUM-sCS7oadMMYImbQYLn' \
# 	  'laWVdI9DY0zOTl1zgla8uu9HGyIuv_gQHP2ExfND_6Vbm29FXV3pHLu6_5wQsZ0-mOFLxgssHLXUj&s' \
# 	  'ig=Cg0ArKJSzAcOvYMZk5ZOEAE&urlfix=1&adurl=https://servedby.flashtalking.com/click' \
# 	  '/1/98145;3371049;2367840;210;0/?ft_impID=6A4E4B98-DA0F-88F7-361E-3BA1078F0145&g=' \
# 	  '3947060DBD153D&random=55963&ft_width=300&ft_height=600&url=' \
# 	  'https://www.rlam.co.uk/Home/Intermediaries/Products/Fixed-Income/OEICs/Monthly-Income-Bond-Fund/' \
# 	  '?utm_source=FTAdviser&utm_medium=Half%20Page&utm_campaign=MIB%202018'
# url = UtilsString.strip_landing(src)
# # print(url)
